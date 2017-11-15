# 附录

## 遇到问题

### jsonify(Entity 对象) 报错：is not JSON serializable

[flask-jsonify-a-list-of-objects](https://stackoverflow.com/questions/21411497/flask-jsonify-a-list-of-objects)

[how-to-serialize-sqlalchemy-result-to-json](https://stackoverflow.com/questions/5022066/how-to-serialize-sqlalchemy-result-to-json)

### windows 下使用`logging`模块的 `TimedRotatingFileHandler` 出现`PermissionError`

久经排查，发现原来是 `DEBUG` 模式下启动了两个进程，导致 log 文件 `rename` 失败，现解决方案是 `DEBUG` 模式下不写日志到文件

## python参考资源

### 博客

[断网环境下利用pip安装Python离线安装包](https://www.cnblogs.com/michael-xiang/p/5690746.html)

### 开源项目

[fsblog：基于Flask的个人开源博客](https://gitee.com/megadata/fsblog)
