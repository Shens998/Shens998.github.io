---
title: Hexo 主题 Next 修改(TBD)
tags:
  - Hexo
categories: Programming
abbrlink: 4300
date: 2017-01-18 10:27:48
---

# 主题美化

## 代码高亮主题修改

根据[Netx的help文档](http://theme-next.iissnan.com/), Next提供了5个Code主题: `normal`, `night`,`night blue`, `night bright`, and`night eighties`
把主题配置文件中的`highlight_theme`值设置为想要的字段(本文用的是`night eighties`)：
```
highlight_theme: night eighties
```
需要注意的是，Next对语言的支持不是很完备。

# Tips

## 中文乱码问题

Hexo是根据Markdown文本来生成对应的静态文件的。可能会遇上中文乱码的问题。只需要将Markdown文件的编码格式改成`utf-8`即可。