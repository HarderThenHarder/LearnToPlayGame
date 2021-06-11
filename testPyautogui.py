"""
@Author: P_k_y
@Time: 6/10/2021
"""
import pyautogui
import random
from Constance import *
import time
import pytesseract

from ToolBox import *

import cv2

pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe'

action_dim = 14
keep_down_time = 0.01


def get_frame():
    """
    获取当前帧画面，并从帧画面中提取相关信息。
    :return:
    """
    frame = pyautogui.screenshot()
    frame = frame.resize((820, 462))

    # 提取当前血量信息
    hp_info_region = (374, 154, 455, 163)
    hp_info_img = frame.crop(hp_info_region)
    # hp_info_img.save('hp_info.png')
    hp_info = extract_hp(np.asarray(hp_info_img))

    # 人头比
    hp_info_region = (590, 15, 640, 35)
    hp_info_img = frame.crop(hp_info_region)
    # hp_info_img.save('kd_info.png')

    img = cv2.cvtColor(np.asarray(frame), cv2.COLOR_RGB2BGR)

    """ 血量信息 """
    img = cv2.rectangle(img, (374, 154), (455, 163), color=(10, 10, 255), thickness=2)
    img = cv2.putText(img, 'HP: %.2f' % hp_info, (465, 163), cv2.FONT_HERSHEY_DUPLEX, 0.35, (10, 10, 255), 1)

    """ 人头信息 """
    img = cv2.rectangle(img, (590, 15), (640, 35), color=(10, 10, 255), thickness=2)    # 人头比

    return img, hp_info


def main():
    while True:
        frame, hp_info = get_frame()

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
    time.sleep(1)
    main()
