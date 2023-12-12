# Night Walker Robot: Object Detection and Autonomous Navigation



## Overview

Welcome to the Night Walker Robot project! This repository contains the code and resources for a robot equipped with a machine learning model for [object detection](https://docs.viam.com/ml/vision/detection/#configure-an-mlmodel-detector). The Night Walker Robot is designed to navigate and explore environments autonomously, especially in low-light conditions.



## Features

- **Object Detection:** The robot is equipped with a state-of-the-art machine learning model for object detection, enabling it to identify and classify various objects in its surroundings.
- **Autonomous Navigation:** Using the information gathered from the object detection model, the Night Walker Robot autonomously navigates through its environment, making informed decisions to avoid obstacles and reach its destination.
- **Low-Light Capabilities:** The robot is optimized for low-light conditions, making it suitable for tasks in environments with limited visibility.



## ML model in Viam `mlmodel`

For this project, we used pre-trained object detection model with [TensorFlow Lite ML](https://www.tensorflow.org/lite). More specific details about integration with **Raspberry Pi** may be found [here](https://github.com/tensorflow/examples/tree/master/lite/examples/object_detection/raspberry_pi).

### Dataset Collection

By capturing the dataset from the transformer camera module, we are able to gather a large amount of images of runway of the track to label the objects. For better recognition of object, we put several green sticky notes for better visibility of objects:

![dataset](imgs\dataset.png)

### Updating/Training Model 

After setting up certain datasets and bounding boxes for different objects, we need to update the training model from **TensorFlow Lite** with respect to our dataset. What we got from the updated `obj-det.tflite` is essential for our **Autonomous Navigation**.

![trained_model](imgs\trained_model.png)

### Model Deployment and Service Configuration

After the ML model is properly trained with sufficient dataset, we may use viam's **vision service** as a **ml model detector**. More specific steps may be found [here](https://docs.viam.com/ml/).



## Demo Video

<video src="E:\Github\night-walker\videos\video.mp4"></video>



## Limitations

The Night Walker Robot excels in low-light object detection and autonomous navigation, leveraging a TensorFlow Lite ML model. However, in extremely dark conditions, the precision of object boundaries may diminish. The model's performance is optimized with green sticky note markers, enhancing visibility; without them, object detection accuracy may decrease. The robot may encounter challenges in adapting to real-time environmental changes and operates within resource constraints on the Raspberry Pi. While it demonstrates advanced capabilities, these limitations underscore the need for continued refinement and consideration of specific deployment scenarios.
