import pandas as pd
import os
import cv2 as cv
import numpy as np


class EvaluationImages:
    def __init__(self, resize=(750, 450)):
        self.resize = resize

    @staticmethod
    def count_number_images(path):
        false_img = []
        true_img = []
        true_img_front = []
        true_img_back = []
        false_img_front = []
        false_img_back = []
        for folder in os.listdir(path):
            print(f'Reading {folder} \n --------------------------')
            if 'false' in folder:
                false_path = os.path.join(path, folder)
                for file_img_false in os.listdir(false_path):
                    if 'front' in file_img_false:
                        false_img_front.append(file_img_false)
                    else:
                        false_img_back.append(file_img_false)
                false_img = false_img_front + false_img_back
                print(f'Number false images front = {len(false_img_front)} image \n'
                      f'Number false images back = {len(false_img_back)} image \n'
                      f'Total number false images = {len(false_img)} image \n')

            if 'true' in folder:
                false_path = os.path.join(path, folder)
                for file_img_true in os.listdir(false_path):
                    if 'front' in file_img_true:
                        true_img_front.append(file_img_true)
                    else:
                        true_img_back.append(file_img_true)
                true_img = true_img_front + true_img_back
                print(f'Number true images front = {len(true_img_front)} image \n'
                      f'Number true images back = {len(true_img_front)} image \n'
                      f'Total number true images = {len(true_img)} image \n')
        return true_img, false_img

    def combine_two_images(self, path_img1, path_img2):
        img1 = cv.imread(path_img1)
        img1 = cv.resize(img1, dsize=self.resize)
        img2 = cv.imread(path_img2)
        img2 = cv.resize(img2, dsize=self.resize)
        combined_image = np.concatenate((img1, img2), axis=0)
        return combined_image

    def compare_two_version(self, path1, path2, ft1, ft2):
        path_save1 = 'output/compare_true_' + path1 + '_' + path2
        os.mkdir(path_save1)
        out1 = list(set(ft1) - set(ft2))
        for image in out1:
            path_image1 = path1 + '/' + path1 + '_true_images/' + image
            path_image2 = path2 + '/' + path2 + '_false_images/' + image
            combined_image = self.combine_two_images(path_image1, path_image2)
            cv.putText(combined_image,
                       text=path1,
                       org=(self.resize[0]//2, self.resize[1]*2//80),
                       fontFace=cv.FONT_HERSHEY_COMPLEX,
                       fontScale=0.75,
                       color=(0, 0, 225))
            cv.putText(combined_image,
                       text=path2,
                       org=(self.resize[0]//2, self.resize[1]*2//2),
                       fontFace=cv.FONT_HERSHEY_COMPLEX,
                       fontScale=0.75,
                       color=(0, 0, 225))
            cv.imwrite(path_save1 + '/' + image, combined_image)


if __name__ == '__main__':
    version_path_1 = 'V2.5.0'
    version_path_2 = 'V2.5.1'
    Class = EvaluationImages()
    true_img1, _ = Class.count_number_images(version_path_1)
    true_img2, _ = Class.count_number_images(version_path_2)
    Class.compare_two_version(version_path_1, version_path_2, true_img1, true_img2)
    Class.compare_two_version(version_path_2, version_path_1, true_img2, true_img1)
