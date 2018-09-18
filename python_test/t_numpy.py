#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import numpy

a = numpy.arange(25).reshape(5, 5)
print(a)
print( a.sum(axis = 0))
print( a.sum(axis = 1))

'''
print("使用列表生成以为数组")
data=[1,2,3,4,5,6]
x=numpy.array(data)
print(x)
print(x.dtype)

a=numpy.arange(25).reshape(5,5)
print(a)
print(a.ndim)
print(a.itemsize)
print(a.size)
print(a.dtype.name)

b=numpy.zeros((3,5))
print(b)
c=numpy.ones((4,5))
print(c)
e=numpy.empty((5,6))
print(e)

'''
