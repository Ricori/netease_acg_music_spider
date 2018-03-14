# 网易云音乐ACG歌曲评论爬虫

## 框架安装
```bash
pip install Scrapy
```
## 配置文件
`config.py`: 设置爬取页数与已经爬取页数，以实现分次爬取

## 持久化启动
1、启动MongoDB，如有非本地服务器或者有权限验证请修改`MongoUtils.py`配置项

2、以持久化启动爬虫
```bash
scrapy crawl music_spider -s JOBDIR=crawls/spider-1
```

3、查看MongoDB数据

## 暂停，恢复爬虫
暂停：
持久化启动可以在任何时候在安全地停止爬虫(按Ctrl-C或者发送一个信号)

恢复启动：
```bash
scrapy crawl music_spider -s JOBDIR=crawls/spider-1
```