# docker sdk 实践（windows、ubuntu、macOS）
> 这里介绍了如何在python中使用 `docker api`，这里是用的是[docker-py](http://docker-py.readthedocs.io)

此处将分别介绍`windows`、`linux（Ubuntu）`、`macOS`下`docker SDK`的使用实践（代码使用`python`，其他语言可以参考[官方文档](https://docs.docker.com/develop/sdk)）

**注**

1. 以下内容仅为个人理解，若有误望不吝指正

## windows
> 实践系统：windows 10 64bit

### 准备工作

`docker`针对`windows 10`推出了[docker-windows](https://www.docker.com/docker-windows),但需要开启`Hyer-V`功能，会导致`VMware Workstation`无法正常工作，故此处使用的是[docker-toolbox](https://www.docker.com/products/docker-toolbox)。

请按照官方文档安装`docker-toolbox`后，启动`docker QuickStart Terminal`即可看到以下输出：

```shell


                        ##         .
                  ## ## ##        ==
               ## ## ## ## ##    ===
           /"""""""""""""""""\___/ ===
      ~~~ {~~ ~~~~ ~~~ ~~~~ ~~~ ~ /  ===- ~~~
           \______ o           __/
             \    \         __/
              \____\_______/

docker is configured to use the default machine with IP 192.168.99.100
For help getting started, check out the docs at https://docs.docker.com

Start interactive shell
```

此时可以在当前终端界面执行`docker`操作（如 docker ps、docker iamges 等）

注意这些命令只限于当前终端，另开 `cmd` 终端的话由于无法连接到 `docker server` 而失败，相关提示如下：

```shell
> docker version
Client:
 Version:      17.10.0-ce
 API version:  1.33
 Go version:   go1.8.3
 Git commit:   f4ffd25
 Built:        Tue Oct 17 19:00:02 2017
 OS/Arch:      windows/amd64
error during connect: Get http://%2F%2F.%2Fpipe%2Fdocker_engine/v1.33/version: open //./pipe/docker_engine: The system cannot find the file specified. In the default daemon configuration on Windows, the docker client must be run elevated to connect. This error may also indicate that the docker daemon is not running.
```

这是由于`docker server`是运行在虚拟机中（ip=192.168.99.100），所以如果想在我们自己的程序中使用`docker api`，需要使用`docker remote api`

首先找到 docker server 的 ip 跟端口，使用 `docker-machine ls` 命令即可查看：

```shell
λ docker-machine ls
NAME      ACTIVE   DRIVER       STATE     URL                         SWARM   DOCKER        ERRORS
default   -        virtualbox   Running   tcp://192.168.99.100:2376           v17.10.0-ce
```

可以看到 URL 为`tcp://192.168.99.100:2376`

```shell
λ docker -H tcp://192.168.99.100:2376 ps
Get http://192.168.99.100:2376/v1.33/containers/json: malformed HTTP response "\x15\x03\x01\x00\x02\x02".
* Are you trying to connect to a TLS-enabled daemon without TLS?
```

通过上面命令，可以看到想要连接到 docker server 需要使用`TLS`

在 cmd 终端，设置以下环境变量即可成功链接：

```shell
set DOCKER_HOST=tcp://192.168.99.100:2376
set DOCKER_CERT_PATH=C:/Users/Administrator/.docker/machine/certs
set DOCKER_TLS_VERIFY=1

docker images
# 此时能得到正常的结果
```

其中`DOCKER_CERT_PATH`可以通过 `docker-machine config` 命令来查看


### 在程序中操作 Docker

现在我们可以开始在程序中操作`docker`了，假设已经安装了 python docker library（若没安装则使用`pip install docker`进行安装）

```python
import docker

# 定义配置
'''
Docker 配置，根据实际情况填写
'''
DOCKER_HOST = "tcp://192.168.99.100:2376"
DOCKER_CERT_PATH = "C:\\Users\\Administrator\\.docker\\machine\\certs"
DOCKER_TLS_VERIFY = "1"


# test_docker.py
#
# 这里使用两种方式链接 docker server
#
# 方式一：通过修改临时环境变量
if DOCKER_HOST is not None:
    os.environ['DOCKER_HOST'] = DOCKER_HOST
if DOCKER_CERT_PATH is not None:
    os.environ['DOCKER_CERT_PATH'] = DOCKER_CERT_PATH
if DOCKER_TLS_VERIFY is not None:
    os.environ['DOCKER_TLS_VERIFY'] = DOCKER_TLS_VERIFY

client = docker.from_env()

# 方式二：使用 TLSConfig
# 配置 TLSConfig，详见：http://docker-py.readthedocs.io/en/stable/tls.html#docker.tls.TLSConfig
tls_config = docker.tls.TLSConfig(
    ca_cert=DOCKER_CERT_PATH+"/ca.pem",
    client_cert=(
        DOCKER_CERT_PATH+'/cert.pem', 
        DOCKER_CERT_PATH+'/key.pem'
    ),
    verify=True
)
client = docker.DockerClient(
    base_url=DOCKER_HOST, 
    tls=tls_config
)


#测试链接是否成功，输出 image 列表
client.images.list()
# [
#   <Image: 'amancevice/superset:latest'>, 
#   <Image: 'mysql/mysql-cluster:latest'>
# ]
```

## Linux
> 实践系统：Ubuntu 16.04

默认情况下 `docker` 使用`unix:///var/run/docker.sock` 来进行 Unix socket 通信，如果 `python` 运行在本地则可以直接链接：

```python
import docker

client = docker.from_env()

#输出 image 列表
client.images.list()
# [
#   <Image: 'amancevice/superset:latest'>, 
#   <Image: 'mysql/mysql-cluster:latest'>
# ]
```

## maxOS
> 实践系统：Mac OS X 10.11.6

启动`docker`程序后使用跟 `Linux` 同样的代码即可