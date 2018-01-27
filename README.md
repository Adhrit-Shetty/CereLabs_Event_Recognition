# Cerelabs Internship - Event Recognition System
### Brief Description:
1. The main goal of the event recognition system is to incorporate as many features with respect to an event in a work environment which can be detected via cctv feeds of that work environment
2. An event is defined as an occurance in that work environment which affects the security in any manner. This occurance can be of any variety such as as intruder in the work place, a previously dynamic but currently static object detection, line crossing into sensitive regions of the work place  and many more
3. Based on the risk that the event poses we can carry inform the users of the system and they can carry out the appropriate actions
4. Once an event occurs and is detected via the system it is recorder for further review
  
### Components:
The system as it stands has these components:
1. ##### Cameras:
   * The system can accept rtsp links to add camera feeds for monitoring
   * The cameras have details associated with it in order such as the room it is located in, resolution etc in order to get better understanding of how all the cameras fit together to form the system
   * Cameras can be added and removed from the system via the interfaces created for these functionalities
2. ##### Rooms:
   * A room is a location in the workspace
   * It has it's own set of privileges and restrictions associated with it i.e. each room can have a security clearance level and should be accessed only by employees having the same or greater clearance level.
   * Any event detected via a camera in a particular room is tagged and stored with room details to help the users of the system understand the level of security threat that the workplace is facing
   * Rooms can be added and removed from the system via the interfaces created for these functionalities
3. ##### Employees:
   * An employee is a person who is associated with the workspace in any manner and is authorized to be detected within the region being monitored by the system
   * Each employee has a clearance level associated with him/her and based on this he/she can be labelled as authorized or unauthorized in a particular room
   * Each employee has a set of images associated with him/her which will be used to classify him/her on being detected
   * Employees can be added and removed from the system via the interfaces created for these functionalities
4. ##### Administrator (Admin):
   * An administrator is an employee who is given the responsibility of monitoring the system and are notified of the events that are detected via the system
   * Usually the administator should be an employee of the security department as he/she can carry out reqired actions based on the level of risk detected via the system
   * Administators can be added and removed from the system via the interfaces created for these functionalities
5. ##### Events:
   * An event has already been defined in the earlier section
   * Each event has a video stored which shows the event occuring and can be played later when required for review or any other purpose
   * Each event has a risk level associated with it
   * Events can be added and removed from the system via the interfaces created for these functionalities

### Implenetation details:
   * The system is made in Python3.5+
   * It makes use of Flask to create the server and Jinja2 to create the templates for the pages
   * It uses websockets to stream the video to the output page

### File and Folder Description:
   * ##### Batch Represent/
      It stores the lua files which are used to create features from the aligned images 
   * ##### Openface/
     Stores the files required by the openface face detection system
   * ##### System/
      * **static :** The CSS, bootstrap and JavaScript files used while rendering the pages are stored in this folder
      * **templates :** The Jinja2 templates for the different pages are stored here
      * **aligndlib.py :** Here the faces captured are aligned for better detection
      * **Camera.py :** Stores all the data related to the cctv cameras that are added to the system. It has the functionality to get frames from the video stream and processes the frames
      * **FaceDetector.py :** Implements Dlib's HOG based face detector to detect faces
      * **FaceRecogniser.py :** Implements LightGBM to classify detected faces using the faces that the model has already been trained with. It also has functionality for training with new faces
      * **ImageUtils.py :** Carries out all the image pre-processing that occurs before an image is used for detecting and infering faces
      * **MotionDetecor.py :** It is used to track the motion of detected objects by constructing background models by frame filtering and averaging
      * **SQLFunctions.py :** An helper function which contains simple and reusable code for database related functionalities
      * **SurveillanceSystem.py :** It is the main file which provides all the central proccessing and ties everything together. It has all the functionality to add and remove cameras, start processing frames, check for events etc
    together.
      * **WebApp.py :** It is the Flask server file and has all the functions related to the web application
  
### Events:
1. ##### Intuder detection via face recognition: 
   * 

### Pipeline:
![Pipeline](https://github.com/AkshatShetty101/CereLabs_Event_Recognition/blob/master/Pipeline.png)

### Enterprise Resource Diagram:
![Enterprise Resource Diagram](https://github.com/AkshatShetty101/CereLabs_Event_Recognition/blob/master/ERD.png)

### Use-Case
To be added soon...
      
### Prerequisites: 
1. Download [models](https://nofile.io/f/WQ1zrvx3XbA/models.tar.gz) and extract it to *home_surveillance/* directory  
2. Download and build [OpenCV 3](https://docs.opencv.org/trunk/d7/d9f/tutorial_linux_install.html) from source with ffmpeg 
3. Download [openface](https://github.com/cmusatyalab/openface) then add it to your PYTHONPATH environment variable
4. Download and build [LightGBM](https://lightgbm.readthedocs.io/en/latest/) then add it to your PYTHONPATH environment variable
5. Database schema is available [here](https://github.com/AkshatShetty101/CereLabs_Event_Recognition/blob/master/database.txt). MySQL 5.7+ required

After completing the pre-requisites to run the server, navigate to *system* and run `python WebApp.py` then access website at http://localhost:5000

### Usage:
   * The system is started by running the system/WebApp.py file
   * Before running the python file make sure the path variables for the database is set along with the username and password