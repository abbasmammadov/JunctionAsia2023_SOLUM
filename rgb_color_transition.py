import numpy as np
import matplotlib.pyplot as plt
from  PIL import Image
import colorsys


black = (0, 0, 0)
red = (255, 0, 0)
yellow = (255, 255, 0)
white = (255, 255, 255)

list_color = [black, red, yellow, white]

def brute_force(img):
    new_img = img.copy()
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            compare = [img[i, j] - black, img[i, j] - red, img[i, j] - yellow, img[i, j] - white]
            compare = [np.sum(np.square(compare[0])), 
                       np.sum(np.square(compare[1])), 
                       np.sum(np.square(compare[2])),
                       np.sum(np.square(compare[3]))]
            new_img[i, j] = list_color[np.argmin(compare)]
    return new_img



def use_hsv(img):
    new_img = img.copy()
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            hsv = colorsys.rgb_to_hsv(img[i, j][0], img[i, j][1], img[i, j][2])
            hsv = list(hsv)
            hsv[2] /= 255.0

            if hsv[2] < 0.35:
                new_img[i, j] = black
            elif hsv[0] < 0.1:
                new_img[i, j] = red
            elif hsv[0] < 0.15:
                new_img[i, j] = yellow
            else:
                new_img[i, j] = white
    return new_img



def visualize(img):
    img = Image.open(img)
    img = np.array(img)
    img = brute_force(img)
    # img = use_hsv(img)
    plt.imshow(img)
    plt.show()
    


visualize("/Users/abbasmammadov/Desktop/code/good3.jpeg")