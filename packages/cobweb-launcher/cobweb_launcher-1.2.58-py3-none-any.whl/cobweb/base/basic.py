import json
import random
import time
import hashlib
import requests


class Params:

    def __init__(self, retry=None, priority=None, version=None, status=None):
        self.retry = retry or 0
        self.priority = priority or 300
        self.version = version or int(time.time())
        self.status = status


class Seed:
    __SEED_PARAMS__ = [
        "retry",
        "priority",
        "version",
        "status"
    ]

    def __init__(
            self,
            seed,
            sid=None,
            retry=None,
            priority=None,
            version=None,
            status=None,
            **kwargs
    ):
        if any(isinstance(seed, t) for t in (str, bytes)):
            try:
                item = json.loads(seed)
                self._init_seed(item)
            except json.JSONDecodeError:
                self.__setattr__("url", seed)
        elif isinstance(seed, dict):
            self._init_seed(seed)
        else:
            raise TypeError(Exception(
                f"seed type error, "
                f"must be str or dict! "
                f"seed: {seed}"
            ))

        seed_params = {
            "retry": retry,
            "priority": priority,
            "version": version,
            "status": status,
        }

        if kwargs:
            # for k, v in kwargs.items():
            #     if k in seed_params.keys():
            #         seed_params[k] = v
            #     else:
            #         self.__setattr__(k, v)
            self._init_seed(kwargs)
            seed_params.update({
                k: v for k, v in kwargs.items()
                if k in self.__SEED_PARAMS__
            })
        if sid or not getattr(self, "sid", None):
            self._init_id(sid)
        self.params = Params(**seed_params)

    def __getattr__(self, name):
        return None

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __getitem__(self, item):
        return getattr(self, item)

    def __str__(self):
        return json.dumps(self.__dict__, ensure_ascii=False)

    def __repr__(self):
        chars = [f"{k}={v}" for k, v in self.__dict__.items()]
        return f'{self.__class__.__name__}({", ".join(chars)})'

    def _init_seed(self, seed_info: dict):
        for k, v in seed_info.items():
            if k not in self.__SEED_PARAMS__:
                self.__setattr__(k, v)

    def _init_id(self, sid):
        if not sid:
            sid = hashlib.md5(self.to_string.encode()).hexdigest()
        self.__setattr__("sid", sid)

    @property
    def to_dict(self) -> dict:
        seed = self.__dict__.copy()
        if seed.get("params"):
            del seed["params"]
        return seed

    @property
    def to_string(self) -> str:
        return json.dumps(
            self.to_dict,
            ensure_ascii=False,
            separators=(",", ":")
        )

    @property
    def seed(self):
        return self.to_string


class Request:
    __SEED_PARAMS__ = [
        "retry",
        "priority",
        "version",
        "status"
    ]

    __REQUEST_ATTRS__ = {
        "params",
        "headers",
        "cookies",
        "data",
        "json",
        "files",
        "auth",
        "timeout",
        "proxies",
        "hooks",
        "stream",
        "verify",
        "cert",
        "allow_redirects",
    }

    def __init__(
            self,
            # url,
            seed,
            random_ua=True,
            check_status_code=True,
            retry=None,
            priority=None,
            version=None,
            status=None,
            **kwargs
    ):
        # self.url = url
        self.check_status_code = check_status_code
        self.request_setting = {}

        seed_params = {
            "retry": retry,
            "priority": priority,
            "version": version,
            "status": status,
        }

        if isinstance(seed, Seed):
            kwargs.update(**seed.to_dict)
        elif isinstance(seed, str):
            kwargs.update(**json.loads(seed))
        elif isinstance(seed, dict):
            kwargs.update(**seed)

        for k, v in kwargs.items():
            if k in self.__class__.__REQUEST_ATTRS__:
                self.request_setting[k] = v
                continue
            elif k in self.__SEED_PARAMS__:
                seed_params[k] = v
            self.__setattr__(k, v)

        if not getattr(self, "method", None):
            self.method = "POST" if self.request_setting.get("data") or self.request_setting.get("json") else "GET"

        if random_ua:
            self._build_header()

        self.params = Params(**seed_params)
        # self.seed = self.to_string

    @property
    def _random_ua(self) -> str:
        v1 = random.randint(4, 15)
        v2 = random.randint(3, 11)
        v3 = random.randint(1, 16)
        v4 = random.randint(533, 605)
        v5 = random.randint(1000, 6000)
        v6 = random.randint(10, 80)
        user_agent = (f"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_{v1}_{v2}) AppleWebKit/{v4}.{v3} "
                      f"(KHTML, like Gecko) Chrome/105.0.0.0 Safari/{v4}.{v3} Edg/105.0.{v5}.{v6}")
        return user_agent

    def _build_header(self) -> dict:
        if not self.request_setting.get("headers"):
            self.request_setting["headers"] = {"accept": "*/*", "user-agent": self._random_ua}
        elif "user-agent" not in [key.lower() for key in self.request_setting["headers"].keys()]:
            self.request_setting["headers"]["user-agent"] = self._random_ua

    def download(self) -> requests.Response:
        response = requests.request(self.method, self.url, **self.request_setting)
        if self.check_status_code:
            response.raise_for_status()
        return response

    def __getattr__(self, name):
        return None

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __getitem__(self, item):
        return getattr(self, item)

    @property
    def to_dict(self):
        _dict = self.__dict__.copy()
        # _dict.pop('seed')
        _dict.pop('params')
        _dict.pop('check_status_code')
        # _dict.pop('request_setting')
        return _dict

    @property
    def to_string(self) -> str:
        return json.dumps(
            self.to_dict,
            ensure_ascii=False,
            separators=(",", ":")
        )

    @property
    def seed(self):
        return self.to_string


class Response:

    def __init__(
            self,
            seed,
            response,
            retry=None,
            priority=None,
            version=None,
            status=None,
            **kwargs
    ):
        self.seed = seed
        self.response = response
        seed_params = {
            "retry": retry,
            "priority": priority,
            "version": version,
            "status": status,
        }
        for k, v in kwargs.items():
            if k in seed_params.keys():
                seed_params[k] = v
            else:
                self.__setattr__(k, v)
        self.params = Params(**seed_params)

    @property
    def to_dict(self):
        _dict = self.__dict__.copy()
        _dict.pop('seed')
        _dict.pop('response')
        _dict.pop('method')
        _dict.pop('params')
        _dict.pop('request_setting')
        return _dict

    @property
    def to_string(self) -> str:
        return json.dumps(
            self.to_dict,
            ensure_ascii=False,
            separators=(",", ":")
        )

    def __getattr__(self, name):
        return None

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __getitem__(self, item):
        return getattr(self, item)
