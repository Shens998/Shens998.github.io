---
title: Matlab矩阵拼接方法
tags:
  - Matlab
categories: Programming
abbrlink: 48206
date: 2017-01-11 21:10:36
---

# 拼接操作符
用 `[]` 做拼接时，有三种连接符：逗号`,` 分号`;` 和空格` `。 
其中，分号表示换行后纵向拼接，纵向拼接要求两个拼接的矩阵的列数相同
而逗号和空格是等价的，表示不换行，直接横向拼接，横向拼接要求2个矩阵行数相同
horzcat  水平方向拼接
vertcat  垂直方向拼接
repmat   通过对现有矩阵进行复制和粘贴操作生成新的矩阵
blkdiag  现有矩阵构造对角矩阵

# Matlab不同行数矩阵拼接
遇到一个不同行数矩阵拼接问题，例如
<!-- more -->
```Matlab
A=[1 2 3 4 5 6]';

B=[1 2 3 4]';
```

 

基本想法是将行数小的矩阵补零，凑成行数一致，matlab中扩充矩阵的函数padarray

下面是合并AB矩阵的程序

 

```Matlab
l=max([length(A),length(B)]);

C=[padarray(A,[l-length(A) 0],'post') padarray(B,[l-length(B) 0],'post')]

```


程序运行结果



```Matlab
C =
1     1
2     2
3     3
4     4
5     0
6     0
```


 

附上Matlab文档中padarray函数的说明：

padarray Syntax


``` Matlab
B = padarray(A, padsize);
B = padarray(A, padsize, padval);
B = padarray(A, padsize, padval, direction);
```


## Description

B = padarray(A, padsize) pads array A with 0's (zeros). padsize is a vector of positive integers that specifies both the amount of padding to add and the dimension along which to add it. The value of an element in the vector specifies the amount of padding to add. The order of the element in the vector specifies the dimension along which to add the padding.( padsize中第一个元素为填充的行数，第二个元素填充的列数)

For example, a padsize value of [2 3] means add 2 elements of padding along the first dimension(第一维，即行) and 3 elements of padding along the second dimension(第二维，即列). By default, paddarray adds padding before the first element and after the last element along the specified dimension.

B = padarray(A, padsize, padval) pads array A where padval specifies the value to use as the pad value(填充值，若不填则默认为0). padarray uses the value 0 (zero) as the default. padval can be a scalar that specifies the pad value directly or one of the following text strings that specifies the method padarray uses to determine the values of the elements added as padding.

|Value        | Meaning|
|:------------|:---|
|'circular'   | Pad with circular repetition of elements within the dimension(重复元素).|
|'replicate'  | Pad by repeating border elements of array(边界元素).|
|'symmetric'  |Pad array with mirror reflections of itself(镜像元素).|

B = padarray(A, padsize, padval, direction) pads A in the direction specified by the string direction. direction can be one of the following strings. The default value is enclosed in braces ({}).


|Value      | Meaning|
|---------|---|
|'both' | Pads before the first element and after the last array element along each dimension. This is the default(默认填充于元素前和元素后).|
|'post' | Pad after the last array element along each dimension(填充于元素后).|
|'pre'|Pad before the first array element along each dimension(填充与元素前).|

Class Support

When padding with a constant value, A can be numeric or logical. When padding using the 'circular', 'replicate', or 'symmetric' methods, A can be of any class. B is of the same class as A.
