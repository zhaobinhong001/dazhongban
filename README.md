# 开发环境说明

## 系统依赖
1. 任意可以安装 docker 的 linux 发行版 (centos，debian等)，推荐 debian 8.6.x
2. docker >= 1.12.0
3. docker-compose >= 1.9.0


## 部署前的配置
1. 配置 volumes(磁盘卷) ，已经配置好了，除特殊情况不需要修改
2. 配置暴露端口 ports 在 docker-compose.yml 选项，已经配置好了，除特殊情况不需要修改

全局的配置在代码根目录下的 .env 文件，需要配置的选项如下：

> _**需要注意的是, 配置 ”=“ 前后不能有空格**_

```shell
# 项目默认的用户名和密码
DJANGO_ADMIN_USER=bankeys
DJANGO_ADMIN_PASS=secret

# 融云相关配置
RONGCLOUD_APPKEY=ik1qhw09ifflp
RONGCLOUD_SECRET=kfx3v7mffJeaJt

# jpush 相关配置
JPUSH_APPKEY=496daf24808978b12e4e0505
JPUSH_SECRET=6e449bd8dd4dd2e5dff00c02

# 四要素认证相关配置, 如果更改可以联系开发二部
IDDENTITY_APPKEY=69tx91g3kpzlqkndszzofj38fr
IDDENTITY_GATEWAY=https://10.7.7.71:3002/api/register

# 验签微服务, 无特殊情况不需要修改
VERIFY_GATEWAY=http://verifysign:8080

# 验证银行 PIN 码微服务, 无特殊情况不需要修改
BANK_CARD=http://bankcard:5000/bank
```

## 部署环境步骤
1. 确保系统依赖和配置以及完成；
2. 在项目的根目录下执行: `docker-compose up --build` (第一次执行可以不加 `--build`). 如果没有提示报错在表示成功启动。
3. 启动后的数据初始化操作，具体操作如下：

```shell
# 第一次执行可以不加 `--build`
docker-compose up --build 
```

## 数据备份与维护
待续


