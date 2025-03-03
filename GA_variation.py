#coding=utf-8

####################
#This version is a pure mutation version of the genetic algorithm, without considering crossover.
#The approach is to compute the local optimum, but a local optimum does not necessarily represent the global optimum. Therefore, the final result may not be perfect.
#Note: Since a limited number of chromosomes are used, the rendering effect of the entire image may not be very good. It is recommended to test with a white background image.
####################

import cv2
import numpy as np
import math
import random
import time
import os,sys


#The color channels RGB A are set to be semi-transparent by default.
channels = 2

IMG_SIZE = 100


#The basic pattern of the chromosome has several corners.
unit_shape_points = 3

#The number of chromosome
unit_num = 100

class shell():
    iter_num = 0
    target_img = None

    def __init__(self):
        self.fitness = 0
        
        #init basic pattern of the chromosome
        self.unit_points = np.random.randint(0,IMG_SIZE,(unit_num,unit_shape_points, 2))
        
        #init color
        self.unit_channels = np.random.randint(0,256,(unit_num,channels))

    # Draw each chromosome separately.
    def draw_whole_unit(self):
        self.units = np.full((unit_num,IMG_SIZE,IMG_SIZE,channels), 0)
        for i in range(unit_num):
            cv2.fillPoly(self.units[i],[self.unit_points[i]],tuple(self.unit_channels[i].tolist()))

    # combine chromosome
    def draw(self):
        #background_color is white
        self.img = np.full((IMG_SIZE,IMG_SIZE,channels-1), 255)
        for i in range(unit_num):
            alpha = self.units[i,:,:,-1]/255.0
            alpha = np.array([alpha])
            alpha = np.swapaxes(alpha,0,1)
            alpha = np.swapaxes(alpha,1,2)
            self.img[:,:,:channels-1] = self.units[i,:,:,:channels-1]*alpha + self.img[:,:,:channels-1]*(np.ones(alpha.shape) - alpha)
        
    
    def fast_draw(self, unit_list):
        img = np.full((IMG_SIZE,IMG_SIZE,channels-1), 255)
        for unit in unit_list:
            alpha = unit[:,:,-1]/255.0
            alpha = np.array([alpha])
            alpha = np.swapaxes(alpha,0,1)
            alpha = np.swapaxes(alpha,1,2)
            img[:,:,:channels-1] = unit[:,:,:channels-1]*alpha + img[:,:,:channels-1]*(np.ones(alpha.shape) - alpha)
        return img


    #####calculate fitness#####
    def fit(self, img = None):
        if img is None:
            compare_img = self.img
        else:
            compare_img = img
        sub = (self.target_img - compare_img).astype(np.int64)
        sum_ = np.sum(sub*sub)
        fitness = np.sqrt(sum_)
        return fitness

    #var_rate is a descending order list [var1,var2,var3,...]
    def variation(self):
        var_rate_list=[0.3,0.1,0.05,0.03,0.02,0.01,0.01]
        iter_list=[-1,50,100,200,400,600,800]

        for i in range(len(var_rate_list)-1,-1,-1):
            if self.iter_num > iter_list[i]:
                var_rate = var_rate_list[i]
                break
                
        var_num = int(unit_num * var_rate)
        random_list = random.sample(range(unit_num),var_num)
        
        
        for iter in range(10):
            change_unit_points = self.unit_points.copy()
            change_unit_channels = self.unit_channels.copy()
            change_units = self.units.copy()
            for i in random_list:
                if var_rate == var_rate_list[-3]:
                    change_unit_points[i] = self.var_points(i,15)
                    change_unit_channels[i] = self.var_color(i,30)
                elif var_rate == var_rate_list[-2]:
                    change_unit_points[i] = self.var_points(i,5)
                    change_unit_channels[i] = self.var_color(i,15)
                elif var_rate == var_rate_list[-1]:
                    change_unit_points[i] = self.var_points_ac(i,5)
                    change_unit_channels[i] = self.var_color_ac(i,15)
                else:
                    change_unit_points[i] = np.random.randint(0,IMG_SIZE,(unit_shape_points,2))
                    change_unit_channels[i] = np.random.randint(0,255,(channels))

                change_units[i] = np.zeros((IMG_SIZE,IMG_SIZE,channels))
                cv2.fillPoly(change_units[i],[change_unit_points[i]],tuple(change_unit_channels[i].tolist()))
            
            img = self.fast_draw(change_units)
            fitness_ = self.fit(img)
            if fitness_ < self.fitness:
                self.fitness = fitness_
                self.img = img
                for i in random_list:
                    self.unit_points[i] = change_unit_points[i]
                    self.unit_channels[i] = change_unit_channels[i]
                    self.units[i] = change_units[i]
                break


    def var(var_rate):
       return True if random.random() > var_rate else False

    def var_points(self, ele, val):
        point = np.zeros((unit_shape_points, 2))
        for i in range(unit_shape_points):
            point[i] = np.array([min(max(0,np.random.randint(-val,val)+self.unit_points[ele][i][0]),IMG_SIZE), min(max(0,np.random.randint(-val,val)+self.unit_points[ele][i][1]),IMG_SIZE)])
        return point

    def var_color(self, ele, val):
        channel = np.zeros((channels))
        for i in range(channels):
            channel[i] = min(max(0,np.random.randint(-val,val)+self.unit_channels[ele][i]),255)
        return channel

    def var_points_ac(self,ele,val):
        point = self.unit_points[ele].copy()
        i = random.sample(range(unit_shape_points),1)[0]
        point[ele][i][0] = min(max(0,np.random.randint(-val,val)+point[ele][i][0]),IMG_SIZE)
        point[ele][i][1] = min(max(0,np.random.randint(-val,val)+point[ele][i][1]),IMG_SIZE)
        return point

    def var_color_ac(self,ele,val):
        channel = np.zeros((channels))
        if var(0.3):
            for i in range(channels):
                channel[i] = min(max(0,np.random.randint(-val,val)+self.unit_channels[ele][i]),255)
        return channel


    def target_format(self, target_img):
        if target_img.shape[:2] != (IMG_SIZE,IMG_SIZE):
            target_img = cv2.resize(target_img,(IMG_SIZE,IMG_SIZE))

        if channels == 2:
            if not target_img.shape[-1] == 1:
                target_img = cv2.cvtColor(target_img,cv2.COLOR_BGR2GRAY)
                target_img = np.array([target_img])
                target_img = np.swapaxes(target_img,0,1)
                target_img = np.swapaxes(target_img,1,2)
        elif not channels == 4:
            try:
                sys.exit(0)
            except:
                print('wrong channels')

        if not self.img.shape == target_img.shape:
            try:
                sys.exit(0)
            except:
                print('target shape not match')
        self.target_img = target_img


def target_channels(target_img):
    global channels
    #RGB or GRAY
    h = int(target_img.shape[0] / 2)
    for w in range(target_img.shape[1]):
        if not (target_img[h][w][0] == target_img[h][w][1] and target_img[h][w][0] == target_img[h][w][2]):
            channels = 4
            break

def main():
    img = cv2.imread("./target.jpg")
    target_channels(img)
    Shell_1 = shell()
    Shell_1.draw_whole_unit()
    Shell_1.draw()
    Shell_1.target_format(img)
    Shell_1.fitness = Shell_1.fit()
    
    dirpath = "./target"
    
    if not os.path.exists(dirpath):
        os.mkdir(dirpath)

    for i in range(100001):
        shell.iter_num += 1
        Shell_1.variation()
        #windows cls
        os.system('cls')
        #linux clear
        #os.system('clear')
        print(i)
        print(Shell_1.fitness)
        if i % 100 == 0:
            img_name = os.path.join(dirpath, str(i) + '_' + str(int(Shell_1.fitness)) + ".jpg")
            cv2.imwrite(img_name,Shell_1.img)

if __name__ == "__main__":
    main()




