#!/usr/bin/env python3
# -*- coding:utf-8 -*-

class NumberObject:
    def __init__(self,value):
        self.value=value

    def __eq__(self,object):
        print('__eq__')
        return self.value==object.value
    def __ne__(self,object):
        print('__ne__')
        return self.value!=object.value
    def __lt__(self, other):
        print('__lt__')
        return self.value<other.value
    def __gt__(self, other):
        print('__gt__')
        return self.value>other.value

if __name__=="__main__":
    num1=NumberObject(1)
    num2=NumberObject(2)
    print('num1==num2?------------>{}\n'.format(num1==num2))
    print('num1!=num2?------------>{}\n'.format(num1!=num2))
    print('num1<num2?------------>{}\n'.format(num1<num2))
    print('num1>num2?------------>{}\n'.format(num1>num2))
