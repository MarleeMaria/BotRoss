import cv2
import numpy as np
import math
from sklearn.cluster import KMeans
from .utils import limit_size, regulate

# lets break this
class ColorPalette:
    def __init__(self, colors, base_len=0):
        self.colors = colors
        # print(self.colors)
        print(colors)
        self.base_len = base_len if base_len > 0 else len(colors)

    @staticmethod
    def from_image(img, n, sentColors, max_img_size=200, n_init=10):
        # scale down the image to speedup kmeans
        img = limit_size(img, max_img_size)

        clt = KMeans(n_clusters=n, n_jobs=1, n_init=n_init)
        clt.fit(img.reshape(-1, 3))
        # print(clt)
        # black and white
        # clt.cluster_centers_ = [[225, 225, 225], [0, 0, 0]]
        # any colors we have!
        clt.cluster_centers_ = sentColors


        return ColorPalette(clt.cluster_centers_)

    def extend(self, extensions):
        extension = [regulate(self.colors.reshape((1, len(self.colors), 3)).astype(np.uint8), *x).reshape((-1, 3)) for x
                     in
                     extensions]

        return ColorPalette(np.vstack([self.colors.reshape((-1, 3))] + extension), self.base_len)

    def to_image(self):
        cols = self.base_len
        #rows = int(math.ceil(len(self.colors) / cols))
        rows = int(len(self.colors) / cols)

        res = np.zeros((rows * 80, cols * 80, 3), dtype=np.uint8)
        for y in range(rows):
            for x in range(cols):
                if y * cols + x < len(self.colors):
                    color = [int(c) for c in self.colors[y * cols + x]]
                    cv2.rectangle(res, (x * 80, y * 80), (x * 80 + 80, y * 80 + 80), color, -1)

        return res

    def __len__(self):
        return len(self.colors)

    def __getitem__(self, item):
        return self.colors[item]
