---
title: PostgreSQL安装
date: 2017-03-19 00:38:05
tags:
---
Tips:

强烈建议关闭360

PostgreSQL 报错
查看服务器状态 报错无效的‘UTF8’编码顺序
检查配置文件postgresql.conf中的配置变量lc_messages，把值改为 English_United States.1252

ps. 检查客户端编码格式

show client_encoding;
检查服务器端编码格式

show server_encoding;