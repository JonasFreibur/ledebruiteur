import os
import cv2
import matplotlib.pyplot as plt
from ..noise.noise import Noise


def create_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def plot_im_grid(df, noise=None, rows=5, columns=5, figsize=(8, 8)):
    if not issubclass(type(noise), Noise) and noise is not None:
        raise ValueError("noise is not of valid type Noise")

    fig = plt.figure(figsize=figsize)
    sample = rows * columns

    for i, (idx, row) in enumerate(df.sample(sample).iterrows()):
        path = row[0]
        img = cv2.imread(path)
        if noise:
            img = noise.add(img)
        fig.add_subplot(rows, columns, i + 1)
        plt.imshow(img)
        plt.axis('off')

    plt.show()
