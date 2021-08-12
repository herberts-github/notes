[TOC]

# Nginx

Web 网站功能由编程语言实现，例如Java、PHP等，专注于网站功能的实现

资源映射与连接处理则由服务器软件，例如Apache、Nginx、Tomcat等

Nginx：HTTP 和反向代理服务器，同时也是邮件代理和通用 TCP/UDP 代理服务器

具有：模块化设计、可扩展、低内存消耗、支持热部署等特性

含有一个主进程和若干工作进程

- 主进程：用于读取和评估配置并维护工作进程
- 工作进程：对请求进行实际处理

基于事件的模型和依赖于操作系统的机制，有效地在工作进程之间分发请求

## 信号

信号（signal）：控制 Nginx 工作状态的模块

```shell
nginx -s signal
```

- stop：快速关机
- quit：正常关机，**在处理完当前请求后再停止工作进程**
- reload：重新加载配置文件，**当配置被修改或添加新的配置时，需要重新启动 Nginx 或重载配置**
- reopen：重新打开日志文件

> 当主进程收到配置重载信号，将检查新配置文件的语法有效性，并尝试应用其中的配置
>
> **成功**：主进程将启动新的工作并向旧工作进程发送关闭请求
>
> **失败**：主进程回滚更改，并继续使用旧配置，旧工作进程在接收关闭请求后停止接受新连接，并为当前请求提供服务
>
> Nginx信号官方文档：http://nginx.org/en/docs/control.html

## 配置文件

模块由配置文件中特定指令控制，配置文件决定了 Nginx 以及模块的工作方式

分为

- 主配置文件：nginx.conf，默认存放 `/etc/nginx`
- 辅助配置文件：以 .conf 作为文件后缀，并默认存放 `/etc/nginx/conf.d`
- Nginx 允许同时存放多个辅助配置文件

**Nginx 指令**

- **简单指令**：由指令名称和参数组成，以空格作为分隔符，分号结尾
    ```shell
    error_page 404 /404.html;
    ```
- **块指令**：与简单指令相同结构，以花括号包围的一组附加指令结束
    ```shell
    location /404.html {
        root /home/ubuntu/www/error_page;
    }
    ```

如果块指令内包含其他指令，则该块指令称为 **上下文**

常见上下文：events、http、server、location

> 注意：上下文包含 隐藏的 main 上下文，并非实际存在，类似于层级的根目录，即所有指令的最外层都是 main
>
> main 上下文作为其他其他上下文的参考对象，例如 events 和 http
>
> http >> server >> location

```shell
http{
    server {
        location / {
            root /www/index index.html;
        }
        location /images/ {
            # ...
        }
    }
}
```

配置文件的注释符为 `#`，默认监听 80 端口，当在本地访问 `http://localhost` 时，服务器根据配置文件设定的资源路径寻找资源，并将符合条件的资源发送给客户端，不存在则发送 404 错误

默认赋值配置文件 `default.conf`，存放在 `/etc/nginx/conf.d` 目录中（Ubuntu： `/etc/nginx/site-available`），里面包含若干 server 块指令示例

```shell
# 查看文件内容
sudo cat /etc/nginx/site-available/default
```

### Nginx 模块与指令

Nginx 文档 Modules reference 查看，常用模块 [ngx_http_rewrite_module](http://nginx.org/en/docs/http/ngx_http_rewrite_module.html)

ngx_http_rewrite_module 模块主要作用：**重定向**，通过正则表达式或判断语句更改请求的 URI

主要指令：if、set、break、return 和 rewrite

**if 指令语法语境**：

| 语法 | if(condition){...} |
| --- | --- |
|默认 | - |
|语境 | server, location |

```nginx configuration
if 条件 {
    ...
}
```

**if 指令没有默认值**，使用范围限制在 `server` 和 `location` 块内，条件情况：

- 变量名称：如果变量值是空字符串或0，条件布尔值为 False
- = 或 !=：比较变量和字符串
- ~ 或 ~*：将变量与正则表达式匹配，区分大小写，如果正则表达式包含 `{}` 或 `;` ，应使用单引号或双引号括起
- -f 或 !-f：检查文件是否存在
- -d 或 !-d：检查目录是否存在
- -e 或 !-e：检查文件、目录或符号链接是否存在
- -x 或 !-x：检查可执行文件

```nginx configuration
# 当请求头 User-Agent 头域的值包含 MSIE 字符串，则重定向到指定 URI
if ($http_user_agent - MSIE){
    rewrite ^(.*)$ /msie/$1 break;
}

# 当请求头 Cookie 域的值满足条件，则设定 $id 变量值为正则部分
if ($http_cookie ~* "id=([^;]+)(?:;|$)"){
    return $id $1;
}

# 当请求方法是 POST，则返回 405
if ($request_method = POST){
    return 405;
}

# 限制下载速度为 10k，$slow 可通过 set 指令设置
if ($slow){
    limit_rate 10k;
}

# 当请求头中 Referer 头域值为空或 www.example.com 时，允许访问，否则返回 403
valid_referers none www.example.com;
if ($invalid_referer){
    return 403;
}
```

```nginx configuration
# 示例：
server{ 
    location / { 
        # 对请求的Referer进行验证，如果没有Referer头域 
        # 或者头域值为www.example.com，则允许访问
        valid_referers none www.example.com; 
        if ($invalid_referer) {
            return 403;
        } 
        root /home/async/www;
    }
    location /images/ {
    root /home/async/www;
    }
}
```

```shell
nginx -s reload  # 重载配置
```

**Nginx 常用变量及其含义**

| 变量名 | 描述 |
| --- | --- |
| $args | 请求参数 |
| $arg_name | 请求参数中 name 字段 |
| $content_type | Content-Type 头域值 |
| $cookie_name | 指定名称的 Cookie |
| $host | Host 头域值 |
| $request | 完整原始请求行 |
| $scheme | 请求方案，如 HTTP 或 HTTPS |
| $server_protocol | 请求协议，如 HTTP/1.1，或 HTTP/2.0 |
| $url | 当前请求的 URI |
| $reqeust_method | 请求方法，GET或POST |

- [Nginx 支持的嵌入变量](http://nginx.org/en/docs/http/ngx_http_core_module.html#variables)
- [Nginx 指令列表](http://nginx.org/en/docs/http/ngx_http_core_module.html#Directives)

**limit_rate指令为例**

| 语法 | limit_rate rate |
| --- | --- |
| 默认 | limit_rate 0; |
| 语境 | http, server, location, if in location 

作用：限制客户端的传输速度，单位为字节/秒，默认值为 0，即不限速

**注意**：对单个请求设置限制，如果客户端同时打开两个链接，则总速率将指定限制的两倍，除了全局限速，还可根据条件设置限速

```nginx configuration
server {
    if (condition){
        set $limit_rate 100k;
    }
}
```

**ngx_http_rewrite_module模块**

| 语法 | rewrite regex replacement [flag]; |
| --- | --- |
| 默认 | - |
| 语境 | server, location, if |

如果指定的正则表达式与请求 URI 匹配，则 URI 将根据 replacement 字符串的指定进行更改。

`rewrite` 按照在配置文件中出现的顺序依次执行，使用标志终止对指令的进一步处理，
如果替换字符串以 `http://`、`https://`或`$scheme` 开头，则停止处理并重定向返回给客户端

**flag 参数**：

- last：停止处理当前 `ngx_http_rewrite_module` 指令集，并开始搜索与更改后的 URI 匹配的新位置
- break：`ngx_http_rewrite_module` 与 `break` 一样，可停止处理当前指令集
- redirect：返回带有 302 代码的临时重定向，如果替换字符串不以 `http://`、`https://`或`$scheme` 开头，则使用它
- permanent：返回 301 代码的永久重定向

```nginx configuration
server {
    ...
    rewrite ^(/download/.*)/media/(.*)\..*$ $1/mp3/$2.mp3 last;
    rewrite ^(/download/.*)/media/(.*)\..*$ $1/mp3/$2.ra last;
    return 403
    ...
}
```

### Nginx 日志

记录每次请求的相关信息，了解客户端请求和服务器端响应状态

分为 **访问日志** 和 **错误日志**

存储路径可在 nginx 主配置文件中查看
- 访问日志存放路径指令名为：`access_log`
- 错误日志存放路径指令名为：`error_log`

```nginx configuration
access_log /var/log/nginx/access.log main;
error_log /var/log/nginx/error.log;
```

#### 访问日志

记录客户端访问 Nginx 的请求信息，如客户端的 IP 地址、请求的 URI、响应状态、Referer 头域的值等

```shell
192.168.0.105 - - [11/Aug/2021:18:51:55 +0800] "GET / HTTP/1.1" 200 223 "-" "PostmanRuntime/7.28.2"
```

Nginx 与 访问日志相关指令是 `log_format` 和 `access_log`

`log_format` 用来设置访问日志的格式，日志文件中的每条日志记录的格式，在主配置文件中的设置如下：

```nginx configuration
# 访问日志默认 main 格式，并且里面记录很多信息
log_format main '$remote_addr - $remote_user [$time_local] "$request"'
                '$status $body_bytes_sent "$http_referer"'
                '"$http_user_agent" "$http_x_forwarded_for"';
```

**log_format** 支持的变量及其释义：

| 变量 | 释义 |
| --- | --- |
| $remote_addr | 客户端 IP（使用代理，显示代理服务器的 IP 地址） |
| $remote_user | 客户端用户名（通常为 "-"） |
| $time_local | 客户端访问时间和时区 |
| $request | 客户端 URL 以及请求方法 |
| $status | 响应状态码，（200/404/...） |
| $body_bytes_sent | 客户端发送的文件主体内容字节数 |
| $http_referer | 客户端所使用的代理 |
| $http_user_agent | 客户端 IP 地址，如果使用代理，仍显示客户端的 IP 地址 |
| $http_x_forwarded_for | 客户端访问来源链接 |

#### 错误日志

记录客户端访问 Nginx 错误时的请求信息，不支持自定义格式（**排查错误和测试**）

等级：`debug`、`info`、`notice`、`warn`、`error` 和 `crit`，从左到右日志级别逐步递增

Nginx 主配置文件将错误日志界别设为 `warn`：

```shell
时间 原因 客户端IP地址 请求方式 协议版本等信息
```