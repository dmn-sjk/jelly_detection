import cv2 as cv
import numpy as np

class JellyClassifier:
    def __init__(self):
        self.single_obj_img = None
    
    def load_single_obj_img(self, img):
        self.single_obj_img = img

    @staticmethod
    def preprocess_img(img_bgr):
        img_bgr = cv.resize(img_bgr, (800, 800))
        img_col = np.copy(img_bgr)

        img_bw = cv.medianBlur(img_bgr, 7)
        img_bw = cv.Canny(img_bw, 37, 181)

        kernel = np.ones((2, 2), np.uint8)
        img_bw = cv.morphologyEx(img_bw, cv.MORPH_GRADIENT, kernel)

        return img_col, img_bw

    @staticmethod
    def get_single_obj_img(img_col, cnt):
        img_gray = cv.cvtColor(img_col, cv.COLOR_BGR2GRAY)
        mask = np.zeros_like(img_gray) 
        cv.drawContours(mask, [cnt], 0, 255, -1) 
        s_obj_img = np.full(img_col.shape, 255, dtype=np.uint8)
        s_obj_img = cv.bitwise_and(img_col, img_col, mask=mask)

        (y, x) = np.where(mask == 255)
        top_x = np.min(x)
        top_y = np.min(y)
        bottom_x = np.max(x)
        bottom_y = np.max(y)

        s_obj_img = s_obj_img[top_y:bottom_y+1, top_x:bottom_x+1]
        s_obj_img[s_obj_img == 0] = 255

        return s_obj_img

    @staticmethod
    def snake(cnt, thr_perimeter):
        perimeter = cv.arcLength(cnt, True)
        if perimeter > thr_perimeter: 
            return True
        return False

    def circle(self, cnt, diff, scnd_diff):
        rect = cv.minAreaRect(cnt)
        w, h = rect[1]
        aspect_ratio = w / h

        if 1 - diff < aspect_ratio < 1 + diff:  
            return True
        elif 1 - scnd_diff < aspect_ratio < 1 + scnd_diff:
            img_col = np.copy(self.single_obj_img)
            img_col = cv.medianBlur(img_col, 5)
            img_gray = cv.cvtColor(img_col, cv.COLOR_BGR2GRAY)

            circles = cv.HoughCircles(img_gray, cv.HOUGH_GRADIENT, 3, 50,
                                    param1=90, param2=45,
                                    minRadius=20, maxRadius=100)
            if circles is not None:
                return True
        return False

    def check_color(self, col_name_list, col_low_list, col_high_list):
        img_hsv = cv.cvtColor(self.single_obj_img, cv.COLOR_BGR2HSV)
        best_area = 0
        best_col_ind = 0
        # for every color
        for j in range(len(col_name_list)):
            img_col = cv.inRange(img_hsv, col_low_list[j], col_high_list[j])
            kernel = np.ones((3, 3), np.uint8)
            img_col = cv.erode(img_col, kernel, iterations=1)
            kernel = np.ones((5, 5), np.uint8)
            img_col = cv.dilate(img_col, kernel, iterations=3)
            contours, hierarchy = cv.findContours(img_col, 1, 2)

            # for every contour on single color image
            for cnt in contours:
                area = cv.contourArea(cnt)
                if area < 550:
                    continue
                elif best_area < area:
                    best_area = area
                    best_col_ind = j

        if best_area == 0: # whites
            return 'white'
        else: # others
            return col_name_list[best_col_ind]

    def check_shape(self, cnt, snake_thr_per=195, crcl_diff=0.25, scnd_crcl_diff=0.45):
        if self.snake(cnt, snake_thr_per):
            return 'snake'
        elif self.circle(cnt, crcl_diff, scnd_crcl_diff):
            return 'circle'
        else:
            return 'bear'

    @staticmethod
    def add_boundingbox(img, contour, shape, color, hsv_lows, hsv_highs):
        (x, y, w, h) = cv.boundingRect(contour)
        if color == 'white':
            col = (255, 255, 255)
        else:
            col_mean = (np.array(hsv_lows[color]) + np.array(hsv_highs[color])) / 2
            col_mean = np.uint8([[col_mean]])

            col = cv.cvtColor(col_mean, cv.COLOR_HSV2RGB).reshape(-1)
            # for some reason color values passed to cv.rectangle() func has to be int, not numpy.int
            col = (int(col[0]), int(col[1]), int(col[2]))
        
        cv.rectangle(img, (x, y), (x + w, y + h), col, 3)
        cv.putText(img, shape, (x, y - 7), cv.FONT_HERSHEY_SIMPLEX, 0.6, col, 2)
