import time
import inspect
import threading
import importlib
from functools import wraps


from cobweb import setting
from cobweb.base import Seed, Queue, logger
from cobweb.utils.tools import dynamic_load_class


def check_pause(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        while not self._pause.is_set():
            try:
                func(self, *args, **kwargs)
            except Exception as e:
                logger.info(f"{func.__name__}: " + str(e))
            finally:
                time.sleep(0.1)

    return wrapper


class Launcher(threading.Thread):

    SEEDS = []

    __DOING__ = {}

    __CUSTOM_FUNC__ = {
        # "download": None,
        # "request": None,
        # "parse": None,
    }

    __LAUNCHER_QUEUE__ = {
        "new": Queue(),
        "todo": Queue(),
        "done": Queue(),
        "upload": Queue()
    }

    __LAUNCHER_FUNC__ = [
        "_reset",
        "_scheduler",
        "_insert",
        "_refresh",
        "_delete",
    ]

    def __init__(self, task, project, custom_setting=None, **kwargs):
        super().__init__()
        self.task = task
        self.project = project

        self._app_time = int(time.time())
        self._stop = threading.Event()  # 结束事件
        self._pause = threading.Event()  # 暂停事件

        _setting = dict()

        if custom_setting:
            if isinstance(custom_setting, dict):
                _setting = custom_setting
            else:
                if isinstance(custom_setting, str):
                    custom_setting = importlib.import_module(custom_setting)
                if not inspect.ismodule(custom_setting):
                    raise Exception
                for k, v in custom_setting.__dict__.items():
                    if not k.startswith("__") and not inspect.ismodule(v):
                        _setting[k] = v

        _setting.update(**kwargs)

        for k, v in _setting.items():
            setattr(setting, k.upper(), v)

        self._Crawler = dynamic_load_class(setting.CRAWLER)
        self._Pipeline = dynamic_load_class(setting.PIPELINE)

        self._before_scheduler_wait_seconds = setting.BEFORE_SCHEDULER_WAIT_SECONDS
        self._scheduler_wait_seconds = setting.SCHEDULER_WAIT_SECONDS
        self._todo_queue_full_wait_seconds = setting.TODO_QUEUE_FULL_WAIT_SECONDS
        self._new_queue_wait_seconds = setting.NEW_QUEUE_WAIT_SECONDS
        self._done_queue_wait_seconds = setting.DONE_QUEUE_WAIT_SECONDS
        self._upload_queue_wait_seconds = setting.UPLOAD_QUEUE_WAIT_SECONDS
        self._seed_reset_seconds = setting.SEED_RESET_SECONDS

        self._todo_queue_size = setting.TODO_QUEUE_SIZE
        self._new_queue_max_size = setting.NEW_QUEUE_MAX_SIZE
        self._done_queue_max_size = setting.DONE_QUEUE_MAX_SIZE
        self._upload_queue_max_size = setting.UPLOAD_QUEUE_MAX_SIZE

        self._spider_max_retries = setting.SPIDER_MAX_RETRIES
        self._spider_thread_num = setting.SPIDER_THREAD_NUM
        self._spider_time_sleep = setting.SPIDER_TIME_SLEEP
        self._spider_max_count = setting.SPIDER_MAX_COUNT
        self._time_window = setting.TIME_WINDOW
        self._speed_control = setting.SPEED_CONTROL

        self._done_model = setting.DONE_MODEL
        self._task_model = setting.TASK_MODEL

        self._filter_field = setting.FILTER_FIELD

    @property
    def request(self):
        """
        自定义request函数
        use case:
            from cobweb.base import Request, BaseItem
            @launcher.request
            def request(seed: Seed) -> Union[Request, BaseItem]:
                ...
                yield Request(seed.url, seed)
        """
        def decorator(func):
            self.__CUSTOM_FUNC__["request"] = func
        return decorator

    @property
    def download(self):
        """
        自定义download函数
        use case:
            from cobweb.base import Request, Response, Seed, BaseItem
            @launcher.download
            def download(item: Request) -> Union[Seed, BaseItem, Response, str]:
                ...
                yield Response(item.seed, response)
        """
        def decorator(func):
            self.__CUSTOM_FUNC__["download"] = func
        return decorator

    @property
    def parse(self):
        """
        自定义parse函数, xxxItem为自定义的存储数据类型
        use case:
            from cobweb.base import Request, Response
            @launcher.parse
            def parse(item: Response) -> BaseItem:
               ...
               yield xxxItem(seed, **kwargs)
        """
        def decorator(func):
            self.__CUSTOM_FUNC__["parse"] = func
        return decorator

    def start_seeds(self):
        seeds = [Seed(seed) for seed in self.SEEDS]
        self.__LAUNCHER_QUEUE__['todo'].push(seeds)
        return seeds

    def _remove_doing_seeds(self, seeds):
        for seed in seeds:
            self.__DOING__.pop(seed, None)
        # logger.info("remove %s seeds from __DOING__" % len(seeds))

    def _get_seed(self) -> Seed:
        return self.__LAUNCHER_QUEUE__["todo"].pop()

    def _set_seed(self, seed, **kwargs):
        self.__LAUNCHER_QUEUE__["todo"].push(seed, **kwargs)

    def _upload_data(self, data, **kwargs):
        self.__LAUNCHER_QUEUE__["upload"].push(data, **kwargs)

    def _add_seed(self, seed, **kwargs):
        self.__LAUNCHER_QUEUE__["new"].push(seed, **kwargs)

    def _delete_seed(self, seed, **kwargs):
        self.__LAUNCHER_QUEUE__["done"].push(seed, **kwargs)

    def _execute(self):
        for func_name in self.__LAUNCHER_FUNC__:
            threading.Thread(name=func_name, target=getattr(self, func_name)).start()
            time.sleep(1)

    def run(self):
        threading.Thread(target=self._execute_heartbeat).start()

        self.start_seeds()

        self._Crawler(
            task=self.task, project=self.project,
            stop=self._stop, pause=self._pause,
            # launcher_queue=self.__LAUNCHER_QUEUE__,
            get_seed=self._get_seed,
            set_seed=self._set_seed,
            add_seed=self._add_seed,
            delete_seed=self._delete_seed,
            upload_data=self._upload_data,
            custom_func=self.__CUSTOM_FUNC__,
            thread_num = self._spider_thread_num,
            max_retries = self._spider_max_retries,
            time_sleep=self._spider_time_sleep
        ).start()

        self._Pipeline(
            stop=self._stop, pause=self._pause,
            upload=self.__LAUNCHER_QUEUE__["upload"],
            done=self.__LAUNCHER_QUEUE__["done"],
            upload_size=self._upload_queue_max_size,
            wait_seconds=self._upload_queue_wait_seconds
        ).start()

        self._execute()
        self._polling()

    def _execute_heartbeat(self):
        pass

    def _reset(self):
        pass

    def _scheduler(self):
        pass

    def _insert(self):
        pass

    def _refresh(self):
        pass

    def _delete(self):
        pass

    def _polling(self):
        pass

