# 网易云音乐ACG歌曲评论爬虫

## 持久化启动
1、打开Mongodb服务器，如有权限验证请修改`MongoUtils.py`配置项

2、以持久化启动爬虫
```bash
scrapy crawl music_spider -s JOBDIR=crawls/spider-1
```

3、查看MongoDB数据