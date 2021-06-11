"""
@Author: P_k_y
@Time: 6/10/2021
"""
import pyautogui
import random
from Constance import *
import time
import pytesseract
import numpy as np

import cv2

pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe'

# pyautogui.FAILSAFE = True
# pyautogui.PAUSE = 0.15      # 启用决策延时

action_dim = 14
keep_down_time = 0.01


def get_frame():
    """
    获取当前帧画面，并从帧画面中提取相关信息。
    :return:
    """
    frame = pyautogui.screenshot()
    frame = frame.resize((820, 462))

    # 提取kill-die的信息
    KD_info_region = (590, 15, 640, 35)
    KD_info_img = frame.crop(KD_info_region)
    KD_info = pytesseract.image_to_string(KD_info_img)

    kill, die = KD_info.split('vs')
    kill, die = int(kill), int(die)

    # 提取当前血量信息
    hp_info_region = (375, 145, 455, 155)
    hp_info_img = frame.crop(hp_info_region)
    hp_info_img.save('test.png')

    img = cv2.cvtColor(np.asarray(frame), cv2.COLOR_RGB2BGR)

    img = cv2.rectangle(img, (375, 150), (455, 165), color=(10, 10, 255), thickness=2)

    return img, kill, die


def main():
    while True:
        frame, *_ = get_frame()

        random_action_idx = random.randint(0, action_dim-1)
        action = action_mapping[random_action_idx]

        """ 根据行为类型决定是单个按键还是多个按键 """
        # if random_action_idx <= 9:
        #     pyautogui.keyDown(action)
        #     time.sleep(keep_down_time)
        #     pyautogui.keyUp(action)
        # else:
        #     pyautogui.hotkey(action[0], action[1])

        cv2.imshow("test", frame)
        cv2.waitKey(1)


if __name__ == '__main__':
    pyautogui.alert(text='Automatic script is ready. Start to train?', title='AI Scrip')
    time.sleep(2)
    # get_frame()
    main()
