---
title: PostgreSQL客户端认证pg_hba.conf文件
date: 2017-03-19 00:39:24
tags:
---

本文主要参考postgreSQL 9.3版本的官方手册，以及[该文](http://www.qingpingshan.com/shujuku/postgresql/156383.html)

pg_hba.conf 文件
该文件负责对postgreSQL的客户端认证方式进行配置。在pg_hba.conf文件中，每条记录占一行，指定一条访问认证规则。总共有7中访问方式

连接方式|数据库 |用户 |地址| 连接方式|授权选项
----|----|----|----|----|----
local|      database | user | address |auth-method  |[auth-options]
host   |    database|  user | address | auth-method |[auth-options]
hostssl   | database | user | address | auth-method | [auth-options]
hostnossl  |database | user | address | auth-method | [auth-options]
host      | database  |user | IP-address IP-mask | auth-method | [auth-options]
hostssl   | database | user | IP-address IP-mask | auth-method | [auth-options]
hostnossl  |database | user | IP-address IP-mask | auth-method | [auth-options]

举个栗子：
32 -> 192.168.1.1/32 表示必须是来自这个IP地址的访问才合法；
24 -> 192.168.1.0/24 表示只要来自192.168.1.0 ~ 192.168.1.255的都合法；
16 -> 192.168.0.0/16 表示只要来自192.168.0.0 ~ 192.168.255.255的都合法；
8 -> 192.0.0.0/16 表示只要来自192.0.0.0 ~ 192.255.255.255的都合法；
0 -> 0.0.0.0/0 表示全部IP地址都合法，/左边的IP地址随便了只要是合法的IP地址即可；

# 访问规则说明
## 连接方式（Type）
连接方式共有四种：**local，host hostssl，hostnossl**

1.  **local**
这条记录匹配通过 Unix 域套接字进行的联接企图， 没有这种类型的记录，就不允许 Unix 域套接字的联接。

2. **host**
这条记录匹配通过TCP/IP网络进行的联接尝试.他既匹配通过ssl方式的连接，也匹配通过非ssl方式的连接.
**Tips**：要使用该选项你要在postgresql.conf文件里设置 listen_address 选项，不在listen_address里的IP地址是无法匹配到的。因为默认的行为是只在localhost上监听本地连接。

3. **hostssl**
这条记录匹配通过在TCP/IP上进行的SSL联接企图.
要使用该选项，服务器编译时必须使用–with-openssl选项，并且在服务器启动时ssl设置是打开的，具体内容可见[这里](https://www.postgresql.org/docs/9.3/static/ssl-tcp.html)。

4. **hostnossl**
与hostssl相反，只匹配通过在TCP/IP上进行的非SSL联接企图

# 数据库
声明记录所匹配的数据库。
值 all 表明该记录匹配所有数据库;
值 sameuser表示如果被请求的数据库和请求的用户同名，则匹配;
值 samegroup 表示请求的用户必须是一个与数据库同名的组中的成员;
值 replication 表示匹配一条replication连接，它不指定一个特定的数据库，一般在流复制中使用;

在其他情况里，这就是一个特定的 PostgreSQL 数据库的名字。 我们可以通过用逗号分隔的方法声明多个数据库。 一个包含数据库名的文件可以通过对该文件前缀 @ 来声明．该文件必需和 pg_hba.conf 在同一个目录。

# 用户user
为这条记录声明所匹配的 PostgreSQL 用户，值 all 表明它匹配 于所有用户。否则，它就是特定 PostgreSQL 用户的名字，多个用户名可以通过用逗号分隔的方法声明，在名字前面加上+代表匹配该用户组的所有用户。一个包含用户名的文件可以 通过在文件名前面前缀 @ 来声明，该文件必需和 pg_hba.conf 在同一个目录。

##地址address
指定匹配的客户端的地址，它可以是一个主机名，一个IP地址范围，或者下面提到的这些选项。

一个IP地址范围是一个标准的点分十进制表示的 IP地址/掩码值。注意， 在’IP地址’,’/‘和’掩码值’之间不要有任何的空白字符。

比如对于IPv4地址来说， 172.20.143.89/32指定单个主机的IP，172.20.143.0/24代表一个小的子网。对于IPv6地址来说，::1/128指定单个主机(这里是本机环回地址)，fe80::7a31:c1ff:0000:0000/96 指定一个IPv6的子网。0.0.0.0/0代表所有IPv4地址，::0/0代表所有IPv6地址。

一个IPv4地址选项只能匹配IPv4地址，一个IPv6地址选项只能匹配IPv6地址，即使给出的地址选项在IPV4和IPv6中同时存在。

当然你可以使用 all 选项来匹配所有的IP地址，使用 samehost 匹配服务器自己所有的IP地址，samenet来匹配服务器直接接入的子网。

如果指定的是主机名(既不是IP地址也不是上面提到的选项)，这个主机名将会和发起连接请求的客户端的IP地址的反向名称解析结果(即通过客户端的IP解析其主机名，比如使用反向DNS查找)进行比对，如果存在匹配，再使用正向名称解析(例如DNS查找)将主机名解析为IP地址(可能有多个IP地址)，再判断客户端的IP地址是否在这些IP地址中。如果正向和反向解析都成功匹配，那么就真正匹配这个地址(所以在pg_nba.conf文件里的主机地址必须是客户端IP的 address-to-name 解析返回的那个主机名。一些主机名数据库允许将一个IP地址和多个主机名绑定,但是在解析IP地址时，操作系统只会返回一个主机名)。

有些主机名以点(.)开头，匹配那些具有相同后缀的主机名，比如*.example.com匹配foo.example.com(当然不仅仅只匹配foo.example.com)。

还有，在pg_hba.conf文件中使用主机名的时候，你最好能保证主机名的解析比较快，一个好的建议就是建立一个本地的域名解析缓存(比如nscd)。

本选项只能在连接方式是host,hostssl或者hostnossl的时候指定。

IP地址，子网掩码
这两个字段包含可以看成是标准点分十进制表示的 IP地址/掩码值的一个替代。例如。使用255.255.255.0 代表一个24位的子网掩码。它们俩放在一起，声明了这条记录匹配的客户机的 IP 地址或者一个IP地址范围。本选项只能在连接方式是host,hostssl或者hostnossl的时候指定。

## 认证方法authentication method
1. **Trust**
无条件地允许联接，这个方法允许任何可以与PostgreSQL 数据库联接的用户以他们期望的任意 PostgreSQL 数据库用户身份进行联接，而不需要口令。

2. **Reject**
联接无条件拒绝，常用于从一个组中”过滤”某些主机。

3. **MD5**
要求客户端提供一个 MD5 加密的口令进行认证，这个方法是允许加密口令存储在pg_shadow里的唯一的一个方法。MD5是常用的密码认证方式，如果你不使用ident，最好使用md5。密码是以md5形式传送给数据库，较安全，且不需建立同名的操作系统用户。

4. **Password**
Password是以明文密码传送给数据库，建议不要在生产环境中使用。

5. **Ident**
Ident是Linux下PostgreSQL默认的local认证方式，凡是能正确登录服务器的操作系统用户（注：不是数据库用户）就能使用本用户映射的数据库用户不需密码登录数据库。用户映射文件为pg_ident.conf，这个文件记录着与操作系统用户匹配的数据库用户，如果某操作系统用户在本文件中没有映射用户，则默认的映射数据库用户与操作系统用户同名。比如，服务器上有名为user1的操作系统用户，同时数据库上也有同名的数据库用户，user1登录操作系统后可以直接输入psql，以user1数据库用户身份登录数据库且不需密码。
此外PostgreSQL还支持更多的加密方法可以参考官方的文件[这里](https://www.postgresql.org/docs/9.3/static/auth-pg-hba-conf.html).