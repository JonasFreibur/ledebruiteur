"""
Le Debruiteur
Jonas Freiburghaus
Romain Capocasale
He-Arc, INF3dlm-a
Image Processing course
2019-2020
"""

import tensorflow.keras.backend as K


def generator_loss(y_true, y_pred, Dg, style_features, comb_features):
    """Generator loss

    Arguments:
        y_true {Array} -- Ground truth
        y_pred {Array} -- Predicted array
        Dg {float} -- Discriminator loss on fake images
        style_features {list} -- Style features
        comb_features {list} -- Combination features

    Returns:
        float -- Generator loss
    """

    def loss(y_true, y_pred):
        s_loss = 0
        for style_feature, comb_feature in zip(style_features, comb_features):
            s_loss += style_loss(style_feature, comb_feature)

        s_loss /= len(style_features)

        return 0.5 * adversial_loss(Dg) + pixel_loss(y_true, y_pred) + s_loss

    return loss


def pixel_loss(y_true, y_pred):
    """Pixel loss l2 loss of pixelwise differences

    Arguments:
        y_true {Array} -- Ground truth
        y_pred {Array} -- Predicted array

    Returns:
        float -- RMSE
    """
    return K.sqrt(K.mean(K.square(y_pred - y_true)))


def style_loss(style_feature, comb_feature):
    """Style loss

    Arguments:
        style_feature {Array} -- Style feature
        comb_feature {Array} -- Combination feature

    Returns:
        float -- style loss
    """
    S = gram_matrix(style_feature)
    C = gram_matrix(comb_feature)
    channels = 1
    size = 100 * 100
    return K.sum(K.square(S - C)) / (4.0 * (channels ** 2) * (size ** 2))


def gram_matrix(x):
    """Gram matrix

    Arguments:
        x {Array} -- Input array

    Returns:
        array -- Gram matrix
    """
    features = K.batch_flatten(K.permute_dimensions(x, (2, 0, 1)))
    gram = K.dot(features, K.transpose(features))
    return gram


def adversial_loss(x):
    """Adversial loss

    Arguments:
        x {Array} -- Input array

    Returns:
        float -- Adversial loss
    """
    return -K.mean(K.log(x))