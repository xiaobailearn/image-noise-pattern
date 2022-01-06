import math

import numpy as np
import cv2
import random


def line_damage_error(img, num_precent=0.1):
    """
           数据传输通道异常
           输入:
               image  图像
           返回数据传输通道异常后的图像
      """
    # 将图像转化为YUV格式图像
    YUVImg = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
    # 分离通道
    y, Cr, Cb = cv2.split(YUVImg)
    # 获取图像属性
    row, col, chs = YUVImg.shape
    # 生成数据传输通道损坏矩阵
    damage = np.ones(img.shape[0:2], dtype=np.uint8)
    # 随机生成一个8位二进制图像，转换二进制后，0表示损坏的数据传输通道,1表示该通道传输正常
    dataChs = random.randint(0, int(math.pow(2, 7)))#224#random.randint(0, 255)
    for i in range(int(row*num_precent)):
        for j in range(int(row*num_precent)):
            # 控制传输通道
            damage[i][j] = dataChs

    # 将每个通道与通道损坏矩阵做按位与运算，得出对应通道的传输后的数据
    y = cv2.bitwise_and(y, damage)
    Cr = cv2.bitwise_and(Cr, damage)
    Cb = cv2.bitwise_and(Cb, damage)

    # 通道融合
    dst = cv2.merge([y, Cr, Cb])

    return dst

def replace_str(int_str, num):
    '''替换字符串中字符
    str:需要替换的字符串
    num:需要替换的字符的数量
    '''
    position = random.sample(range(0,8), num)
    new_int_ls = ['0']*8
    int_str = list(int_str)
    for i in range(len(int_str)):
        if (i in position) or (int_str[i] == 0):
            continue
        else:
            new_int_ls[i] = int_str[i]
    return ''.join(new_int_ls)

def line_damage_error2(img, num_precent=0.2):
    """
           数据传输通道异常
           输入:
               image  图像
           返回数据传输通道异常后的图像
      """
    # 将图像转化为YUV格式图像
    YUVImg = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
    # 分离通道
    Y, Cr, Cb = cv2.split(YUVImg)
    # 获取图像属性
    row, col, chs = YUVImg.shape
    for i in random.sample(range(row),int(row*num_precent)): #
        for j in random.sample(range(col),int(col*num_precent)): #
            Y[i][j] = int(replace_str(bin(Y[i][j])[2:], 1), 2)
            Cr[i][j] = int(replace_str(bin(Cr[i][j])[2:], 1), 2)
            Cb[i][j] = int(replace_str(bin(Cb[i][j])[2:], 1), 2)
    # 通道融合
    dst = cv2.merge([Y, Cr, Cb])
    return cv2.cvtColor(dst,cv2.COLOR_YCrCb2BGR)

# '''
#下面几行代码用来验证增强结果
src = cv2.imread("../VOCdevkit/VOC2007/JPEGImages/000000.jpg")
# cv2.imshow('original img', src)
error_img = line_damage_error2(src, 0.5)
cv2.imshow('augmentation img', error_img)
cv2.waitKey(0)
# '''
