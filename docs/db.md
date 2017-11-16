# buter 数据实体

注：

1. 如无特殊说明，每个表都有自增ID：`id`

## Application
> 表名：app

字段名 | 类型 | 默认值 | 必填 | 备注 
---------|----------|---------|----------|---------
name|String||是|应用名称
version|String|||版本信息
remark|String|||应用描述
addDate|Date||是|录入日期


## Resource
> 表名：resource

`Resource`指的是上传到`buter`的文件（包括但不限于镜像文件、应用升级补丁等）