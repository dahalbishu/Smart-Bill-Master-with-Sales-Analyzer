# Smart Bill Master with Sales Analyzer System
This research has been published under the title *Automated Retail Billing: Streamlining Checkout with QR Codes and Object Tracking Using YOLOv8 and DeepSORT* in the **International Journal of Science, Engineering and Technology**, Volume 12, Issue 5. The publication can be accessed [here](https://www.ijset.in/wp-content/uploads/IJSET_V12_issue5_747.pdf), and the DOI is [10.61463/ijset.vol.12.issue5.253](https://doi.org/10.61463/ijset.vol.12.issue5.253).

# Abstract
In the contemporary retail landscape, long checkout queues and the issuance of expired products
present significant challenges to operational efficiency. To address these issues and enhance the billing process,
we propose an innovative solution that automates billing while effectively managing sales data. Our system
features a conveyor belt mechanism activated by a touch sensor, where products, each with unique QR codes,
are placed. A camera captures live video of the conveyor belt, enabling real-time detection and decoding of
these QR codes, along with immediate alerts for any expired products identified. The system generates a
comprehensive bill detailing product names, IDs, and prices, while securely storing scanned data in a database
for in-depth sales and profit analysis, complemented by graphical visualizations. Registered customers receive a
PDF copy of their bill via email through the Simple Mail Transfer Protocol (SMTP), enhancing their overall
experience. By employing the You Only Look Once version 8 (YOLOv8) model alongside the Deep Simple Online
and Realtime Tracking (DeepSORT) algorithm, the system ensures precise object tracking and accurate
scanning of each product. The Raspberry Pi serves as the core component of the system, managing the
integration of advanced hardware and software. This solution significantly improves the efficiency and
accuracy of the billing process, offering a holistic approach to modern retail management.


# Getting Started

## Prerequisites
1. Raspberry Pi
2. Motor Driver – L298N
3. DC Motor
4. Piezo Active Buzzer
5. Webcam
6. Touch Sensor
7. Led Light 


## Pin Configuration for Raspberry Pi
- `ses` (pin 37): Touch sensor input.
- `in1` (pin 3) and `in2` (pin 5): Motor control pins for the L298N motor driver.
- `in3` (pin 11) and `in4` (pin 13): LED control pins for the L298N motor driver.
- `buzz` (pin 15): Buzzer output.

- Connect all ground (GND) wires to the ground pin of the Raspberry Pi to establish a common ground reference.


**Note:** You can change the pin configuration as required. If you make changes, ensure to update the pin descriptions in the `main.py` configuration accordingly. Default pin configurations are already present in the `main.py` script.

**Note:** The LED bulb is connected to the motor driver to provide higher voltage, as the Raspberry Pi output voltage is limited.

## GPIO Setup
1. Set GPIO mode to use physical pin numbering on the Raspberry Pi (GPIO.BOARD).
2. Configure pins as follows:
   - `ses` is set as input.
   - `in1` and `in2` are set as output for motor control.
   - `in3` and `in4` are set as output for LED control.
   - `buzz` is set as output for the buzzer.
   
## Motor Driver Configuration
- **OUT1 and OUT2:** Used to drive the DC gear motor.
- **OUT3 and OUT4:** Used to control the LED light.
- OUT3 is connected to the positive terminal of the LED bulb.
- OUT4 is connected to the negative terminal of the LED bulb.


## Webcam Connection:
- Connect the webcam to one of the USB ports on the Raspberry Pi.

Ensure that the webcam is recognized by the Raspberry Pi and is accessible for video capture in the `main.py` script.

## Accessing Remote Database

To enable the Raspberry Pi to access a remote database hosted on a laptop, the following steps are required:

1. Open the 'my.ini' configuration file of the MySQL server on the laptop.

2. Add the following line in the `[mysqld]` section of the 'my.ini' file:
    ```ini
    bind-address = 0.0.0.0
    ```
   This setting allows remote connections to the server's database from any IP address.

3. Save the 'my.ini' file and restart the MySQL server to apply the changes.

4. Grant privileges to the Raspberry Pi's IP address to connect to the database. Execute the following commands in the MySQL shell on the laptop:

    ```sql
    CREATE USER 'app'@'192.168.1.116' IDENTIFIED BY 'password';
    GRANT ALL PRIVILEGES ON *.* TO 'app'@'192.168.1.116';
    ```
   In the above commands, '192.168.1.116' represents the IP address of the Raspberry Pi. Adjust it based on the actual IP address of your Raspberry Pi.

   Replace 'password' with a strong and secure password for the 'app' user.

These steps allow the Raspberry Pi to establish a remote connection to the database hosted on the laptop. Ensure that the firewall settings on the laptop allow incoming connections on the MySQL port (default is 3306) for successful communication.


## Database Setup
Run the provided SQL script ourshoppingcenter.sql to create the necessary database.

## Software Dependencies
Install required Python libraries:
pyzbar
opencv-python
smtplib
FPDF
tkinter
num2words
and other some libraries

## Hardware Connection
Connect Raspberry Pi with the motor driver, DC motor, piezo buzzer, webcam, and touch sensor in the proper configuration.

## Running the System
Open a Python IDE on the Raspberry Pi.
Run main.py to start the system.

## Running Sales Analysis
To analyze sales data, use the `salesanalysis_final.py` script. This script processes the recorded sales and profit data stored in the database, providing insightful graphical analysis.



## Features
Automatic Billing: The system automates the billing process through the conveyor belt, touch button, and QR code scanning.

Digital Screen Display: The bill with product details and prices is displayed on a digital screen.

Expiry Date Alerts: Users receive alerts when a product’s expiry date has passed.

Sales Data Analysis: Sales and profit data are recorded in the database, and graphical analysis can be viewed through plotted graphs.

Customer Email: Registered customers receive a PDF of their bill via email.

Object Detection: Object detection algorithms ensure all QR codes are scanned accurately.

Real-time Billing: The collaboration between hardware and software components enables a real-time billing system.

## Troubleshooting
In case of issues, check the hardware connections and ensure all dependencies are installed.



-------------------------------------------------------------------------------------------------------------------------------
# YOLOv8-DeepSORT Object Tracking - Smart Bill Master with Sales Analyzer

## Installation

To set up the environment, follow these steps:

1. Create a Conda environment with Python 3.9:

    ```bash
    conda create --name billmaster python=3.9
    ```

2. Activate the Conda environment:

    ```bash
    conda activate billmaster
    ```

3. Navigate to the project directory:

    ```bash
    cd path/to/YOLOv8-DeepSORT-Object-Tracking
    ```
4. For GPU support (Optional): 

   ```bash
   conda install pytorch torchvision torchaudio pytorch-cuda=12.4 -c pytorch -c nvidia
   ```

5. Install the required dependencies:

    ```bash
    pip install -e .
    ```

## Dataset

Download the dataset from the provided [here](https://drive.google.com/drive/folders/13R2yus7L8AjsEkIGYPs52fH0dBwGeijf?usp=drive_link).

Organize the dataset as follows:

- Change to the YOLOv8 detection directory:

    ```bash
    cd ./ultralytics/yolo/v8/detect
    ```

- Download the 'detection-1' folder from the provided link.

- Place the downloaded 'detection-1' folder into the following directory.

## Training

To train the YOLOv8 model for object detection, follow these steps:

1. Run the training script:

    ```bash
    python train.py model=yolov8l.pt data="detection-1/data.yaml" epochs=50 imgsz=640 batch=8
    ```

   Adjust the parameters as needed for your specific use case.

## Model Performance
The model achieved the following performance on the validation set:

| Metric        | Value  |
|---------------|--------|
| Precision     | 0.973  |
| Recall        | 0.972  |
| mAP@50        | 0.99   |
| mAP@50-95     | 0.873  |

## Download Model Weights

You can download the pre-trained model weights from [here](https://drive.google.com/drive/folders/1a0R1WCcFqSIqC0mbEcDaUJeKTJefsi9T?usp=drive_link)

## Prediction

For predicting on videos using the trained model, use the following command:

   ```bash
   python predict.py model='best.pt' source='vid.mp4'
   ```

Replace 'best.pt' with the path to your trained model weights file and 'vid.mp4' with the path to the input video file.

Feel free to explore and customize the codebase according to your requirements. If you encounter any issues or have questions, refer to the documentation or seek assistance from the community.



----------------------------------------------------------------------------------------------------------------------------------------------

# Demo Video
You can find a demo video of the system [here](https://drive.google.com/file/d/1Nx5U0XAAnP2LRwvy6ZQsLpdIsvvsCjZC/view?usp=drive_link).

# Contributors
1. Bishwambhar Dahal 
2. Sirjana Bhatta
3. Sujana Acharya
4. Apsara Shrestha
5. Praches Acharya

# Acknowledgments
We would like to express our sincere gratitude to our supervisor, Er. Praches Acharya, for his invaluable guidance throughout this research. We also extend our heartfelt thanks to the Department of Electronics and Computer Engineering at Thapathali Campus for providing us with the resources and a conducive environment that greatly contributed to the success of this research.
Also, we would like to thank Department of Electronics and Computer Engineering,
Thapathali Campus for providing us the guidance, and wonderful learning
environment.

