from uuid import uuid4
import json
from redis import Redis
from .job import NutsJob
from .cron import Cron
import datetime
import logging


class Worker():
    '''
        A NUTS worker
    '''
    id: str
    redis: Redis
    scheduler: Cron
    logger: logging.Logger
    jobs: list[NutsJob]
    kwargs: dict[str, any]
    scheduled_queue: str
    pending_queue: str
    completed_queue: str
    last_run: datetime.datetime
    running_list: str
    should_run: bool

    def __init__(self, redis: Redis, jobs: list[NutsJob], **kwargs):
        self.id = str(uuid4())
        self.scheduled_queue = 'nuts|jobs|scheduled'
        self.running_list = 'nuts|job|running'
        self.pending_queue = 'nuts|jobs|pending'
        self.completed_queue = 'nuts|jobs|completed'
        self.kwargs = kwargs
        self.should_run = True
        self.is_leader = False

        self.last_run = datetime.datetime.fromtimestamp(0)

        self.redis = redis

        self.scheduler = Cron()

        self.logger = logging.getLogger(f'worker|{self.id}')
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        self.jobs = []

        is_leader = self.check_leader()
        if is_leader:
            self.logger.info(f'Worker {self.id} assuming leadership')

        for job in jobs:
            j = job.Job()

            self.jobs.append(j)

            if is_leader and j.schedule:
                self.logger.info(f'Registering Cron Job {j.name}')

                next_execution = self.scheduler.get_next_execution(j.schedule).timestamp()
                scheduled_job = False
                running_job = None
                try:
                    pending = self.redis.zscan('nuts|jobs|pending', match=j.name)
                    if pending[1][0]:
                        if pending[1][1] != next_execution:
                            # Schedule has changed
                            self.redis.zrem(self.scheduled_queue, job.name)
                            self.redis.zadd(self.scheduled_queue, {job.name: next_execution})
                        else:
                            scheduled_job = True

                except Exception:
                    pass

                running_job = self.redis.hget(self.running_list, j.name)

                if not scheduled_job and not running_job:
                    self.redis.zadd(self.pending_queue, {j.name: next_execution})

    def check_leader(self) -> bool:
        leadership_check = self.redis.setnx('leader_id', self.id)

        if not leadership_check:
            leader_id = self.redis.get('leader_id')
            if leader_id == self.id:
                # Puts a 60 second life on the current leader so we aren't left in limbo if the leader worker dies ungracefully.
                self.redis.expire('leader_id', 60)

                self.is_leader = True

        else:
            # Puts a 60 second life on the current leader so we aren't left in limbo if the leader worker dies ungracefully.
            self.redis.expire('leader_id', 60)
            self.is_leader = True

    def shutdown(self, signum, frame):
        self.logger.info(f'Received shutdown command {signum}.')
        self.should_run = False

        if self.is_leader:
            self.release_leader()

    def release_leader(self):
        if self.is_leader:
            self.logger.info('Shutdown: Releasing leadership')
            self.redis.expire('leader_id', -1)

    def schedule_pending_job(self, job_name, job_params=[]):
        self.redis.sadd(self.pending_queue, json.dumps([job_name, job_params]))

    def move_scheduled_to_pending(self):
        now = datetime.datetime.now(datetime.timezone.utc)
        now_timestamp = round(now.timestamp())
        start = round(self.last_run.timestamp())

        ready_jobs = self.redis.zrange(self.scheduled_queue, start=start, end=now_timestamp, withscores=True)

        if len(ready_jobs) > 0:
            latest = max(j[0] for j in ready_jobs)
            self.redis.zremrangebyscore(self.scheduled_queue, min=self.last_run.timestamp(), max=latest)

        for job in ready_jobs:
            self.schedule_pending_job(job[0])

        self.last_run = now

    def move_pending_to_running(self, job: NutsJob, job_args: list):
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        self.redis.hset(self.running_list, f'{self.id}|{job.name}', json.dumps({'timestamp': now, 'args': job_args}))

    def remove_running(self, job: NutsJob):

        self.redis.hdel(self.running_list, f'{self.id}|{job.name}')

    def move_to_completed(self, job: NutsJob):
        self.redis.sadd(self.completed_queue, job.name)

    def queue_completed_jobs(self):

        completed_jobs = self.redis.smembers(self.completed_queue)

        for job_name in completed_jobs:
            self.redis.srem(self.completed_queue, job_name)
            job = [j for j in self.jobs if j.name == job_name.decode()][0]

            next_execution = self.scheduler.get_next_execution(job.schedule).timestamp()

            self.redis.zadd(self.scheduled_queue, {job.name: next_execution})

    def run(self):
        # Check that we have a leader each time this runs so we don't leave any jobs in limbo if the leader has gone down
        self.check_leader()

        if self.is_leader:
            # Move ready jobs to the pending queue
            self.move_scheduled_to_pending()

        try:
            data = self.redis.spop(self.pending_queue, 1)
            if not len(data):
                self.logger.info('No pending job data')
                return
            else:
                [job_name, job_args] = json.loads(data[0])

                jobs = [j for j in self.jobs if j.name == job_name]

                if not len(jobs):
                    self.logger.info(f'No job matches name {job_name}')
                    return
                else:
                    job = jobs[0]
                    self.move_pending_to_running(job, job_args)

                    try:
                        job.run(job_args, **self.kwargs)
                    except Exception as ex:
                        # Deal with user error gracefully
                        self.logger.error(f'Unhandled Exception In Job: {job.name}: {ex}')

                    self.remove_running(job)

                    if job.success:
                        self.logger.info(f'SUCCESS: {job.name}, {job.result}')
                        # Light DAG support, can chain together jobs in a workflow by defining the next step that should
                        # be taken after a job completes
                        if job.next:
                            self.schedule_pending_job(job.next, job.result)

                    else:
                        self.logger.error(f'Error running job {job.name}: {job.error}')

                    if job.schedule:
                        self.move_job_to_completed(job)

        except Exception as ex:
            self.logger.error(f'Unhandled Exception in worker run process: {ex}')

        # Post Execution

        if self.is_leader:
            self.queue_completed_jobs()
