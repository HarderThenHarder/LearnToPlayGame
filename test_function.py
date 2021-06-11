"""
@author: P_k_y
"""
import cv2
import numpy as np


def extract_hp():
    img_path = 'hp_info.png'
    hp_img = cv2.imread(img_path)
    hp_img = cv2.cvtColor(hp_img, cv2.COLOR_RGB2GRAY)

    _, hp_img_binary = cv2.threshold(hp_img, 100, 255, cv2.THRESH_BINARY)

    up = np.sum(hp_img_binary / 255)
    down = hp_img_binary.shape[0] * hp_img_binary.shape[1]

    hp_info = up / down

    cv2.imshow('origin', hp_img)
    cv2.imshow('binary', hp_img_binary)

    cv2.waitKey()


if __name__ == '__main__':
    extract_hp()