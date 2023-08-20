# Parking Lot Detection

To achieve good results, we used pre-trained model of YOLOv5. You can find more information on how to use, and set-up the environment from their [github](https://github.com/ultralytics/yolov5).

Fork (clone) their repository and change the "yolov5_folder" in the `demo.py`, and `demo_vid.py` files to your forked or cloned folder path. Then after downloading the necessary checkpoints, you can run the `detect.py` file. 

An example is shown below (for performing real-time detections, and saving results)

`python detect.py --source 0 --weights yolov5s.pt --epochs 300 --save-txt`

