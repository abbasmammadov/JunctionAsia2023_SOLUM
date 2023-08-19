import os
import threading
import time

# interval = 5

def run_detection(video_dir):
    # change the working directory to yolov5
    yolov5_dir = '../../yolov5'
    os.chdir(yolov5_dir)
    det_cmd = f'python3 detect.py --source {video_dir} --save-txt'
    print('running command: ', det_cmd)
    os.system(det_cmd)

def run_update_status():
    
    # change the working directory to improved_car_parking_lot
    update_dir = '../JunctionAsia2023/improved_car_parking_lot'
    os.chdir(update_dir)
    update_cmd = 'python3 update_status.py'
    print('running command: ', update_cmd)
    os.system(update_cmd)
    # time.sleep(interval)

video_dir = "video.mp4"
run_detection(video_dir)
run_update_status()
os.command('python3 txt2screen.py')
# # Start threads
# thread1.start()
# time.sleep(1)
# thread2.start()

# # Wait for both threads to finish
# thread1.join()
# thread2.join()

print("Both processes are done!")