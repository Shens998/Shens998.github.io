---
title: PostGIS存入读取数据
date: 2017-03-19 00:48:02
tags:
  - PostgreSQL
categories: Programming
---
# PostGIS 导入栅格（Raster）数据
利用 raster2pgsql 命令，示例代码如下：

`raster2pgsql -C -s 4326 -t 300x300"E:\Data\Tiff\SST\A20022132002243.L3m_MO_SST_sst_4km.tif" raster_test | psql -h localhost -p 5432 -U postgres -d RasterDB -W`
参数的详细介绍见该[网址](http://www.postgis.org/documentation/manual-svn/using_raster.xml.html#RT_Raster_Loader).

利用QGIS 查看PostGIS中的栅格数据
DB Mangaer-add to canvas

# PostGIS导入适量数据（shapefile）

1. 文件路径中不能含有中文字符
2. SHP文件导入时要设定好参考系，即SRID标识符

