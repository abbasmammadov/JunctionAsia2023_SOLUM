import os
from iou import calculate_iou
# import time

# get real time information from yolov5

yolov5_expts = '../../yolov5/runs/detect' # the path to the yolov5 experiments
sort_by_exp = sorted(os.listdir(yolov5_expts), key=lambda x: int(x[-1]) if x[-1].isnumeric() else 0)
# print('sort_by_exp: ', sort_by_exp)
last_exp = sort_by_exp[-1]

yolov5_folder = os.path.join(yolov5_expts, last_exp, 'labels')
lot_status = 'lot_status.txt'

# for every second, compare the current status with the previous status
# if the current status is the same as the previous status, then it means the car has parked

sort_by_time = sorted(os.listdir(yolov5_folder), key=lambda x: int(x.split('.')[0].split('_')[1]))

tolerence = 1e-3

if len(sort_by_time) > 1:
    # assign the previous status, and the current status
    previous_status, curr_status = sort_by_time[-2:]

    # read the previous status
    with open(os.path.join(yolov5_folder, previous_status), 'r') as f:
        previous_status = f.readlines()
    
    # read the current status
    with open(os.path.join(yolov5_folder, curr_status), 'r') as f:
        curr_status = f.readlines()
    
    previous_status, curr_status = previous_status[0], curr_status[0]
    
    x_cen_prev, y_cen_prev, width_prev, height_prev = previous_status.split(' ')[1:]
    x_cen_curr, y_cen_curr, width_curr, height_curr = curr_status.split(' ')[1:]
        
    # if the difference between the previous status and the current status is less than the tolerence, then it means the car has parked
    if abs(float(x_cen_prev) - float(x_cen_curr)) < tolerence and abs(float(y_cen_prev) - float(y_cen_curr)) < tolerence and abs(float(width_prev) - float(width_curr)) < tolerence and abs(float(height_prev) - float(height_curr)) < tolerence:
        print('The car has parked!')
        lot_status_info = []
        with open(lot_status, 'r') as f:
            lot_status_info.append(f.readlines())

        lot_status_info = lot_status_info[0]
        
        # now calculate the iou between the current status and the lot status
        ious = []
        
        for i, info in enumerate(lot_status_info):
            # print('lot ', i, end = ': ')
            x_cen_lot, y_cen_lot, width_lot, height_lot = info[:-1].split(' ')[1:]
            
            # now calculate the ious between the current status and the lot status
            gt = [float(x_cen_lot), float(y_cen_lot), float(width_lot), float(height_lot)]
            pred = [float(x_cen_curr), float(y_cen_curr), float(width_curr), float(height_curr)]
            
            iou = calculate_iou(gt, pred)
            ious.append(iou)
        
        max_iou = max(ious)
        
        # index of the max iou
        max_iou_index = ious.index(max_iou)
        
        print('original max lot: ', lot_status_info[max_iou_index])
        
        status = lot_status_info[max_iou_index].split(' ')[0]
        
        # update the lot status
        lot_status_info[max_iou_index] = lot_status_info[max_iou_index].replace(status, 'occupied')
        
        # write the updated lot status to the file
        with open(lot_status, 'w') as f:
            f.writelines(lot_status_info)
            print('The lot status has been updated! updated lot:', max_iou_index)
        
    else:
        print('The car has not parked yet!')