---
title: PostgreSQL配置文件postgresql.conf
date: 2017-03-19 00:45:42
tags:
  - PostgreSQL
categories: Programming
---
postgresql.conf文件，将数据库服务器的监听模式修改为监听所有主机发出的连接请求。
定位到#listen_addresses=’localhost’。PostgreSQL安装完成后，默认是只接受来在本机localhost的连接请 求。