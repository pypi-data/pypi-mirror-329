import os
from typing import Union
from cobweb import setting
from cobweb.utils import OssUtil
from cobweb.crawlers import Crawler
from cobweb.base import Seed, BaseItem, Request, Response
from cobweb.exceptions import OssDBPutPartError, OssDBMergeError


oss_util = OssUtil(is_path_style=bool(int(os.getenv("PRIVATE_LINK", 0))))


class FileCrawlerAir(Crawler):

    @staticmethod
    def download(item: Request) -> Union[Seed, BaseItem, Response, str]:
        seed_dict = item.seed.to_dict
        seed_dict["bucket_name"] = oss_util.bucket
        try:
            seed_dict["oss_path"] = key = item.seed.oss_path or getattr(item, "oss_path")

            if oss_util.exists(key):
                seed_dict["data_size"] = oss_util.head(key).content_length
                yield Response(item.seed, "exists", **seed_dict)

            else:
                seed_dict.setdefault("end", "")
                seed_dict.setdefault("start", 0)

                if seed_dict["end"] or seed_dict["start"]:
                    start, end = seed_dict["start"], seed_dict["end"]
                    item.request_setting["headers"]['Range'] = f'bytes={start}-{end}'

                if not item.seed.identifier:
                    content = b""
                    chunk_size = oss_util.chunk_size
                    min_upload_size = oss_util.min_upload_size
                    seed_dict.setdefault("position", 1)

                    response = item.download()

                    content_type = response.headers.get("content-type", "").split(";")[0]
                    seed_dict["data_size"] = content_length = int(response.headers.get("content-length", 0))

                    if content_type and content_type in setting.FILE_FILTER_CONTENT_TYPE:
                        """过滤响应文件类型"""
                        response.close()
                        seed_dict["filter"] = True
                        seed_dict["msg"] = f"response content type is {content_type}"
                        yield Response(item.seed, response, **seed_dict)

                    elif seed_dict['position'] == 1 and min_upload_size >= content_length > 0:
                        """过小文件标识返回"""
                        response.close()
                        seed_dict["filter"] = True
                        seed_dict["msg"] = "file size is too small"
                        yield Response(item.seed, response, **seed_dict)

                    elif seed_dict['position'] == 1 and chunk_size > content_length > min_upload_size:
                        """小文件直接下载"""
                        for part_data in response.iter_content(chunk_size):
                            content += part_data
                        response.close()
                        oss_util.put(key, content)
                        yield Response(item.seed, response, **seed_dict)

                    else:
                        """中大文件同步分片下载"""
                        seed_dict.setdefault("upload_id", oss_util.init_part(key).upload_id)

                        for part_data in response.iter_content(chunk_size):
                            content += part_data
                            if len(content) >= chunk_size:
                                upload_data = content[:chunk_size]
                                content = content[chunk_size:]
                                oss_util.put_part(key, seed_dict["upload_id"], seed_dict['position'], content)
                                seed_dict['start'] += len(upload_data)
                                seed_dict['position'] += 1

                        response.close()

                        if content:
                            oss_util.put_part(key, seed_dict["upload_id"], seed_dict['position'], content)
                        oss_util.merge(key, seed_dict["upload_id"])
                        seed_dict["data_size"] = oss_util.head(key).content_length
                        yield Response(item.seed, response, **seed_dict)

                elif item.seed.identifier == "merge":
                    oss_util.merge(key, seed_dict["upload_id"])
                    seed_dict["data_size"] = oss_util.head(key).content_length
                    yield Response(item.seed, "merge", **seed_dict)

        except OssDBPutPartError:
            yield Seed(seed_dict)
        except OssDBMergeError:
            yield Seed(seed_dict, identifier="merge")


