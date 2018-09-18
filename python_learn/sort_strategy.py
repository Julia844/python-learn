#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import numpy
from sympy import diff
from decimal import Decimal
from math import sin, cos, exp

class BiSection:
    # find where the function become 0 in [a,b] using bisection
    def __init__(self):
        return

    def bisection(self, function, a, b):
        start = a
        end = b
        if function(a) == 0:
            return a
        elif function(b) == 0:
            return b
        elif function(a) * function(b) > 0:
            print("couldn\'t find root in [a,b]")
            return
        else:
            mid = (start + end) / 2
            while abs(start - mid) > 0.0000001:
                if function(mid) == 0:
                    return mid
                elif function(mid) * function(start) < 0:
                    end = mid
                else:
                    start = mid
                mid = (start + end) / 2
            return mid


class InterSection:
    # find the point which navigates function:f getting the slope is 0
    def intersection(self, function, a, b):
        x0 = a
        x1 = b
        while True:
            x2 = x1 - function(x1) / (function(x1) - function(x0)) / (x1 - x0)
            if abs(x2 - x1) < 0.0000001:
                return x2
            x0 = x1
            x1 = x2


class LUDecomposition:
    def __init__(self, table):
        rows, columns = numpy.shape(table)
        self.L = numpy.zeros((rows, columns))
        self.U = numpy.zeros((rows, columns))
        self.table = table

    def decomposition(self):
        rows, column = numpy.shape(self.table)
        if rows != column:
            return
        for i in range(column):
            for j in range(i - 1):
                sum = 0
                for k in range(j - 1):
                    sum += self.L[i][k] * self.U[k][j]
                self.L[i][j] = (self.table[i][j] - sum) / self.U[j][j]
            self.L[i][i] = 1
            for j in range(i - 1, column):
                sum1 = 0
                for k in range(i - 1):
                    sum1 += self.L[i][k] * self.U[k][j]
                self.U[i][j] = self.table[i][j] - sum1
        return self.L, self.U


class Newton:
    # use f1 implement Intersection
    def newton(self, function, function1, startingInt):  # function is the f(x) and function1 is the f'(x)
        x_n = startingInt
        while True:
            x_n1 = x_n - function(x_n) / function1(x_n)
            if abs(x_n - x_n1) < 0.00001:
                return x_n1
            x_n = x_n1


def f(x):
    return (x ** 3) - 2 * x - 5


def f1(x):
    return 3 * (x ** 2) - 2


class NewtonRaphson:
    # Finds root from the point 'a' of function'

    def raphson(self,function,a):
        while True:
            x=a
            c = Decimal(a) - Decimal(eval(function)) / Decimal(eval(str(diff(function))))
            print('c:{}'.format(c))
            x = c
            a = c
            if (abs(eval(function))) < 10 ** -15:
                return c
    def verify_result(self):
        # Find root of trignometric fucntion
        # Find value of  pi
        print ('sin(x) = 0', self.raphson('sin(x)', 2))

        # Find root of polynomial
        print ('x**2 - 5*x +2 = 0', self.raphson('x**2 - 5*x +2', 0.4))

        # Find Square Root of 5
        print ('x**2 - 5 = 0', self.raphson('x**2 - 5', 0.1))

        #  Exponential Roots
        print ('exp(x) - 1 = 0', self.raphson('exp(x) - 1', 0))


if __name__ == "__main__":

    print('test BiSection')
    bisection = BiSection()
    print(bisection.bisection(f, 1, 1000))

    print("test InterSection")
    intersection = InterSection()
    print(intersection.intersection(f, 3, 3.5))

    print("test LU decomposition")
    # matrix=numpy.arange(25).reshape(5,5)
    matrix = numpy.array([[2, -2, 1], [0, 1, 2], [5, 3, 1]])
    lu = LUDecomposition(matrix)
    print(matrix)
    for obj in lu.decomposition():
        print(obj)

    print("test Newton")
    newton = Newton()
    print(newton.newton(f, f1, 3))

    print("test Newton Raphson")
    nr=NewtonRaphson()
    nr.verify_result()
