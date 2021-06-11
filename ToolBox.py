"""
@author: P_k_y
"""
import cv2
import numpy as np


def extract_hp(hp_img_array: np.array) -> float:
    """
    输入np.array()<RGB模式>的图像，提取出当前血量。
    :param hp_img_array: 血量图像
    :return: 血量 -> (0, 1)
    """
    hp_img = cv2.cvtColor(hp_img_array, cv2.COLOR_RGB2GRAY)

    _, hp_img_binary = cv2.threshold(hp_img, 100, 255, cv2.THRESH_BINARY)

    up = np.sum(hp_img_binary / 255)
    down = hp_img_binary.shape[0] * hp_img_binary.shape[1]

    return up / down
