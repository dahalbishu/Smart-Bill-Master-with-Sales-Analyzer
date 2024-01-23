# Smart Bill Master with Sales Analyzer System
# Abstract
Smart Bill Master with Sales Analyzer system has been developed to streamline the
process of creating bills and recording data in a database. The system consists of a
conveyor belt that moves when a touch button is pressed, multiple products with their
own unique QR codes are placed on the moving platform. The QR codes are scanned
using a camera and detected through image processing. The system shows the bill with
the product’s name, product id, and price on a digital screen. The system also alerts
users when a product's expiry date has passed. Data from the QR codes is recorded in
the database for sales and profit analysis, which can be viewed through plotted graphs.
Customers registered in the database receive a PDF of their bill via email. Object
detection algorithms are used to ensure all QR codes are scanned, and YOLOv8 model
with DeepSORT algorithm is used for object tracking. Thus, we obtain a real time,
automatic billing system through collaboration between hardware and software.

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

Expiry Date Alerts: Users receive alerts when a product's expiry date has passed.

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

4. Install the required dependencies:

    ```bash
    pip install -e '.[dev]'
    ```

## Dataset

Download the dataset from the provided [YOLOv8-DeepSORT Dataset Google Drive link]( https://drive.google.com/drive/folders/1zYtoQVUe5BzWOrYn7ZpevUNd-alyM4oL ).

Organize the dataset as follows:

- Change to the YOLOv8 detection directory:

    ```bash
    cd ./YOLOv8-DeepSORT-Object-Tracking/ultralytics/yolo/v8/detect
    ```

- Download the 'detection-1' folder from the Google Drive link.

- Place the downloaded 'detection-1' folder into the following directory.

## Training

To train the YOLOv8 model for object detection, follow these steps:

1. Run the training script:

    ```bash
    python train.py model=yolov8l.pt data="detection-1/data.yaml" epochs=50 imgsz=640 batch=8
    ```

   Adjust the parameters as needed for your specific use case.

## Prediction

For predicting on videos using the trained model, use the following command:

   ```bash
   python predict.py model='best.pt' source='vid.mp4'
   ```

Replace 'best.pt' with the path to your trained model weights file and 'vid.mp4' with the path to the input video file.

Feel free to explore and customize the codebase according to your requirements. If you encounter any issues or have questions, refer to the documentation or seek assistance from the community.



----------------------------------------------------------------------------------------------------------------------------------------------

# Demo Video
You can find a demo video of the system ( https://drive.google.com/drive/folders/1zYtoQVUe5BzWOrYn7ZpevUNd-alyM4oL ).

# Contributors
1. Apsara Shrestha
2. Bishwambhar Dahal
3. Sirjana Bhatta
4. Sujana Acharya

# Acknowledgments
We would like to thank Institute of Engineering (IOE) for the inclusion of Minor
Project on the syllabus for the course Bachelor in Electronics, Communication and
Information Engineering.
Also, we would like to thank Department of Electronics and Computer Engineering,
Thapathali Campus for providing us the guidance, and wonderful learning
environment. We would also like to thank our supervisor Er. Praches Acharya for
continuous guidance and encouragement

