import time
import threading

from cobweb.db import ApiDB
from cobweb.base import Seed, logger
from cobweb.constant import DealModel, LogTemplate
from .launcher import Launcher, check_pause


class LauncherApi(Launcher):

    def __init__(self, task, project, custom_setting=None, **kwargs):
        super().__init__(task, project, custom_setting, **kwargs)
        self._db = ApiDB()

        self._todo_key = "{%s:%s}:todo" % (project, task)
        self._done_key = "{%s:%s}:done" % (project, task)
        self._fail_key = "{%s:%s}:fail" % (project, task)
        self._heartbeat_key = "heartbeat:%s_%s" % (project, task)

        self._statistics_done_key = "statistics:%s:%s:done" % (project, task)
        self._statistics_fail_key = "statistics:%s:%s:fail" % (project, task)
        self._speed_control_key = "speed_control:%s_%s" % (project, task)

        self._reset_lock_key = "lock:reset:%s_%s" % (project, task)

        # self._bf_key = "bloom_%s_%s" % (project, task)
        # self._bf = BloomFilter(self._bf_key)

        self._heartbeat_start_event = threading.Event()
        self._redis_queue_empty_event = threading.Event()

    @property
    def heartbeat(self):
        return self._db.exists(self._heartbeat_key)

    def statistics(self, key, count):
        if not self._task_model and not self._db.exists(key):
            self._db.setex(key, 86400 * 30, int(count))
        else:
            self._db.incrby(key, count)

    def _get_seed(self) -> Seed:
        """
        从队列中获取种子（频控）
        设置时间窗口为self._time_window（秒），判断在该窗口内的采集量是否满足阈值（self._spider_max_speed）
        :return: True -> 种子, False -> None
        """
        if (self._speed_control and self.__LAUNCHER_QUEUE__["todo"].length and
                not self._db.auto_incr(self._speed_control_key, t=self._time_window, limit=self._spider_max_count)):
            expire_time = self._db.ttl(self._speed_control_key)
            logger.info(f"Too fast! Please wait {expire_time} seconds...")
            time.sleep(expire_time / 2)
            return None
        seed = self.__LAUNCHER_QUEUE__["todo"].pop()
        return seed

    @check_pause
    def _execute_heartbeat(self):
        if self._heartbeat_start_event.is_set():
            self._db.setex(self._heartbeat_key, 5)
        time.sleep(3)

    @check_pause
    def _reset(self):
        """
        检查过期种子，重新添加到redis缓存中
        """
        reset_wait_seconds = 30
        if self._db.lock(self._reset_lock_key, t=120):

            _min = -int(time.time()) + self._seed_reset_seconds \
                if self.heartbeat else "-inf"

            self._db.members(self._todo_key, 0, _min=_min, _max="(0")

            if not self.heartbeat:
                self._heartbeat_start_event.set()

            self._db.delete(self._reset_lock_key)

        time.sleep(reset_wait_seconds)

    @check_pause
    def _scheduler(self):
        """
        调度任务，获取redis队列种子，同时添加到doing字典中
        """
        if not self._db.zcount(self._todo_key, 0, "(1000"):
            time.sleep(self._scheduler_wait_seconds)
        elif self.__LAUNCHER_QUEUE__['todo'].length >= self._todo_queue_size:
            time.sleep(self._todo_queue_full_wait_seconds)
        else:
            members = self._db.members(
                self._todo_key, int(time.time()),
                count=self._todo_queue_size,
                _min=0, _max="(1000"
            )
            for member, priority in members:
                seed = Seed(member, priority=priority)
                self.__LAUNCHER_QUEUE__['todo'].push(seed)
                self.__DOING__[seed.to_string] = seed.params.priority

    @check_pause
    def _insert(self):
        """
        添加新种子到redis队列中
        """
        seeds = {}
        status = self.__LAUNCHER_QUEUE__['new'].length < self._new_queue_max_size
        for _ in range(self._new_queue_max_size):
            seed = self.__LAUNCHER_QUEUE__['new'].pop()
            if seed:
                seeds[seed.to_string] = seed.params.priority
        if seeds:
            self._db.zadd(self._todo_key, seeds, nx=True)
        if status:
            time.sleep(self._new_queue_wait_seconds)

    @check_pause
    def _refresh(self):
        """
        刷新doing种子过期时间，防止reset重新消费
        """
        if self.__DOING__:
            refresh_time = int(time.time())
            seeds = {k:-refresh_time - v / 1000 for k, v in self.__DOING__.items()}
            self._db.zadd(self._todo_key, item=seeds, xx=True)
        time.sleep(15)

    @check_pause
    def _delete(self):
        """
        删除队列种子，根据状态添加至成功或失败队列，移除doing字典种子索引
        """
        # seed_info = {"count": 0, "failed": [], "succeed": [], "common": []}

        seed_list = []
        status = self.__LAUNCHER_QUEUE__['done'].length < self._done_queue_max_size

        for _ in range(self._done_queue_max_size):
            seed = self.__LAUNCHER_QUEUE__['done'].pop()
            if not seed:
                break
            seed_list.append(seed.to_string)

        if seed_list:

            self._db.zrem(self._todo_key, *seed_list)
            self._remove_doing_seeds(seed_list)

        if status:
            time.sleep(self._done_queue_wait_seconds)

    def _polling(self):
        wait_scheduler_execute = True
        check_emtpy_times = 0
        while not self._stop.is_set():
            queue_not_empty_count = 0
            pooling_wait_seconds = 30

            for q in self.__LAUNCHER_QUEUE__.values():
                if q.length != 0:
                    queue_not_empty_count += 1
                    wait_scheduler_execute = False

            if queue_not_empty_count == 0:
                pooling_wait_seconds = 3
                if self._pause.is_set():
                    check_emtpy_times = 0
                    if not self._task_model and (
                            not wait_scheduler_execute or
                            int(time.time()) - self._app_time > self._before_scheduler_wait_seconds
                    ):
                        logger.info("Done! ready to close thread...")
                        self._stop.set()

                    elif self._db.zcount(self._todo_key, _min=0, _max="(1000"):
                        logger.info(f"Recovery {self.task} task run！")
                        self._pause.clear()
                        self._execute()
                    else:
                        logger.info("pause! waiting for resume...")
                elif check_emtpy_times > 2:
                    self.__DOING__ = {}
                    if not self._db.zcount(self._todo_key, _min="-inf", _max="(1000"):
                        self._pause.set()
                else:
                    logger.info(
                        "check whether the task is complete, "
                        f"reset times {3 - check_emtpy_times}"
                    )
                    check_emtpy_times += 1
            else:
                logger.info(LogTemplate.launcher_pro_polling.format(
                    task=self.task,
                    doing_len=len(self.__DOING__.keys()),
                    todo_len=self.__LAUNCHER_QUEUE__['todo'].length,
                    done_len=self.__LAUNCHER_QUEUE__['done'].length,
                    redis_seed_count=self._db.zcount(self._todo_key, "-inf", "+inf"),
                    redis_todo_len=self._db.zcount(self._todo_key, 0, "(1000"),
                    redis_doing_len=self._db.zcount(self._todo_key, "-inf", "(0"),
                    upload_len=self.__LAUNCHER_QUEUE__['upload'].length,
                ))

            time.sleep(pooling_wait_seconds)

        logger.info("Done! Ready to close thread...")

