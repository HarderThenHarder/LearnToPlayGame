"""
@Author: P_k_y
@Time: 6/10/2021
"""
import pyautogui
import random
from Constance import *
import time
import math

from ToolBox import *

import cv2

action_dim = 14
keep_down_time = 0.2

last_key_down = None


def extract_frame_info(enemy_hp_low_hsv, enemy_hp_high_hsv, es, self_attack_r, attack_by_tower_low_hsv,
                       attack_by_tower_high_hsv, resize_w=820, resize_h=462):
    """
    获取当前帧画面，并从帧画面中提取相关信息。
    :return:
    """
    frame = pyautogui.screenshot()
    frame = frame.resize((resize_w, resize_h))

    """ 提取当前血量信息 """
    hp_info_region = (374, 154, 455, 163)
    hp_info_img = frame.crop(hp_info_region)
    # hp_info_img.save('hp_info.png')
    hp_info = extract_hp(np.asarray(hp_info_img))

    """ 人头比 """
    hp_info_region = (590, 15, 640, 35)
    hp_info_img = frame.crop(hp_info_region)
    # hp_info_img.save('kd_info.png')

    """ 是否被塔攻击 """
    is_attacked_by_tower_region = (395, 210, 425, 240)
    is_attacked_by_tower_img = frame.crop(is_attacked_by_tower_region)
    # is_attacked_by_tower_img.save('is_attacked_by_tower.png')
    is_attacked_by_tower_flag = is_attacked_by_tower(is_attacked_by_tower_img, attack_by_tower_low_hsv,
                                                     attack_by_tower_high_hsv)

    """ 将PIL图片转换为cv2格式的np.array """
    img = cv2.cvtColor(np.asarray(frame), cv2.COLOR_RGB2BGR)

    """ 血量信息 """
    img = cv2.rectangle(img, (374, 154), (455, 163), color=(10, 10, 200), thickness=2)
    img = cv2.putText(img, 'HP: %.2f' % hp_info, (465, 163), cv2.FONT_HERSHEY_TRIPLEX, 0.45, (10, 10, 255), 1)

    """ 人头信息 """
    img = cv2.rectangle(img, (650, 15), (750, 35), color=(200, 200, 100), thickness=2)  # 人头比
    img = cv2.putText(img, 'KDA INFO', (670, 45), cv2.FONT_HERSHEY_TRIPLEX, 0.35, (200, 200, 200), 1)

    """ 自身是否被塔攻击 """
    if is_attacked_by_tower_flag:
        img = cv2.putText(img, '<Under Attack>', (355, 190), cv2.FONT_HERSHEY_TRIPLEX, 0.45, (10, 10, 255), 1)

    """ 敌方信息 """
    enemy_center, dis2enemy, relative_pos = None, None, (0, 0)
    res = get_roi(img, es, enemy_hp_low_hsv, enemy_hp_high_hsv)
    if res:
        x, y, w, h = res
        center = [x + 25, y + 47]
        cv2.circle(img, (center[0], center[1]), 3, (50, 50, 200), -1)
        cv2.circle(img, (int(resize_w / 2), int(resize_h / 2)), 3, (50, 200, 50), -1)
        dis2enemy = math.hypot(center[0] - resize_w / 2, center[1] - resize_h / 2)

        enemy_box_color = (50, 200, 0) if dis2enemy > self_attack_r else (0, 50, 200)
        dotted_rectangle(img, (x - 30, y - 25), (x + 80, y + 120), enemy_box_color, 2, label='Enemy Object')

        attack_line_color = (0, 200, 0) if dis2enemy > self_attack_r else (0, 0, 200)
        cv2.line(img, (int(resize_w / 2), int(resize_h / 2)), (center[0], center[1]), color=attack_line_color,
                 thickness=1)

        dis_txt_coord = (int((resize_w / 2 + center[0]) / 2), int((resize_h / 2 + center[1]) / 2))
        relative_pos = (int(center[0] - resize_w / 2), int(center[1] - resize_h / 2))
        img = cv2.putText(img, '%.2f' % dis2enemy, dis_txt_coord, cv2.FONT_HERSHEY_TRIPLEX, 0.35, (200, 200, 200), 1)
        enemy_center = center

    return img, hp_info, enemy_center, is_attacked_by_tower_flag, dis2enemy, relative_pos


def do_action(action_idx_list):
    action_list = [action_mapping[action_idx] for action_idx in action_idx_list]

    for action in action_list:
        pyautogui.keyDown(action)

    time.sleep(keep_down_time)

    for action in action_list:
        pyautogui.keyUp(action)


def simple_attack(enemy_center, hp_info, dis2enemy, self_attack_r, relative_pos):
    action_list = []

    if enemy_center:
        if dis2enemy > self_attack_r:
            if relative_pos[0] < 0:
                action_list.append(8)
            else:
                action_list.append(9)
            if relative_pos[1] < 0:
                action_list.append(6)
            else:
                action_list.append(7)
        attack_action = random.randint(0, 3)
        action_list.append(attack_action)
    else:
        random_move_idx = random.randint(6, 9)
        action_list.append(random_move_idx)

    if hp_info < 0.5:
        action_list.append(5)

    do_action(action_list)


def main():
    es = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))
    enemy_hp_lower_hsv = np.array([0, 191, 182])
    enemy_hp_high_hsv = np.array([5, 205, 255])
    attacked_by_tower_low_hsv = np.array([0, 197, 147])
    attacked_by_tower_high_hsv = np.array([0, 255, 255])

    self_attack_r = 300

    while True:
        frame, hp_info, enemy_center, is_attacked_by_tower_flag, dis2enemy, relative_pos = extract_frame_info(enemy_hp_lower_hsv,
                                                                                                              enemy_hp_high_hsv, es,
                                                                                                              self_attack_r,
                                                                                                              attacked_by_tower_low_hsv,
                                                                                                              attacked_by_tower_high_hsv)

        simple_attack(enemy_center, hp_info, dis2enemy, self_attack_r, relative_pos)

        cv2.imshow("Visualized Window", frame)
        cv2.waitKey(1)


if __name__ == '__main__':
    pyautogui.alert(text='Automatic script is ready. Start to train?', title='AI Scrip')
    time.sleep(1)
    main()
