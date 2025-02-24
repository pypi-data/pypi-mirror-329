import json
import os
import threading
import time
import traceback
from inspect import isgenerator
from typing import Union, Callable, Mapping
from urllib.parse import urlparse

from requests import Response as Res

from cobweb.constant import DealModel, LogTemplate
from cobweb.base import (
    Seed,
    BaseItem, 
    Request, 
    Response, 
    ConsoleItem,
    logger
)
from cobweb.utils import LoghubDot


class Crawler(threading.Thread):

    def __init__(
            self,
            task: str,
            project: str,
            stop: threading.Event,
            pause: threading.Event,
            # launcher_queue: Union[Mapping[str, Queue]],
            get_seed: Callable,
            set_seed: Callable,
            add_seed: Callable,
            delete_seed: Callable,
            upload_data: Callable,
            custom_func: Union[Mapping[str, Callable]],
            thread_num: int,
            max_retries: int,
            time_sleep: int,
    ):
        super().__init__()
        self.task = task
        self.project = project
        self._stop = stop
        self._pause = pause
        self._get_seed = get_seed
        self._set_seed = set_seed
        self._add_seed = add_seed
        self._delete_seed = delete_seed
        self._upload_data = upload_data

        for func_name, _callable in custom_func.items():
            if isinstance(_callable, Callable):
                self.__setattr__(func_name, _callable)

        self.thread_num = thread_num
        self.time_sleep = time_sleep
        self.max_retries = max_retries

        self.loghub_dot = LoghubDot()

    @staticmethod
    def request(seed: Seed) -> Union[Request, BaseItem]:
        yield Request(seed.url, seed, timeout=5)

    @staticmethod
    def download(item: Request) -> Union[Seed, BaseItem, Response, str]:
        response = item.download()
        yield Response(item.seed, response, **item.to_dict)

    @staticmethod
    def parse(item: Response) -> BaseItem:
        upload_item = item.to_dict
        upload_item["text"] = item.response.text
        yield ConsoleItem(item.seed, data=json.dumps(upload_item, ensure_ascii=False))

    # def get_seed(self) -> Seed:
    #     return self._todo.pop()

    def distribute(self, item, seed):
        if isinstance(item, BaseItem):
            self._upload_data(item)
        elif isinstance(item, Seed):
            self._add_seed(item)
        elif isinstance(item, str) and item == DealModel.poll:
            self._set_seed(seed)
        elif isinstance(item, str) and item == DealModel.done:
            self._delete_seed(seed)
        elif isinstance(item, str) and item == DealModel.fail:
            seed.params.seed_status = DealModel.fail
            self._delete_seed(seed)
        else:
            raise TypeError("yield value type error!")

    def spider(self):
        while not self._stop.is_set():

            seed = self._get_seed()

            if not seed:
                time.sleep(1)
                continue

            elif seed.params.retry > self.max_retries:
                seed.params.seed_status = DealModel.fail
                self._delete_seed(seed)
                continue

            seed_detail_log_info = LogTemplate.log_info(seed.to_dict)

            try:
                request_iterators = self.request(seed)

                if not isgenerator(request_iterators):
                    raise TypeError("request function isn't a generator!")

                iterator_status = False

                for request_item in request_iterators:

                    iterator_status = True

                    if isinstance(request_item, Request):
                        iterator_status = False
                        start_time = time.time()
                        download_iterators = self.download(request_item)
                        if not isgenerator(download_iterators):
                            raise TypeError("download function isn't a generator")

                        for download_item in download_iterators:
                            iterator_status = True
                            if isinstance(download_item, Response):
                                iterator_status = False
                                logger.info(LogTemplate.download_info.format(
                                    detail=seed_detail_log_info,
                                    retry=seed.params.retry,
                                    priority=seed.params.priority,
                                    seed_version=seed.params.seed_version,
                                    identifier=seed.identifier or "",
                                    status=download_item.response,
                                    response=LogTemplate.log_info(download_item.to_dict)
                                ))
                                if isinstance(download_item.response, Res):
                                    end_time = time.time()
                                    self.loghub_dot.build(
                                        topic=urlparse(download_item.response.request.url).netloc,
                                        data_size=int(download_item.response.headers.get("content-length", 0)),
                                        cost_time=end_time - start_time, status = 200,
                                        url=download_item.response.url,
                                        proxy_type=seed.params.proxy_type,
                                        proxy=seed.params.proxy,
                                        project=self.project, task=self.task,
                                    )
                                parse_iterators = self.parse(download_item)
                                if not isgenerator(parse_iterators):
                                    raise TypeError("parse function isn't a generator")
                                for parse_item in parse_iterators:
                                    iterator_status = True
                                    if isinstance(parse_item, Response):
                                        raise TypeError("upload_item can't be a Response instance")
                                    self.distribute(parse_item, seed)
                            else:
                                self.distribute(download_item, seed)
                    else:
                        self.distribute(request_item, seed)

                if not iterator_status:
                    raise ValueError("request/download/parse function yield value error!")
            except Exception as e:
                exception_msg = ''.join(traceback.format_exception(type(e), e, e.__traceback__))
                url = seed.url
                status = e.__class__.__name__
                if getattr(e, "response", None) and isinstance(e.response, Res):
                    url = e.response.request.url
                    status = e.response.status_code
                self.loghub_dot.build(
                    topic=urlparse(url).netloc,
                    data_size=-1, cost_time=-1,
                    status=status, url=url,
                    proxy_type=seed.params.proxy_type,
                    proxy=seed.params.proxy,
                    project=self.project,
                    task=self.task,
                    msg=exception_msg,
                )
                logger.info(LogTemplate.download_exception.format(
                    detail=seed_detail_log_info,
                    retry=seed.params.retry,
                    priority=seed.params.priority,
                    seed_version=seed.params.seed_version,
                    identifier=seed.identifier or "",
                    exception=''.join(traceback.format_exception(type(e), e, e.__traceback__))
                ))
                seed.params.retry += 1
                self._set_seed(seed)
                # time.sleep(self.time_sleep * seed.params.retry)
            # except Exception as e:
            #     logger.info(LogTemplate.download_exception.format(
            #         detail=seed_detail_log_info,
            #         retry=seed.params.retry,
            #         priority=seed.params.priority,
            #         seed_version=seed.params.seed_version,
            #         identifier=seed.identifier or "",
            #         exception=''.join(traceback.format_exception(type(e), e, e.__traceback__))
            #     ))
            #     seed.params.retry += 1
            #     # self._todo.push(seed)
            #     self._set_seed(seed)
            #     # time.sleep(self.time_sleep * seed.params.retry)
            finally:
                time.sleep(0.1)
        logger.info("spider thread close")

    def run(self):
        threading.Thread(name="loghub_dot", target=self.loghub_dot.build_run).start()
        for index in range(self.thread_num):
            threading.Thread(name=f"spider_{index}", target=self.spider).start()

