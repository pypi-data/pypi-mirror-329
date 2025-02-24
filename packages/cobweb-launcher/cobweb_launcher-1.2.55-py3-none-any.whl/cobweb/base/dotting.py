import os
import json
from aliyun.log import LogClient, LogItem, PutLogsRequest


class LoghubDot:

    def __init__(self):
        endpoint = os.getenv("DOTTING_ENDPOINT", "")
        accessKeyId = os.getenv("DOTTING_ACCESS_KEY", "")
        accessKey = os.getenv("DOTTING_SECRET_KEY", "")
        self.client = LogClient(endpoint=endpoint, accessKeyId=accessKeyId, accessKey=accessKey) \
            if endpoint and accessKeyId and accessKey else None

    def build(self, topic, **kwargs):
        if self.client:
            temp = {}
            log_items = []
            log_item = LogItem()
            for key, value in kwargs.items():
                if not isinstance(value, str):
                    temp[key] = json.dumps(value, ensure_ascii=False)
                else:
                    temp[key] = value
            contents = sorted(temp.items())
            log_item.set_contents(contents)
            log_items.append(log_item)
            request = PutLogsRequest(
                project="databee-download-log",
                logstore="download-logging",
                topic=topic,
                logitems=log_items,
                compress=True
            )
            self.client.put_logs(request=request)
