# Buter App

## Logger
> 日志保存到 `./logs/buter.log` 文件中，默认每天产生一个文件

默认日志相关的配置如下：

```python
LOG_LEVEL = logging.DEBUG
LOG_FORMAT = '%(asctime)s %(levelname)s %(process)d - %(filename)s (%(lineno)d) : %(message)s'
LOG_FILE = "./logs/buter.log"
# 默认保留15天内的日志
LOG_BACKUP = 15
LOG_ENCODING = 'utf-8'
```

## Models
> 此处定义了数据相关的实体类

### Application
> 应用程序类，表名：app

字段名 | 类型 | 默认值 | 必填 | 备注 
---------|----------|---------|----------|---------
id|Long| |是|自增ID
name|String| |是|应用名称
remark|String| | |应用描述
addDate|Date| | |录入时间

