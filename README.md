# JunctionAsia2023_SOLUM

Junction Asia 2023 hackathon

The aim of the project is to improve usefullness of the Electronic Shelf Label (ESL). For that we have developed software covering several use cases.

webpage_qr directory

First part of the project exploits the marketing capabilities of the ESL. The price tags put on the items in the supermarket are usually static even when they are implemented using ESL. We want to utilize the dynamically changable property of ESL to suggest users other similar products or capture their attention to discounts
and special offers or ongoing events.

We generate specifically designed labels in the first part of the project. "esl_templates" directory contains the generated images for each label we will be projecting to the device. Label mainly consists of price, picture of the suggested product, and the QR leading to a informative website containing detailed product information and discounted products list.

"qr_code_generation" directory hosts the scripts that convert the information website url to QR code that will be put on product labels. In addition it contains directory containing the said QR code images.

Complete labels that be put on the devices are located in "esl_templates" directory.

The informative website generation code is located in "templates directory"

"owner" directory consists of python scripts running the alghorthms to predict future sales as well give retailers an idea of items relevant to give item.

"upload_image.py" scripts is the main alghorithm that helps us direct the final generated labels to the ESL's LED screen.

we used SOLUM's POST api to upload image to ESL's LED screen. It can upload images to different devices at the same time, and it supports png, jpeg, and jpg image formats. Since device's screen size can vary we resize our images before uploading to device.

Here are the major areas where we applied machine learning for getting the most out of the device for both customers and owners

  * For Owners, We used time series forcasting models to perform accurate prediction of the future sales of products, in specified stores. However, besides machine learning, we also generated deterministic recommendations to help owners decide on items.

* For Customers, Using word2vector models, we calculated semantic similarity of goods so that we can recommend related products for our customers. 

* In addition to the above use-cases, we also leveraged the device so that it can accurately track, and lead customers to empty parking lots using Object detection algorithms which are used to detect cars. For details on how to run our object detection model: please visit the following [README](https://github.com/abbasmammadov/JunctionAsia2023_SOLUM/blob/main/improved_car_parking_lot/README.md).


Under the root directory
```bash
python webpage_qr/app.py <local-ip-address> 
```
This makes the following websites active:
http://local-ip-address:5000/owner
http://local-ip-address:5000/esl1
http://local-ip-address:5000/esl2
http://local-ip-address:5000/esl3
These are accessed from the corresponding QR codes.
