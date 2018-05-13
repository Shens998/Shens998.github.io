---
title: 基于Github和Hexo的多端个人博客同步
date: 2018-05-13 19:39:17
tags:
  - Hexo
categories: Programming
---
# 基于Github和Hexo的个人博客构建

基于Github和Hexo的个人博客教程网上很多，可以参考[这里](https://www.jianshu.com/p/6fb0b287f950)

# 多终端博客内容同步

## 基本原理
Github即充当了个人静态网站的角色也利用其最基础的文件备份和版本控制的方法，将本地的网站文件备份到Github上。
利用Github建立两个仓库Master和Hexo

Master - 对应的博客网站仓库
Hexo   - 对应的Hexo网站内战代码

同样的在本地也建立这两个仓库。
在操作时，是在Master分支下新建博客页面并将生成的静态网站push到Master分支，同时在Hexo分支下将Hexokinase网站的代码Push到Hexo分支
#要在hexo的配置中将部署git设置为master分支

## 基本代码

Hexo 命令
```cmd
hexo -g #新建新文件
hexo -s #在本地网站中查看
hexo -d #将网页推送到远程仓库
```

Git 命令
```
git add. #添加目录下所有文件
git commit -m "更新说明" #提交并添加更新说明
git push -u origin master #推送更新到远程仓库

```
在另一个终端
```
git init 
git remote add origin <server> 
git fetch --all 
git reset --hard origin/master

```

日常维护
```
#在hexo分支
git pull #同步更新 
hexo new post "新建文章" #简写形式 hexo n "新建文章" 
hexo clean #清除旧的public文件夹
hexo generate #生成静态文件 简写形式 
hexo g 
hexo deploy #发布到github上 简写形式 hexo d 

git checkout hexo #切换到hexo分支
git add . #添加更改文件到缓存区 
git commit -m "更新说明" #提交到本地仓库 
git push -u origin master #推送到远程仓库进行备份

```