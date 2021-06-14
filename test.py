"""
@author: P_k_y
"""
import cv2
import numpy as np
import pyautogui
import time


def extract_hp():
    img_path = 'hp_info.png'
    hp_img = cv2.imread(img_path)
    hp_img = cv2.cvtColor(hp_img, cv2.COLOR_RGB2GRAY)

    _, hp_img_binary = cv2.threshold(hp_img, 100, 255, cv2.THRESH_BINARY)

    kernel = np.ones((3, 3), np.uint8)
    hp_img_binary_closed = cv2.morphologyEx(hp_img_binary, cv2.MORPH_CLOSE, kernel)

    up = np.sum(hp_img_binary / 255)
    down = hp_img_binary.shape[0] * hp_img_binary.shape[1]

    hp_info = up / down

    res = np.vstack((hp_img, hp_img_binary, hp_img_binary_closed))
    cv2.imshow('HP', res)

    # cv2.imshow('origin', hp_img)
    # cv2.imshow('binary', hp_img_binary)
    # cv2.imshow('binary_closed', hp_img_binary_closed)

    cv2.waitKey()


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

    cv2.putText(img, label, (start[0], end[1] + 20), cv2.cv2.FONT_HERSHEY_TRIPLEX, 0.55, color, 1)


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
        (x, y, w, h) = bounding_boxes[0]
        dotted_rectangle(frame, (x-30, y-25), (x+80, y+120), (255, 50, 0), 2, label='[Enemy] Meng Ya')
        center = [int(x + w / 2), int(y + h / 2)]
        cv2.circle(frame, (center[0], center[1]), 1, (255, 0, 0), -1)

        cv2.imshow("Frame", frame)
        cv2.imshow("Diff", diff)
        cv2.imshow("Mask", mask)

        return center[0], center[1]

    cv2.imshow("Frame", frame)
    cv2.imshow("Diff", diff)
    cv2.imshow("Mask", mask)

    return None


def is_attacked_by_tower_test(lower_hsv=(0, 197, 147), high_hsv=(5, 255, 255)):
    es = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))

    frame = cv2.imread('is_attacked_by_tower.png')

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lowerb=lower_hsv, upperb=high_hsv)

    contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) > 0:
        print('Yes')
    else:
        print('No')

    cv2.imshow("Frame", frame)
    cv2.imshow("Mask", mask)

    cv2.waitKey()


def extract_enemy_by_hp():
    es = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))
    lower_hsv = np.array([0, 191, 182])
    high_hsv = np.array([5, 205, 255])

    while True:
        frame = pyautogui.screenshot()
        frame = frame.resize((820, 462))
        frame = np.asarray(frame)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        get_roi(frame, es, lower_hsv, high_hsv)

        key = cv2.waitKey(10) & 0xFF
        if key == ord('q'):
            break


def extract_enemy():
    target_img = 'target_imgs/enemy1.png'

    while True:
        coords = pyautogui.locateOnScreen(target_img)

        if coords:
            # 获取定位到的图中间点坐标
            x, y = pyautogui.center(coords)
            # 右击该坐标点
            pyautogui.rightClick(x, y)
            print('find!')
        else:
            print('no enemy!')

        time.sleep(0.1)


if __name__ == '__main__':
    extract_hp()
    # extract_enemy_by_hp()
    # is_attacked_by_tower_test()