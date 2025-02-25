import threading
import time

# from cobweb.base import Seed
from cobweb.db import ApiDB


class ApiScheduler:

    def __init__(self, task, project, scheduler_wait_seconds=30):
        self._todo_key = "{%s:%s}:todo" % (project, task)
        self._download_key = "{%s:%s}:download" % (project, task)
        self._heartbeat_key = "heartbeat:%s_%s" % (project, task)
        self._speed_control_key = "speed_control:%s_%s" % (project, task)
        self._reset_lock_key = "lock:reset:%s_%s" % (project, task)
        self._db = ApiDB()

        self.scheduler_wait_seconds = scheduler_wait_seconds
        self.working = threading.Event()

    @property
    def heartbeat(self):
        return self._db.exists(self._heartbeat_key)

    def set_heartbeat(self):
        return self._db.setex(self._heartbeat_key, 5)

    def schedule(self, key, count):
        if not self._db.zcount(key, 0, "(1000"):
            time.sleep(self.scheduler_wait_seconds)
        else:
            source = int(time.time())
            members = self._db.members(key, source, count=count, _min=0, _max="(1000")
            for member, priority in members:
                # seed = Seed(member, priority=priority)
                yield member, priority

    def insert(self, key, items):
        if items:
            self._db.zadd(key, items, nx=True)

    def reset(self, keys, reset_time=30):
        if self._db.lock(self._reset_lock_key, t=120):

            if isinstance(keys, str):
                keys = [keys]

            _min = reset_time - int(time.time()) if self.heartbeat else "-inf"

            for key in keys:
                if self._db.exists(key):
                    self._db.members(key, 0, _min=_min, _max="(0")

            if not self.heartbeat:
                self.working.set()
                time.sleep(10)

            self._db.delete(self._reset_lock_key)

    def refresh(self, key, items: dict[str, int]):
        refresh_time = int(time.time())
        its = {k: -refresh_time - v / 1000 for k, v in items.items()}
        if its:
            self._db.zadd(key, item=its, xx=True)

    def delete(self, key, values):
        if values:
            self._db.zrem(key, *values)




