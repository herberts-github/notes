[TOC]

# URI/URL

## URI 

统一资源标识符，[RFC2396](https://www.ietf.org/rfc/rfc2396.txt)

- Uniform：规定统一格式可方便处理多种不同类型的资源，而不用根据上下文环境识别资源指定访问方式
- Resource：资源定义为 “可标识的任何东西”，可以是单一或多数的集合体
- Identifier：可标识的对象，标识符

URI：由某个协议方案表示的资源的定位标识符

**协议方案**：访问资源所使用的协议类型名称

- http
- ftp
- mailto
- telnet
- file 等

> 由 IANA（互联网号码分配局）管理颁布 - [IANA URI 标识符方案](http://www.iana.org/assignments/uri-schemes/uri-schemes.xhtml)

## URL

URI 用字符串标识某一互联网资源

URL 表示资源的地点（互联网所处位置），是 URI 的子集

## URI 格式

表示指定的 URI，使用涵盖所有必要信息的绝对 URI / URL 以及相对 URL

**绝对 URI 格式**：

```markdown
http://user:pass@www.example.jp:80/dir/index.html?uid=1#ch1
|           |           |        |      |            |   |—— 片段标识符：标记出已获取资源中的子资源（可选）
|           |           |        |      |            |—— 查询字符串：针对已指定的文件路径内的资源（可选）
|           |           |        |      |—— 带层次的文件路径：指定服务器上文件路径定位特指资源
|           |           |        |—— 服务器端口：服务器连接的网络端口号（可选，默认80）
|           |           |—— 服务器地址：指定待访问的地址（DNS解析网站名称/IPv4或6地址名）
|           |—— 登录信息（认证）：指定用户认证信息作为从服务器端获取资源必要登录信息（可选）
|—— 协议名：使用协议方案获取访问资源时指定协议类型（可使用 data: 或 javascript: 指定数据或脚本程序方案名）
```