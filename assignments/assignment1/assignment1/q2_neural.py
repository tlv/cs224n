#!/usr/bin/env python

import numpy as np
import random

from q1_softmax import softmax
from q2_sigmoid import sigmoid, sigmoid_grad
from q2_gradcheck import gradcheck_naive


def forward_backward_prop(X, labels, params, dimensions):
    """
    Forward and backward propagation for a two-layer sigmoidal network

    Compute the forward propagation and for the cross entropy cost,
    the backward propagation for the gradients for all parameters.

    Notice the gradients computed here are different from the gradients in
    the assignment sheet: they are w.r.t. weights, not inputs.

    Arguments:
    X -- M x Dx matrix, where each row is a training example x.
    labels -- M x Dy matrix, where each row is a one-hot vector.
    params -- Model parameters, these are unpacked for you.
    dimensions -- A tuple of input dimension, number of hidden units
                  and output dimension
    """

    ### Unpack network parameters (do not modify)
    ofs = 0
    Dx, H, Dy = (dimensions[0], dimensions[1], dimensions[2])

    W1 = np.reshape(params[ofs:ofs+ Dx * H], (Dx, H))
    ofs += Dx * H
    b1 = np.reshape(params[ofs:ofs + H], (1, H))
    ofs += H
    W2 = np.reshape(params[ofs:ofs + H * Dy], (H, Dy))
    ofs += H * Dy
    b2 = np.reshape(params[ofs:ofs + Dy], (1, Dy))

    # Note: compute cost based on `sum` not `mean`.
    ### YOUR CODE HERE: forward propagation
    Z1 = X.dot(W1) + np.repeat(np.reshape(b1, (1, b1.size)), labels.shape[0], axis=0)
    H = sigmoid(Z1)
    Z2 = H.dot(W2) + np.repeat(np.reshape(b2, (1, b2.size)), labels.shape[0], axis=0)
    pred = softmax(Z2)
    cost = np.sum(-labels * np.log(pred))
    ### END YOUR CODE

    ### YOUR CODE HERE: backward propagation
    gradb2_split = pred - labels
    gradb2 = np.sum(gradb2_split, axis=0)
    gradW2 = H.T.dot(gradb2_split)
    gradb1_split = gradb2_split.dot(W2.T) * sigmoid_grad(sigmoid(Z1))
    gradb1 = np.sum(gradb1_split, axis=0)
    gradW1 = X.T.dot(gradb1_split)
    ### END YOUR CODE

    ### Stack gradients (do not modify)
    grad = np.concatenate((gradW1.flatten(), gradb1.flatten(),
        gradW2.flatten(), gradb2.flatten()))
    return cost, grad


def sanity_check():
    """
    Set up fake data and parameters for the neural network, and test using
    gradcheck.
    """
    print "Running sanity check..."

    N = 20
    dimensions = [10, 5, 10]
    data = np.random.randn(N, dimensions[0])   # each row will be a datum
    labels = np.zeros((N, dimensions[2]))
    for i in xrange(N):
        labels[i, random.randint(0,dimensions[2]-1)] = 1

    params = np.random.randn((dimensions[0] + 1) * dimensions[1] + (
        dimensions[1] + 1) * dimensions[2], )

    gradcheck_naive(lambda params:
        forward_backward_prop(data, labels, params, dimensions), params)


def your_sanity_checks():
    """
    Use this space add any additional sanity checks by running:
        python q2_neural.py
    This function will not be called by the autograder, nor will
    your additional tests be graded.
    """
    print "Running your sanity checks..."
    ### YOUR CODE HERE
    dimensions = [1, 1, 2]
    params = np.array([1.,-1.,1.,2.,1.,2.])
    labels_1 = np.array([[0., 1.]])
    X_1 = np.array([[1.]])
    labels_2 = np.array([[0., 1.], [0., 1.]])
    X_2 = np.array([[1.], [1.]])
    gradcheck_naive(lambda params:
        forward_backward_prop(X_1, labels_1, params, dimensions), params)
    gradcheck_naive(lambda params:
        forward_backward_prop(X_2, labels_2, params, dimensions), params)
    ### END YOUR CODE


if __name__ == "__main__":
    sanity_check()
    your_sanity_checks()
