import threading
import time
import traceback

from inspect import isgenerator
from typing import Union, Callable, Mapping

from cobweb.base import Queue, Seed, BaseItem, Request, Response, logger
from cobweb.constant import DealModel, LogTemplate
from cobweb.utils import download_log_info
from cobweb import setting


class Crawler(threading.Thread):

    def __init__(
            self,
            upload_queue: Queue,
            custom_func: Union[Mapping[str, Callable]],
            launcher_queue: Union[Mapping[str, Queue]],
    ):
        super().__init__()

        self.upload_queue = upload_queue
        for func_name, _callable in custom_func.items():
            if isinstance(_callable, Callable):
                self.__setattr__(func_name, _callable)

        self.launcher_queue = launcher_queue

        self.spider_thread_num = setting.SPIDER_THREAD_NUM
        self.max_retries = setting.SPIDER_MAX_RETRIES

    @staticmethod
    def request(seed: Seed) -> Union[Request, BaseItem]:
        stream = True if setting.DOWNLOAD_MODEL else False
        yield Request(seed.url, seed, stream=stream, timeout=5)

    @staticmethod
    def download(item: Request) -> Union[Seed, BaseItem, Response, str]:
        response = item.download()
        yield Response(item.seed, response, **item.to_dict)

    @staticmethod
    def parse(item: Response) -> BaseItem:
        pass

    def get_seed(self) -> Seed:
        return self.launcher_queue['todo'].pop()

    def distribute(self, item, seed):
        if isinstance(item, BaseItem):
            self.upload_queue.push(item)
        elif isinstance(item, Seed):
            self.launcher_queue['new'].push(item)
        elif isinstance(item, str) and item == DealModel.poll:
            self.launcher_queue['todo'].push(seed)
        elif isinstance(item, str) and item == DealModel.done:
            self.launcher_queue['done'].push(seed)
        elif isinstance(item, str) and item == DealModel.fail:
            seed.params.seed_status = DealModel.fail
            self.launcher_queue['done'].push(seed)
        else:
            raise TypeError("yield value type error!")

    def spider(self):
        while True:
            seed = self.get_seed()

            if not seed:
                continue

            elif seed.params.retry >= self.max_retries:
                seed.params.seed_status = DealModel.fail
                self.launcher_queue['done'].push(seed)
                continue

            seed_detail_log_info = download_log_info(seed.to_dict)

            try:
                request_iterators = self.request(seed)

                if not isgenerator(request_iterators):
                    raise TypeError("request function isn't a generator!")

                iterator_status = False

                for request_item in request_iterators:

                    iterator_status = True

                    if isinstance(request_item, Request):
                        iterator_status = False
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
                                    response=download_log_info(download_item.to_dict)
                                ))
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
                logger.info(LogTemplate.download_exception.format(
                    detail=seed_detail_log_info,
                    retry=seed.params.retry,
                    priority=seed.params.priority,
                    seed_version=seed.params.seed_version,
                    identifier=seed.identifier or "",
                    exception=''.join(traceback.format_exception(type(e), e, e.__traceback__))
                ))
                seed.params.retry += 1
                self.launcher_queue['todo'].push(seed)
            finally:
                time.sleep(0.1)

    def run(self):
        for index in range(self.spider_thread_num):
            threading.Thread(name=f"spider_{index}", target=self.spider).start()

