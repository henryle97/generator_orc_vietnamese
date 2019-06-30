#!/usr/bin/python
# -*- coding: utf-8 -*-

from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import json
import os
import random
import sys
# from config import *

SAVE_TEXT_IMAGE_TO_DISK = True
FONT_SIZE = 20
FONT_SIZE_MIN = 20
FONT_SIZE_MAX = 20
IMG_WIDTH = 300
IMG_HEIGHT = 30

# DATASET_DIR = 'data/train/characters/'
DATASET_DIR = 'data/train/img_label/'
DATASET_FILE_NAME = 'dataset.csv'
DATASET_FILE = DATASET_DIR + DATASET_FILE_NAME
FONT_LIST = 'fonts/fonts.list'

CHARACTERS_SET = 'data/vi.characters.csv'
WORDS_SET = 'data/vi_VN.dic'
#SUM_SAMPLES = 105640
SUM_SAMPLES = 
#NO_LABEL = 190
NO_LABEL = 5




class DataGenerator:
    def __init__(self):
        self.i = 0
        self.log = []
        self.errors = []
        self.data_folder = DATASET_DIR
        self.font_list = FONT_LIST
        self.data_set_csv = DATASET_FILE
        self.characters = []
        self.dataset_size = 0
        self.color = ['#FD9206', '#FA1707', '#000000', '#4321EC']

    # def rgb2gray(self, rgb):
    #     return np.dot(rgb[..., :3], [0.299, 0.587, 0.114])

    # def get_list_characters(self):
    #     if len(self.characters) != 0:
    #         return self.characters
    #     else:
    #         characters = []
    #         with open(CHARACTERS_SET) as cf:
    #             for r in cf:
    #                 if ',,' in r:
    #                     c = ','
    #                 else:
    #                     _, c = r.split(',')
    #                 characters.append(c.replace('\n', ''))

    #         self.characters = characters
    #         return characters
    def get_list_words(self):
        with open(WORDS_SET) as ws:
            words = ws.readlines()

        words = [x.strip() for x in words]
        return words

    def create_text_image(self, text, font_ttf, idx_category, font_size):
        try:
            


            # Lấy width và height của text mới 
            image_fake = Image.new("RGB", (IMG_WIDTH, IMG_HEIGHT), (255, 255, 255))
            draw = ImageDraw.Draw(image_fake)
            font = ImageFont.truetype(font_ttf, font_size)
            w, h = draw.textsize(text, font=font)

            # Tạo ảnh có kích thừa phù hợp với text
            image = Image.new("RGB", (w+4, h+4), (255, 255, 255))
            draw = ImageDraw.Draw(image)

            
            color_rand_ind = random.randint(0,3)
            color_rand=self.color[color_rand_ind]

            # draw.text(((IMG_WIDTH - w) / 2, (IMG_HEIGHT - h) / 2), text, (0, 0, 0), font=font)
            draw.text((1, 1), text, fill=color_rand, font=font)

            if SAVE_TEXT_IMAGE_TO_DISK:
                image.save(self.data_folder + str(self.i) + '.jpg')

                with open(self.data_folder+str(self.i)+'.txt', 'w') as f:
                    f.write(text.replace(' ', ''))

                self.i = self.i + 1
                return

            self.log.append({'font': font_ttf, 'image': str(self.i) + '.jpg'})
            # self.i = self.i + 1
            return image
        except Exception as e:
            self.errors.append({'font': font_ttf, 'errors': str(e)})
            print(str(e))
            return None

    def generate_data_set(self, text, idx_category):
        images = []
        with open(self.font_list, 'r') as fonts:
            for font in fonts:
                if '#' not in font:
                    for font_size in range(FONT_SIZE_MIN, FONT_SIZE_MAX + 1):
                        # Lấy ngẫu nhiên 10% font 
                        x = random.randint(1,100)
                        if x <= 2:
                            image = self.create_text_image(text, font.replace('\n', ''), idx_category, font_size)
                        # if image != None:
                        #     self.dataset_size = self.dataset_size + 1
                        #     images.append(image)
                        

        # self.i = 0
        return images

    def generate_dataset(self):
        words = self.get_list_words()
        if SAVE_TEXT_IMAGE_TO_DISK and not os.path.exists(self.data_folder):
                os.makedirs(self.data_folder)
        ch_size = len(words)
        for idx, text in enumerate(words):
            # Tạo text từ vi_VI.dic + random 6 chữ số 
            number_rand = random.randint(100000,999999)
            rd = random.randint(1,10)
            if rd <= 6:
                text = text + ' ' + str(number_rand)
            else:
                text = text.upper() + '/' + str(number_rand)
            c_images = self.generate_data_set(text, idx)
            percent = (idx / ch_size) * 100
            print(f'Done {percent:.3f}%')
            # if self.i > 500:
            #     return
            # print('.', end='')
            # for ic in c_images:
            #     image = np.asarray(ic)
            #     # image = self.rgb2gray(image)
            #     image = image.reshape(1, IMG_WIDTH * IMG_HEIGHT)
            #     with open(DATASET_FILE, 'ab') as df:
            #         image = np.concatenate((image, np.array([[int(idx)]])), axis=1)
            #         np.savetxt(df, image, delimiter=",", fmt="%d")


if __name__ == "__main__":
    print('Generating dataset...')
    generator = DataGenerator()
    generator.generate_dataset()
    # print('Text Image Dataset is generated:', DATASET_FILE_PATH)
    print('Done!')
