import matplotlib.pyplot as plt
import numpy as np

lots = []
with open("lot_status.txt", "r") as f:
    for line in f:
        lots.append(line.strip().split())

canvas_width = 250
canvas_height = 122

canvas = np.ones((canvas_height, canvas_width, 3)) 

black = (0, 0, 0)
white = (1, 1, 1)
red = (1, 0, 0)

def xywh2edge(x, y, w, h, stat="free"):
    for i in range(max(0, x-w//2), min(x+w//2, 249)):
        canvas[max(0, y-h//2), i] = black
        canvas[min(y+h//2, 121), i] = black
    for j in range(max(0, y-h//2), min(y+h//2, 121)):
        canvas[j, max(0, x-w//2)] = black
        canvas[j, min(x+w//2, 249)] = black

    if stat == "occupied":
        for i in range(max(0, x-w//2), min(x+w//2, 249)):
            for j in range(max(0, y-h//2), min(y+h//2, 121)):
                canvas[j, i] = red

for elem in lots:
    xywh2edge(int(float(elem[1])*250), int(float(elem[2])*122), int(float(elem[3])*250), int(float(elem[4])*122), str(elem[0]))

plt.imshow(canvas)
plt.axis('off') 
# plt.show()
plt.savefig("lot_status.png")