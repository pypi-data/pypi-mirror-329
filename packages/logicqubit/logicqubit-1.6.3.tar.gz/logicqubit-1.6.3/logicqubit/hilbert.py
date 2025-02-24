#!/usr/bin/python
# -*- coding: UTF-8 -*-

# Author Cleoner S. Pietralonga
# e-mail: cleonerp@gmail.com
# Apache License

import numpy as np
from sympy.physics.quantum import TensorProduct
from logicqubit.utils import *

"""
Hilbert space
"""
class Hilbert():
    __number_of_qubits = 1
    __numeric = True
    __first_left = True

    @staticmethod
    def ket(value):  # get ket state
        result = Matrix([[Utils.onehot(i, value)] for i in range(2)], Hilbert.__numeric)
        return result

    @staticmethod
    def bra(value):  # get bra state
        result = Matrix([Utils.onehot(i, value) for i in range(2)], Hilbert.__numeric)
        return result

    @staticmethod
    def getState():  # get state of all qubits
        if Hilbert.getIsNumeric():
            state = Hilbert.kronProduct([Hilbert.ket(0) for i in range(Hilbert.getNumberOfQubits())])
        else:
            if Hilbert.isFirstLeft():
                a = sp.symbols([str(i) + "a" + str(i) + "_0" for i in range(1, Hilbert.getNumberOfQubits() + 1)])
                b = sp.symbols([str(i) + "b" + str(i) + "_1" for i in range(1, Hilbert.getNumberOfQubits() + 1)])
            else:
                a = sp.symbols([str(Hilbert.getNumberOfQubits() + 1 - i) + "a" + str(i) + "_0" for i in
                                reversed(range(1, Hilbert.getNumberOfQubits() + 1))])
                b = sp.symbols([str(Hilbert.getNumberOfQubits() + 1 - i) + "b" + str(i) + "_1" for i in
                                reversed(range(1, Hilbert.getNumberOfQubits() + 1))])
            state = Hilbert.kronProduct([Hilbert.ket(0) * a[i] + Hilbert.ket(1) * b[i] for i in range(Hilbert.getNumberOfQubits())])
        return state

    @staticmethod
    def getAdjoint(psi):  # get adjoint matrix
        result = psi.adjoint()
        return result

    @staticmethod
    def product(Operator, psi):  # performs an operation between the operator and the psi state
        result = Operator * psi
        return result

    @staticmethod
    def kronProduct(list):  # Kronecker product
        A = list[0]  # acts in qubit 1 which is the left most
        for M in list[1:]:
            A = A.kron(M)
        return A

    @staticmethod
    def setNumberOfQubits(number):
        Hilbert.__number_of_qubits = number

    @staticmethod
    def getNumberOfQubits():
        return Hilbert.__number_of_qubits

    @staticmethod
    def setNumeric(numeric):
        Hilbert.__numeric = numeric

    @staticmethod
    def getIsNumeric():
        return Hilbert.__numeric

    @staticmethod
    def setFirstLeft(value):
        Hilbert.__first_left = value

    @staticmethod
    def isFirstLeft():
        return Hilbert.__first_left


"""
Wrap methods from the numpy, cupy and sympy libraries.
"""
class Matrix:

    def __init__(self, matrix, numeric=True):
        self.__matrix = matrix
        self.__numeric = numeric
        if isinstance(matrix, list):  # if it's a list
            if self.__numeric:
                self.__matrix = np.array(matrix)  # create matrix with numpy
            else:
                self.__matrix = sp.Matrix(matrix)  # create matrix with sympy
        else:
            if isinstance(matrix, Matrix):  # if it's a Matrix class
                self.__matrix = matrix.get()
            else:
                self.__matrix = matrix

    def __add__(self, other):  # sum of the matrices
        result = self.__matrix + other.get()
        return Matrix(result, self.__numeric)

    def __sub__(self, other):  # subtraction of the matrices
        result = self.__matrix - other.get()
        return Matrix(result, self.__numeric)

    def __mul__(self, other):  # product of the matrices
        if isinstance(other, Matrix):
            other = other.get()
            if self.__numeric:
                result = np.dot(self.__matrix, other)  # for numpy matrix
            else:
                result = self.__matrix * other
        else:
            result = self.__matrix * other
        return Matrix(result, self.__numeric)

    def __truediv__(self, other):
        result = self.__matrix * (1./other)
        return Matrix(result, self.__numeric)

    def __eq__(self, other):
        return self.__matrix == other.get()

    def __str__(self):
        return str(self.__matrix)

    def kron(self, other):  # Kronecker product
        if self.__numeric:
            result = np.kron(self.__matrix, other.get())
        else:
            result = TensorProduct(self.__matrix, other.get())
        return Matrix(result, self.__numeric)

    def get(self):
        return self.__matrix

    def getAngles(self):  # converts state coefficients into angles
        angles = []
        if self.__numeric:
            angles = np.angle(self.__matrix)
        else:
            print("This session is symbolic!")
        return angles

    def trace(self):  # get matrix trace
        result = self.__matrix.trace()
        return Matrix(result, self.__numeric)

    def adjoint(self):  # get matrix adjoint
        if self.__numeric:
            result = self.__matrix.transpose().conj()
        else:
            result = self.__matrix.transpose().conjugate()
        return Matrix(result, self.__numeric)
