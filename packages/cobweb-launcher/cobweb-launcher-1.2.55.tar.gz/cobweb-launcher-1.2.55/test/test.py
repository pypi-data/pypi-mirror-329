import os


os.environ["SPIDER_NUM"] = "1"
os.environ["REDIS_HOST"] = "r-j6cc5zw8m3pqom4chmpd.redis.rds.aliyuncs.com"
os.environ["REDIS_PASSWORD"] = "SpiderLinux666"
os.environ["REDIS_PORT"] = "6379"
os.environ["REDIS_DB"] = "0"
os.environ["SCHEDULER_QUEUE_LENGTH"] = "100"
os.environ["STORER_QUEUE_LENGTH"] = "10"
os.environ["LOGSTORE"] = "download_meta"
os.environ["LOGHUB_ACCESS_KEY"] = "LTAI5tH2FLYsBkxcbiLdoYZT"
os.environ["LOGHUB_ACCESS_SECRET"] = "4oD1NVvYfaWiqxkmGx6c2xtpPWEq17"
os.environ["BUCKET"] = "databee-video"
os.environ["ENDPOINT"] = "http://oss-cn-hangzhou.aliyuncs.com"
os.environ["OSS_ACCESS_KEY"] = "LTAI5tH2FLYsBkxcbiLdoYZT"
os.environ["OSS_ACCESS_SECRET"] = "4oD1NVvYfaWiqxkmGx6c2xtpPWEq17"
os.environ["CHUNK_SIZE"] = "1048576"
os.environ["MIN_SIZE"] = "1024"


from cobweb import LauncherPro

app = LauncherPro("test", "test", SPIDER_THREAD_NUM=1)


if __name__ == '__main__':
    print()
    app.start()
