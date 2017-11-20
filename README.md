# Buter
> 基于 `Docker`  的远程应用部署管理平台

![structure](docs/images/structure.png)

## 相关库

* [Flask](https://github.com/pallets/flask)
* [sqlalchemy](https://github.com/zzzeek/sqlalchemy)
* [flask-sqlalchemy](https://github.com/mitsuhiko/flask-sqlalchemy)
* [docker-py](https://github.com/docker/docker-py)

**打包**

* [pyInstaller](http://www.pyinstaller.org)

更多 `pyInstaller` 的说明详见[这里](https://pyinstaller.readthedocs.io/en/stable/usage.html)

执行 `package.py` 即可打包（默认打包成单个可执行文件存放到 `dist` 目录，`windows` 平台为 `buter.exe`，Linux/mac OS 为 `buter`）

完整的项目运行目录如下：

```text
|- static/              # 静态资源，buter-admin 项目打包后复制到此处
|- logs/                # 日志文件
|- buter.exe            # 主程序
|- setting.py           # 额外的配置文件，覆盖默认配置
```

## LOGS

### 0.0.1

- [ ] 环境检测（os、python、docker）
- [ ] Application 数据对象`CURD`
- [ ] 部署`Java`应用