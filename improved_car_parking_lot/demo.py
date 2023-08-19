import os
import threading
import time

interval = 5

def run_detection():
    # change the working directory to yolov5
    yolov5_dir = '../../yolov5'
    os.chdir(yolov5_dir)
    det_cmd = 'python3 detect.py --source 0 --save-txt'
    print('running command: ', det_cmd)
    os.system(det_cmd)

def run_update_status():
    while True:
        # change the working directory to improved_car_parking_lot
        update_dir = '../JunctionAsia2023/improved_car_parking_lot'
        os.chdir(update_dir)
        update_cmd = 'python3 update_status.py'
        print('running command: ', update_cmd)
        os.system(update_cmd)
    # time.sleep(interval)

# Create threads
thread1 = threading.Thread(target=run_detection)
thread2 = threading.Thread(target=run_update_status)

# Start threads
thread1.start()
time.sleep(1)
thread2.start()

# Wait for both threads to finish
thread1.join()
thread2.join()

print("Both processes are done!")