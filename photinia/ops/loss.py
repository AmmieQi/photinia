#!/usr/bin/env python3

"""
@author: xi
@since: 2018-08-23
"""

import tensorflow as tf


def reduce_loss_to_scalar(loss):
    order = len(loss.shape)
    if order > 1:
        axis = tuple(range(1, order))
        loss = tf.reduce_sum(loss, axis=axis)
    loss = tf.reduce_mean(loss)
    return loss


def mse(target, output, reduce=True):
    loss = tf.square(target - output)
    if reduce:
        return reduce_loss_to_scalar(loss)
    return loss


def neg_log_likelihood(target, output, axis=-1, eps=1e-6, reduce=True):
    loss = tf.reduce_sum(target * output, axis=axis)
    loss = -tf.log(loss + eps)
    if reduce:
        return reduce_loss_to_scalar(loss)
    return loss


def cross_entropy(target, output, axis=-1, eps=1e-6, reduce=True):
    loss = tf.negative(
        target * tf.log(output + eps) +
        (1.0 - target) * tf.log(1.0 - output + eps)
    )
    loss = tf.reduce_sum(loss, axis=axis)
    if reduce:
        return reduce_loss_to_scalar(loss)
    return loss
