# 应用部署
> 应用部署分为`完整部署`、`迭代部署`两种模式

![app-deploy](images/app-deploy.png)


**如何判定合法性？**
> 用户上传的文件要求为`zip`格式的压缩文件

对于`完整部署`的应用，标准的目录结构如下（解压后）：

```text
|- image@version.tar
|- app.zip / app
|- run.txt
|- README.md
```

`tar`文件为`docker save/export` 得到的文件，用于执行 `docker load`命令

`zip`文件为应用相关文件，将被解压到应用根目录（`{程序目录}/apps/{app名称}`）

`run.txt` 保存的是`docker create`命令，命令中可以包含以下占位符（格式 `#变量名#`，如 `#name#` 将会被变量`name`替换），系统内置变量有：

* `app.name`    应用名称（仅包含字母跟数字）
* `app.path`    应用根目录
* `app.id`      应用 ID，如 1,2
