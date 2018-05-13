---
title: 股票价格时序分析
tags:
  - Python
categories: Analytics
abbrlink: 37313
date: 2017-01-12 09:46:42
---
# Introduction
<font size="4">本文是在之前做数据分析的学习时候发现沈浩老师微信公共号分享的一篇文章,[股票分析| 用Python玩玩A股股票数据分析-可视化部分](http://mp.weixin.qq.com/s?__biz=MzIxNTQ4NzAwNA==&mid=2247484332&idx=1&sn=746f134abe4e6a2d459e96d1e7f74f44&chksm=9796c4dfa0e14dc98d304d211feb626c01f171bb1d765fa50a4b7aa1f6e219c368cb08ba7464&mpshare=1&scene=23&srcid=0112PO0iXGR6jcvgqrrBakiU#rd), 边学python边学习了。</font>
```Python
import pandas as pd
import pandas_datareader.data as dr
import datetime


start = datetime.datetime(2010,1,1)
end = datetime.date.today()

dianjian= dr.DataReader("601669.SS","yahoo",start,end)
maotai = dr.DataReader("600519.SS","yahoo",start,end)
quanjude = dr.DataReader("002186.SZ","yahoo",start,end)

type(dianjian)
```
pandas.core.frame.DataFrame
<!-- more -->
```Python
len(dianjian)
```
1338
```Python
dianjian.head()
```

|Date|Open|High|Low|Close|Volume|Adj Close|
|:---------|:---|:---|:---|:---|:--------|:---|
|2011-10-27|4.92|5.01|4.85|4.96|186583300|4.36|
|2011-10-28|5.04|5.18|4.92|4.97|218858400|4.37|
|2011-10-31|4.95|5.08|4.84|5.06|196341900|4.45|
|2011-11-01|5.00|5.27|4.97|5.09|284853100|4.47|
|2011-11-02|4.96|5.30|4.93|5.26|218048700|4.62|

```Python
dianjian.tail()
```

|Date|Open|High|Low|Close|Volume|Adj Close|
|:---------|:---|:---|:---|:---|:--------|:---|
|2016-12-08|7.39|7.39|7.20|7.22|71872100|7.22| 
|2016-12-09|7.21|7.47|7.16|7.40|137389300|7.40|
|2016-12-12|7.32|7.33|6.95|7.16|121215100|7.16|
|2016-12-13|7.09|7.17|7.00|7.12|60272400|7.12|
|2016-12-14|7.09|7.11|6.83|6.87|82643000|6.87|

```Python
import matplotlib.pyplot as plt
%matplotlib inline
# 控制图标尺寸
%pylab inline
pylab.rcParams['figure.figsize']=(15,9)
dianjian['Adj Close'].plot(grid = True)
```
Populating the interactive namespace from numpy and matplotlib
<matplotlib.axes._subplots.AxesSubplot at 0x21852ac4d68>

![mark](http://ojnmbqawr.bkt.clouddn.com/blog/20170112/151312262.png-Shuiyin)
# 三只股票聚合在一个dataframe里面
```Python
stocks = pd.DataFrame({"dijian": dianjian["Adj Close"],
                       "maotai": maotai["Adj Close"],
                       "quanjude": quanjude["Adj Close"]})
stocks.head()
```

|Date|dijian|maotai|quanjude|
|:---------|:--|:--------|:-----| 
|2010-01-04|NaN|109.08326|14.571|
|2010-01-05|NaN|108.76288|15.051|
|2010-01-06|NaN|107.04219|14.881|
|2010-01-07|NaN|105.09082|14.419|
|2010-01-08|NaN|103.98699|NaN|

```Python
stocks.plot(grid=True)
<matplotlib.axes._subplots.AxesSubplot at 0x21852ac4c88>
```

![mark](http://ojnmbqawr.bkt.clouddn.com/blog/20170112/151414282.png-Shuiyin)
# 不同股票双坐标可视化
```Python
stocks.plot(secondary_y=["maotai","quanjude"],grid=True)
<matplotlib.axes._subplots.AxesSubplot at 0x21854c92978>
```

![mark](http://ojnmbqawr.bkt.clouddn.com/blog/20170112/151430030.png-Shuiyin)
# 以某一日股价为基准标准化股价
```Python
stock_return =stocks.apply(lambda x:x/x[1000])
stock_return.head()
```

|Date|dijian|maotai|quanjude|
|:---------|:--|:--------|:-----| 
|2010-01-04|NaN|1.015128|0.761325|
|2010-01-05|NaN|1.012146|0.786405|
|2010-01-06|NaN|0.996134|0.777522|
|2010-01-07|NaN|0.977974|0.753383|
|2010-01-08|NaN|0.967702|NaN|

```Python
stock_return.tail()
```

|Date|dijian|maotai|quanjude|
|:---------|:-------|:-------|:-------| 
|2016-12-08|2.406667|3.142726|1.129108|
|2016-12-09|2.466667|3.143843|1.160458|
|2016-12-12|2.386667|3.041756|1.104028|
|2016-12-13|2.373333|3.098988|1.110298|
|2016-12-14|2.290000|3.092101|1.110298|

```Python
stock_return.plot(grid=True).axhline(y =1,color ="black",lw=2)
<matplotlib.lines.Line2D at 0x218558bc048>
```

![mark](http://ojnmbqawr.bkt.clouddn.com/blog/20170112/151441927.png-Shuiyin)
# TBD