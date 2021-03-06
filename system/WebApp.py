from flask import Flask, render_template, Response, redirect, url_for, request, jsonify, send_file, session, g
from flask_uploads import UploadSet, configure_uploads, IMAGES
import Camera
from flask_socketio import SocketIO, send, emit 
import SurveillanceSystem
import json
import shutil
import logging
from logging.handlers import RotatingFileHandler
import threading
import time
from random import random
import os
import sys
import cv2
import psutil
import SQL_Functions
import re
import ImageUtils
import numpy as np

LOG_FILE = 'logs/WebApp.log'

# Initialises system variables, this object is the heart of the application
HomeSurveillance = SurveillanceSystem.SurveillanceSystem()
# Initialise database variable
DataBase = SQL_Functions.DatabaseHelper() 
# Threads used to continuously push data to the client
alarmStateThread = threading.Thread() 
facesUpdateThread = threading.Thread() 
monitoringThread = threading.Thread() 
alarmStateThread.daemon = False
facesUpdateThread.daemon = False
monitoringThread.daemon = False
event_capture = None

# Flask setup
app = Flask('SurveillanceWebServer')
app.config['SECRET_KEY'] = os.urandom(24) # Used for session management
socketio = SocketIO(app)
photos = UploadSet('photos', IMAGES)
base_dir = 'training-images/'
app.config['UPLOADED_PHOTOS_DEST'] = base_dir 
configure_uploads(app, photos)

LOG_TAG = '[WEB_APP.PY]'


@app.route('/', methods=['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        session.pop('user',None) # Drops session everytime user tries to login

        if len(request.form['username']) == 0 or len(request.form['password']) == 0:
            error = 'The username or password field(s) cannot be empty. Please try again'
        else:
            auth = DataBase.admin('verify')(request.form['username'], request.form['password']) # Database Auth
            if len(auth) == 0 or auth[0] == False:
                error = 'Invalid username or password. Please try again'
            elif auth[0] == True:
                print('{} {} has logged in successfully'.format(LOG_TAG, request.form['username']))
                session['user'] = request.form['username']
                if not HomeSurveillance.recogniser.classifierFlag:
                    print("retrain through login page")
                    app.logger.info("retrain through login page")
                    o_fname, n_fname, o_fname2, n_fname2, retrained = HomeSurveillance.recogniser.trainClassifier(DataBase)#calling the module in FaceRecogniser to start training
                    #print(o_fname, n_fname, o_fname2, n_fname2)
                    HomeSurveillance.trainingEvent.clear() # Block processing threads
                    HomeSurveillance.recogniser.switchClassifiers(o_fname, n_fname, o_fname2, n_fname2)
                    HomeSurveillance.trainingEvent.set() # Release processing threads       
                    app.logger.info("Finished re-training")
                return redirect(url_for('home'))
    
    return render_template('login.html', error = error)

@app.route('/master_remove', methods=['GET','POST'])
def master_remove():
    alert=None
    room_data = DataBase.room('get')(None,'room_id','description')
    clear_data = DataBase.clearance_master('get')()
    privilege_data = DataBase.privilege_master('get')()
    cam_data = DataBase.cam_master('get')()
    risk_data = DataBase.risk_level_master('get')()
    type_data = DataBase.type_master('get')()
    employee_data = DataBase.employee('get')(None)
    admin_data = DataBase.admin('get')(None)
    print(admin_data)
    if request.method == 'POST':
        data = dict(request.form)
        id = data.get('id')[0]
        content = data.get('content')
        if str(id) == '1':
            print(id,content)
            output = DataBase.room('delete')(int(content[0]))
            print(output)
            if output == True:
                return Response(json.dumps({'url': output,'message':'Room is successfully removed'}), mimetype='text/json')
            else:
                return Response(json.dumps({'url': output,'message':'Failed to remove room'}), mimetype='text/json')
        elif str(id) == '2':
            print(id,content)
            output = DataBase.clearance_master('delete')(int(content[0]))
            print(output)
            if output == True:
                return Response(json.dumps({'url': output,'message':'Clearance level is successfully removed'}), mimetype='text/json')
            else:
                return Response(json.dumps({'url': output,'message':'Failed to remove clearance level'}), mimetype='text/json')
        elif str(id) == '3':
            print(id,content)
            output = DataBase.cam_master('delete')(int(content[0]))
            print(output)
            if output == True:
                return Response(json.dumps({'url': output,'message':'Camera is successfully removed'}), mimetype='text/json')
            else:
                return Response(json.dumps({'url': output,'message':'Failed to remove camera'}), mimetype='text/json')
        elif str(id) == '4':
            print(id,content)
            output = DataBase.privilege_master('delete')(int(content[0]))
            print(output)
            if output == True:
                return Response(json.dumps({'url': output,'message':'Privilege level is successfully removed'}), mimetype='text/json')
            else:
                return Response(json.dumps({'url': output,'message':'Failed to remove privilege level'}), mimetype='text/json')
        elif str(id) == '5':
            print(id,content)
            output = DataBase.risk_level_master('delete')(int(content[0]))
            print(output)
            if output == True:
                return Response(json.dumps({'url': output,'message':'Risk level is successfully removed'}), mimetype='text/json')
            else:
                return Response(json.dumps({'url': output,'message':'Failed to remove risk level'}), mimetype='text/json')
        elif str(id) == '6':
            print(id,content)
            output = DataBase.type_master('delete')(int(content[0]))
            print(output)
            if output == True:
                return Response(json.dumps({'url': output,'message':'Event type is successfully removed'}), mimetype='text/json')
            else:
                return Response(json.dumps({'url': output,'message':'Failed to remove event type'}), mimetype='text/json')
        elif str(id) == '7':
            print(id,content)
            output = DataBase.employee('delete')(int(content[0]))
            print(output)
            if output == True:
                return Response(json.dumps({'url': output,'message':'Employee is successfully removed'}), mimetype='text/json')
            else:
                return Response(json.dumps({'url': output,'message':'Failed to remove employee'}), mimetype='text/json')
        elif str(id) == '8':
            print(id,content)
            output = DataBase.admin('delete')(int(content[0]))
            print(output)
            if output == True:
                return Response(json.dumps({'url': output,'message':'Administrator is successfully removed'}), mimetype='text/json')
            else:
                return Response(json.dumps({'url': output,'message':'Failed to remove administrator'}), mimetype='text/json')
    return render_template('master_remove.html', room_data = room_data, clear_data = clear_data, cam_data = cam_data, \
     privilege_data = privilege_data, risk_data = risk_data, type_data = type_data,employee_data = employee_data, admin_data = admin_data)

@app.route('/master_add', methods=['GET','POST'])
def master_add():
    error = None
    success = None
    value = None
    clear_data = DataBase.clearance_master('get')()
    room_data = DataBase.room('get_ids')()
    risk_data = DataBase.risk_level_master('get')()
    if request.method == 'POST':
        if "add_camera" in request.form:
            print("{} add_camera".format(LOG_TAG))
            room_id = request.form['room_id']
            value = 1
            if not str(room_id) == "false":
                res = request.form['res']
                model = request.form['model']
                link = request.form['link']
                data = DataBase.cam_master('insert')(int(room_id),res,model,link)
                data = json.loads(data)
                if int(data.get('status')) == 1:
                    success = data.get('message')
                    print("{} {}".format(LOG_TAG,data.get('message')))
                else:
                    print("{} {}".format(LOG_TAG,data.get('message')))
                    error = data.get('message')
            else:
                error = "Please select a Room Id"
        elif "add_emp" in request.form:
            print("add_emp")
            return redirect(url_for('register_employee'))
        elif "add_admin" in request.form:
            print("add_admin")
            return redirect(url_for('register_admin'))
        elif "add_room" in request.form:
            print("{} add_room".format(LOG_TAG))
            level = request.form['level1']
            value = 2
            if not str(level) == "false":
                room_id = request.form['room_id1']
                data = DataBase.room('insert')(int(room_id),int(level))
                data = json.loads(data)
                if int(data.get('status')) == 1:
                    success = data.get('message')
                    print("{} {}".format(LOG_TAG,data.get('message')))
                else:
                    print("{} {}".format(LOG_TAG,data.get('message')))
                    error = data.get('message')
            else:
                error="Please select a clearance level"
        elif "add_event_type" in request.form:
            print("{} add_event_type".format(LOG_TAG))
            level = request.form['level3']
            if not str(room_id) == "false":
                type_id = request.form['type_id3']
                desc = request.form['desc3']
                data = DataBase.type_master('insert')(int(type_id),int(level),str(desc))
                data = json.loads(data)
                value = 4
                if int(data.get('status')) == 1:
                    success = data.get('message')
                    print("{} {}".format(LOG_TAG,data.get('message')))
                else:
                    print("{} {}".format(LOG_TAG,data.get('message')))
                    error = data.get('message')
            else:
                error="Please select a risk level"
        elif "add_risk" in request.form:
            print("{} add_risk".format(LOG_TAG))
            level = request.form['level2']
            desc = request.form['desc2']
            data = DataBase.risk_level_master('insert')(int(level),str(desc))
            data = json.loads(data)
            value = 3
            if int(data.get('status')) == 1:
                success = data.get('message')
                print("{} {}".format(LOG_TAG,data.get('message')))
            else:
                print("{} {}".format(LOG_TAG,data.get('message')))
                error = data.get('message')
            
        elif "add_privilege" in request.form:
            print("{} add_privilege".format(LOG_TAG))
            level = request.form['level4']
            desc = request.form['desc4']
            data = DataBase.privilege_master('insert')(int(level),str(desc))
            data = json.loads(data)
            value = 5
            if int(data.get('status')) == 1:
                success = data.get('message')
                print("{} {}".format(LOG_TAG,data.get('message')))
            else:
                print("{} {}".format(LOG_TAG,data.get('message')))
                error = data.get('message')
            
        elif "add_clearance" in request.form:
            print("{} add_clearance".format(LOG_TAG))
            level = request.form['level5']
            desc = request.form['desc5']
            data = DataBase.clearance_master('insert')(int(level),str(desc))
            data = json.loads(data)
            value = 6
            if int(data.get('status')) == 1:
                success = data.get('message')
                print("{} {}".format(LOG_TAG,data.get('message')))
            else:
                print("{} {}".format(LOG_TAG,data.get('message')))
                error = data.get('message')
                    
    return render_template('master_add.html', error = error, success = success, value = value, room_data = room_data, clear_data = clear_data, risk_data = risk_data)


@app.route('/home')
def home():
    if g.user:
        return render_template('index.html')
    return redirect(url_for('login'))

@app.route('/register_employee', methods=['GET', 'POST'])
def register_employee():
    """Register an Employee"""
    error = None
    data = DataBase.clearance_master('get')()
    emp_name =  dict((i[1],i[0]) for i in DataBase.employee('get')())
    print(emp_name)
    fname = None
    g.user = 'admin' # Hack
    if request.method == 'POST' and g.user:
        clearance_level = request.form['clearance_level']
        try:
            assert int(clearance_level) in data.keys()
        except:
            print('{} Clearance Level Data is incorrect'.format(LOG_TAG))
            error = "Please select a clearance level from the dropdown"
        if not error:
            name = request.form['fullname'].strip()
            regex_to_match = re.compile('^[A-Za-z ]+$')
            fname=""
            if not (len(name) > 0 and regex_to_match.match(name) != None):
                error = "Name is invalid"
            if not error:
                print('{} Valid data Posted'.format(LOG_TAG))
                try:
                    if emp_name[name]:
                        print('present!')
                        fname = str(emp_name[name])
                except KeyError:
                    print('Not already registered!!')
                    fname = str(DataBase.employee('insert')(name,int(clearance_level)))
                    print(fname)
                files = request.files.getlist('recog_data')
                print(files)
                recog_data = list()
                if len(files) > 0:
                    print(os.getcwd())
                    if(os.path.isdir(os.getcwd()+'/training-images/' +fname) == True):
                        print('deleted old folder!')
                        shutil.rmtree(os.getcwd()+'/training-images/' +fname)
                    os.mkdir(os.getcwd()+'/training-images/' +fname)
                    app.config['UPLOADED_PHOTOS_DEST'] = base_dir+fname
                    configure_uploads(app, photos)
                    print(app.config['UPLOADED_PHOTOS_DEST'])    
                    print('made dir')
                    for file in files:
                        filename = photos.save(file)
                        print(filename)
                        name = request.form.get('name')
                        # image = 'uploads/imgs/' +fname+"/" +filename
                        # with open(image, "rb") as imageFile:
                        #     image_data = imageFile.read()
                        #     recog_data.append(image_data)
            # TODO: Add module which converts recog_data to vector and returns it
    return render_template('register_employee.html', error = error, data = data, emp_id = fname)

@app.route('/register_admin', methods=['GET', 'POST'])
def register_admin():
    """Register an Administrator"""
    error = None
    data = DataBase.privilege_master('get')()
    print(data)
    success = None
    g.user = 'admin' # Hack
    if request.method == 'POST' and g.user:
        print("HERE!!!!!")
        privilege_level = int(request.form['privilege_level'])
        try:
            assert int(privilege_level) in data.keys()
        except:
            print('{} Privilege Level Data is incorrect'.format(LOG_TAG))
            error = "Please select a privilege level from the dropdown"
        emp_id = int(request.form['emp_id'])
        db_result = DataBase.employee('get')(emp_id)
        db_result = [v[0] for v in db_result]
        print(db_result)
        if emp_id not in db_result:
            emp_id = None
            error = "Employee does not exist"
        
        regex_to_match = re.compile('^[A-Za-z0-9@$#]+')
        username = request.form['username'].strip()
        password = request.form['password']
        if not (len(username) > 0 and regex_to_match.match(username) != None):
            error = "Invalid Username"
        
        regex_to_match = re.compile('[A-Z]+[a-z]*[1-9]+') # 1 or more Cap, 0 or more small, 1 or more number
        if not (len(password) > 0 and regex_to_match.match(password) != None):
            error = "Password should have 1 or more Cap, 0 or more small, 1 or more number"
        
        result = False
        if not error:
            print('{} Valid data Posted'.format(LOG_TAG))
            print(emp_id, privilege_level, username, password)
            result = DataBase.admin('insert')(emp_id, privilege_level, username, password)
            success = True
        if result == True:
            redirect(url_for('home'))

    return render_template('register_admin.html', error = error, data = data, success = success)

@app.before_request
def before_request():
    """Initialise session"""
    # g.user = None
    g.user = 'admin' # Hack
    # if 'user' in session:
    #     g.user = session['user']

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST' and 'photo' in request.files:
        try:
            filename = photos.save(request.files['photo'])
            image = request.files['photo']
            name = request.form.get('name')
            image = 'uploads/imgs/' + filename
            with open(image, "rb") as imageFile:
                image = imageFile.read()    
            wriitenToDir = HomeSurveillance.add_face(DataBase, name, image, upload = True)
            message = "file uploaded successfully"
        except:
            message = "file upload unsuccessfull"

        return render_template('index.html', message = message)
    if g.user:
        return render_template('index.html')
    else:
        return redirect(url_for('login'))
    print(message)

def gen(camera):
    """Can read processed frame or unprocessed frame.
    When streaming the processed frame with read_processed()
    and setting the drawing variable in the SurveillanceSystem 
    class, you can see all detection bounding boxes. This
    however slows down streaming and therefore read_jpg()
    is recommended"""
    while True:
        frame = camera.read_processed()    # read_jpg()  # read_processed()    
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')  # Builds 'jpeg' data with header and payload

@app.route('/video_streamer/<camNum>')
def video_streamer(camNum):
    global event_capture
    if event_capture != None:
        print('Released!')
        event_capture.release()
    """Used to stream frames to client, camNum represents the camera index in the cameras array"""
    return Response(gen(HomeSurveillance.cameras[int(camNum)]),
                    mimetype='multipart/x-mixed-replace; boundary=frame') # A stream where each part replaces the previous part the multipart/x-mixed-replace content type must be used.

@app.route('/events', methods=['GET', 'POST'])
def events():
    error = None
    if request.method == 'POST':
        pass
    return render_template('events.html', error=None)

@app.route('/get_events', methods=['GET', 'POST'])
def get_events():
    error = None
    if request.method == 'POST':
        pass
        return redirect(url_for('/events'))
    else:
        allEvents = DataBase.events('get')()
        results = list()
        for i,row in enumerate(allEvents):
            data = {
                'event_id': row[0],
                'time_start': row[1].strftime("%Y-%m-%d %H:%M:%S"),
                'time_end': row[2].strftime("%Y-%m-%d %H:%M:%S"),
                'type_id': row[3],
                'cam_id': row[4],
                'event_description': row[6]
                # 'url': row
            }
            results.append(data) 
    return Response(json.dumps(results), mimetype='text/json')

def getClip(eventNum):
    global event_capture
    if event_capture != None:
        print('Released!')
        event_capture.release() 
    url = DataBase.events('get')(eventNum, 'data')
    url = url[0][0].decode()
    print(url)
    event_capture = cv2.VideoCapture(url)  
    while True:
        ret, frame = event_capture.read()
        frame = ImageUtils.resize_mjpeg(frame)
        ret, jpeg = cv2.imencode('.jpg', frame)
        jpeg = jpeg.tostring()
        if not ret:
            continue
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg + b'\r\n\r\n')  # Builds 'jpeg' data with header and payload

@app.route('/events_streamer/<eventNum>')
def events_streamer(eventNum):
    """Used to stream frames to client, eventNum represents the event_id"""
    return Response(getClip(eventNum), 
        mimetype='multipart/x-mixed-replace; boundary=frame')# A stream where each part replaces the previous part the multipart/x-mixed-replace content type must be used.

def system_monitoring():
    """Pushes system monitoring data to client"""
    while True:
        cameraProcessingFPS = []
        for camera in HomeSurveillance.cameras:
    
            cameraProcessingFPS.append("{0:.2f}".format(camera.processingFPS))
            app.logger.info("FPS: " +str(camera.processingFPS) + " " + str(camera.streamingFPS))
        systemState = {'cpu':cpu_usage(),'memory':memory_usage(), 'processingFPS': cameraProcessingFPS}
        socketio.emit('system_monitoring', json.dumps(systemState) ,namespace='/surveillance')
        time.sleep(3)

def cpu_usage():
      psutil.cpu_percent(interval=1, percpu=False) #ignore first call - often returns 0
      time.sleep(0.12)
      cpu_load = psutil.cpu_percent(interval=1, percpu=False)
      app.logger.info("CPU Load: " + str(cpu_load))
      return cpu_load  

def memory_usage():
     mem_usage = psutil.virtual_memory().percent
     app.logger.info("System Memory Usage: " + str( mem_usage))
     return mem_usage 

@app.route('/add_camera', methods = ['GET','POST'])
def add_camera():
    """Adds camera new camera to SurveillanceSystem's cameras array"""
    if request.method == 'POST':  
        camURL = request.form.get('camURL')
        with HomeSurveillance.camerasLock :
            HomeSurveillance.add_camera(SurveillanceSystem.Camera.IPCamera(camURL))
        data = {"camNum": len(HomeSurveillance.cameras) -1}
        app.logger.info("Addding a new camera with url: ")
        app.logger.info(camURL)
        return jsonify(data)
    return render_template('index.html')

@app.route('/remove_camera', methods = ['GET','POST'])
def remove_camera():
    if request.method == 'POST':
        print('In remove camera!')
        camID = request.form.get('camID')
        sd, camNum = camID.split('_')
        app.logger.info("Removing camera: ")
        app.logger.info(camID)
        with HomeSurveillance.camerasLock:
            HomeSurveillance.remove_camera(int(camNum))
            DataBase.cam_master('delete')(int(camNum))
            app.logger.info("Removing camera number : " + camNum)
            data = {"alert_status": "removed"}
            return jsonify(data)
    return render_template('index.html')

@app.route('/remove_face', methods = ['GET','POST'])
def remove_face():
    if request.method == 'POST':
        predicted_name = request.form.get('predicted_name')
        camNum = request.form.get('camera')

        with HomeSurveillance.cameras[int(camNum)].peopleDictLock:
            try:
                del HomeSurveillance.cameras[int(camNum)].people[predicted_name]
                app.logger.info("==== REMOVED: " + predicted_name + "===")
            except Exception as e:
                app.logger.error("ERROR could not remove Face" + e)
                pass

        data = {"face_removed":  'true'}
        return jsonify(data)
    return render_template('index.html')

@app.route('/add_face', methods = ['GET','POST'])
def add_face():
    if request.method == 'POST':
        trust = request.form.get('trust')
        new_name = request.form.get('new_name')
        person_id = request.form.get('person_id')
        camNum = request.form.get('camera')
        img = None
        
        with HomeSurveillance.cameras[int(camNum)].peopleDictLock:  
            try:  
                img = HomeSurveillance.cameras[int(camNum)].people[person_id].face   # Gets face of person detected in cameras 
                predicted_name = HomeSurveillance.cameras[int(camNum)].people[person_id].identity
                del HomeSurveillance.cameras[int(camNum)].people[person_id]    # Removes face from people detected in all cameras 
            except Exception as e:
                app.logger.error("ERROR could not add Face" + e)
 
        app.logger.info("trust " + str(trust))
        if str(trust) == "false":
            wriitenToDir = HomeSurveillance.add_face(new_name,img, upload = False)
        else:
            wriitenToDir = HomeSurveillance.add_face(predicted_name,img, upload = False)

        systemData = {'camNum': len(HomeSurveillance.cameras) , 'people': HomeSurveillance.peopleDB, 'onConnect': False}
        socketio.emit('system_data', json.dumps(systemData) ,namespace='/surveillance')
           
        data = {"face_added":  wriitenToDir}
        return jsonify(data)
    return render_template('index.html')

@app.route('/retrain_classifier', methods = ['GET','POST'])
def retrain_classifier():
    if request.method == 'POST':
        print("It has begun!")
        app.logger.info("retrain button pushed. clearing event in surveillance objt and calling trainingEvent")
        o_fname, n_fname, o_fname2, n_fname2, retrained = HomeSurveillance.recogniser.trainClassifier(DataBase)#calling the module in FaceRecogniser to start training
        HomeSurveillance.trainingEvent.clear() # Block processing threads
        HomeSurveillance.recogniser.switchClassifiers(o_fname, n_fname, o_fname2, n_fname2)
        HomeSurveillance.trainingEvent.set() # Release processing threads       
        data = {"finished":  retrained}
        app.logger.info("Finished re-training")
        return jsonify(data)
    return render_template('index.html')

@app.route('/get_faceimg/<name>')
def get_faceimg(name):  
    key,camNum = name.split("_")
    try:
        with HomeSurveillance.cameras[int(camNum)].peopleDictLock:
            img = HomeSurveillance.cameras[int(camNum)].people[key].thumbnail 
    except Exception as e:
        app.logger.error("Error " + str(e))
        img = ""

    if img == "":
        return "http://www.character-education.org.uk/images/exec/speaker-placeholder.png"            
    return  Response((b'--frame\r\n'
                     b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n\r\n'),
                    mimetype='multipart/x-mixed-replace; boundary=frame') 


@app.route('/get_all_faceimgs/<name>')
def get_faceimgs(name):  
    key, camNum, imgNum = name.split("_")
    try:
        with HomeSurveillance.cameras[int(camNum)].peopleDictLock:
            img = HomeSurveillance.cameras[int(camNum)].people[key].thumbnails[imgNum] 
    except Exception as e:
        app.logger.error("Error " + e)
        img = ""

    if img == "":
        return "http://www.character-education.org.uk/images/exec/speaker-placeholder.png"            
    return  Response((b'--frame\r\n'
                     b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n\r\n'),
                    mimetype='multipart/x-mixed-replace; boundary=frame') 

def update_faces():
    """Used to push all detected faces to client"""
    while True:
        peopledata = []
        persondict = {}
        thumbnail = None
        with HomeSurveillance.camerasLock :
            for i, camera in enumerate(HomeSurveillance.cameras):
                # print("{}---{}".format(i,HomeSurveillance.cameras[i].url))
                with HomeSurveillance.cameras[i].peopleDictLock:
                    for key, person in camera.people.items():  
                        persondict = {'identity': key , 'confidence': person.confidence, 'camera': i, 'timeD':person.time, 'prediction': person.identity,'thumbnailNum': len(person.thumbnails)}
                        app.logger.info(persondict)
                        peopledata.append(persondict)
        # print(peopledata)
        socketio.emit('people_detected', json.dumps(peopledata) ,namespace='/surveillance')
        time.sleep(4)
                   
@socketio.on('connect', namespace='/surveillance') 
def connect(): 
    
    # Need visibility of global thread object                
    global alarmStateThread
    global facesUpdateThread 
    global monitoringThread

    #print "\n\nclient connected\n\n"
    app.logger.info("client connected")
   
    if not facesUpdateThread.isAlive():
        #print "Starting facesUpdateThread"
        app.logger.info("Starting facesUpdateThread")
        facesUpdateThread = threading.Thread(name='websocket_process_thread_',target= update_faces, args=())
        facesUpdateThread.start()

    if not monitoringThread.isAlive():
        #print "Starting monitoringThread"
        app.logger.info("Starting monitoringThread")
        monitoringThread = threading.Thread(name='monitoring_process_thread_',target= system_monitoring, args=())
        monitoringThread.start()

    cameraData = {}
    cameras = []

    allCameras = DataBase.cam_master('get')('NULL')
    db_url_list = [val[1] for val in allCameras.items()]
    url_list = [c.url for c in HomeSurveillance.cameras]
    #print("DB: {}".format(db_url_list))
    #print("System: {}".format(url_list))
    #print(cameraData)
    with HomeSurveillance.camerasLock :
        for key, value in allCameras.items():
            cameraData = {'camNum': key, 'url': value}
            app.logger.info(cameraData)
            cameras.append(cameraData)    
            if not value in url_list:
                HomeSurveillance.add_camera(SurveillanceSystem.Camera.IPCamera(value))
            else:
                print('cam already present')
    #print(cameraData)
    systemData = {
        'camNum': len(HomeSurveillance.cameras) ,
        'people': HomeSurveillance.peopleDB, 
        'cameras': cameras, 
        'onConnect': True}

    #Create default alert 
    with HomeSurveillance.alertsLock:
        HomeSurveillance.alerts.append(SurveillanceSystem.Alert(DataBase, socketio, '', 'all', 'Recognition', 'unknown', '', '', 0, 1))
    socketio.emit('system_data', json.dumps(systemData) ,namespace='/surveillance')

@socketio.on('disconnect', namespace='/surveillance')
def disconnect():
    #print('Client disconnected')
    app.logger.info("Client disconnected")

if __name__ == '__main__':
    # Starts server on default port 5000 and makes socket connection available to other hosts (host = '0.0.0.0')
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler = RotatingFileHandler(LOG_FILE, maxBytes=1000000, backupCount=10)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.DEBUG)  
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.DEBUG)
    log.addHandler(handler)
    socketio.run(app, host='0.0.0.0', debug=False, use_reloader=False)