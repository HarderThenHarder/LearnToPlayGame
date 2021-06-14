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

    kernel = np.ones((3, 3), np.uint8)
    hp_img_binary = cv2.morphologyEx(hp_img_binary, cv2.MORPH_CLOSE, kernel)

    # 闭运算将图中的噪声做平滑

    up = np.sum(hp_img_binary / 255)
    down = hp_img_binary.shape[0] * hp_img_binary.shape[1]

    return up / down


def dotted_rectangle(img, start, end, color, line_width, label):
    vertexs = []
    for i in range(start[0], end[0], 5):
        vertexs.append((i, start[1]))
    for i in range(start[1], end[1], 5):
        vertexs.append((end[0], i))
    for i in range(end[0], start[0], -5):
        vertexs.append((i, end[1]))
    for i in range(end[1], start[1], -5):
        vertexs.append((start[0], i))
    for i in range(0, len(vertexs), 2):
        cv2.line(img, vertexs[i], vertexs[i + 1], color, line_width)

    cv2.putText(img, label, (start[0], end[1] + 20), cv2.FONT_HERSHEY_TRIPLEX, 0.55, color, 1)


def get_roi(frame, es, lower_hsv, high_hsv):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lowerb=lower_hsv, upperb=high_hsv)

    diff = cv2.threshold(mask, 27, 255, cv2.THRESH_BINARY)[1]
    diff = cv2.morphologyEx(diff, cv2.MORPH_OPEN, es, iterations=1)
    diff = cv2.morphologyEx(diff, cv2.MORPH_CLOSE, es, iterations=5)

    contours, _ = cv2.findContours(diff.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) > 0:
        bounding_boxes = [cv2.boundingRect(c) for c in contours]
        bounding_boxes.sort(key=lambda x: x[0], reverse=False)
        return bounding_boxes[0]

    return None


def is_attacked_by_tower(frame, low_hsv, high_hsv):
    frame = np.asarray(frame)
    hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
    mask = cv2.inRange(hsv, lowerb=low_hsv, upperb=high_hsv)

    contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) > 0:
        return True
    return False
