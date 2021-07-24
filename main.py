#!/usr/bin/python

import cv2 as cv
import json
import os
import argparse
from scripts.jelly_detector import JellyClassifier
from scripts.objs_and_cols_data import *

def main(image_dir, show_bb):
    result = [0] * 15
    jc = JellyClassifier()

    # loading the image
    img = cv.imread(image_dir)

    # preprocessing
    img_col, img_bw = jc.preprocess_img(img)

    # finding contours of every object on image
    contours, hierarchy = cv.findContours(img_bw, 0, 2)

    # for every contour
    for cnt in contours:
        hull = cv.convexHull(cnt)
        area = cv.contourArea(hull)
        # if contour is reasonable
        if area > 500:
            # image of single object
            s_obj_img = jc.get_single_obj_img(img_col, hull)

            jc.load_single_obj_img(s_obj_img)

            # color of the object
            color = jc.check_color(col_name_list, col_low_list, col_high_list)
            shape = jc.check_shape(hull)

            # only snakes are black and for some reason they can be falsely classified
            if color == 'black':
                shape = 'snake'
            # even_lighter_red is color of snakes, but light_red or dark_red can be confused with it
            if not shape == 'snake' and color == 'even_lighter_red':
                color = 'light_red'
            elif shape == 'snake' and (color == 'light_red' or color == 'dark_red'):
                color = 'even_lighter_red'

            if show_bb:
                jc.add_boundingbox(img_col, cnt, shape, color, hsv_lows, hsv_highs)

            result[class_inds[shape][color]] += 1
    
    if show_bb:
        while True:
            key_code = cv.waitKey(10)
            if key_code == 27:
                break
            cv.imshow('Detected jellies', img_col)

    return result

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Code for detection of different types of jellies')
    parser.add_argument('--input', help='Path to folder with input images', default='./images')
    parser.add_argument('--output', help='Path to output file', default='.')
    parser.add_argument('--show_bb', help='\'n\' to turn off showing images', default=True)
    args = parser.parse_args()

    imgs_dir = args.input
    output_file_dir = args.output
    if args.show_bb == 'n':
        show = False
    else:
        show = True

    results = {}
    for image in os.listdir(imgs_dir):
        result = main(os.path.join(imgs_dir, image), show)
        results[image] = result

    with open(os.path.join(output_file_dir, 'output.json'), 'w') as file:
        json.dump(results, file)
