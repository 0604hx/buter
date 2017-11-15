# Main
> 主模块接口

## heartbeat

心跳包测试，参数： `time`，返回值与参数一致

示例： `heartbeat/130000000` 则返回 `130000000`

## info

获取当前平台运行时信息（包括`操作系统`、`Docker`版本、`Python` 版本等）

返回格式如下：

```json
{
  "docker": {
    "version": "17.10.0-ce"
  }, 
  "python": {
    "compiler": "MSC v.1900 64 bit (AMD64)", 
    "version": "3.6.2"
  }, 
  "system": {
    "64Bit": true, 
    "cpu": "Intel64 Family 6 Model 60 Stepping 3, GenuineIntel", 
    "machine": "AMD64", 
    "platform": "win32", 
    "system": "Windows", 
    "version": "10.0.15063"
  }
}
```

