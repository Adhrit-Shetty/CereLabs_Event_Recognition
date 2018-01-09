import pymysql as pms
import time
import datetime
import os
import hashlib
import json

class EventsHelper:
    LOG_TAG = '[EVENTS_HELPER]'

    def __init__(self, db):
        self.db = db

    def insert_event(self, ts_start, ts_stop, type_id, cam_id, tags, data):
        cursor = self.db.cursor()
        # Timestamp in mysql is of format 'YYYY-MM-DD hh:mm:ss'
        myts_start = datetime.datetime.fromtimestamp(ts_start).strftime('%Y-%m-%d %H:%M:%S')
        myts_stop = datetime.datetime.fromtimestamp(ts_stop).strftime('%Y-%m-%d %H:%M:%S')
        sql = "INSERT INTO events(ts_start, ts_stop, type_id, cam_id, tags, data) values(%s, %s, %d, %d, '%s', '%s')" % (myts_start, myts_stop, type_id, cam_id, tags, data)
        try:
            cursor.execute(sql)
            self.db.commit()
            print('{} Insert Successful!'.format(self.LOG_TAG))
        except:
            self.db.rollback()
            print('{} Error: Insert Unsuccessful!'.format(self.LOG_TAG))

    def delete_event(self, event_id):
        cursor = self.db.cursor()
        sql = "DELETE FROM events WHERE event_id = %d" % (event_id)
        try:
            cursor.execute(sql)
            self.db.commit()
            print('{} Delete Successful!'.format(self.LOG_TAG))
        except:
            self.db.rollback()
            print('{} Error: Delete Unsuccessful!'.format(self.LOG_TAG))

    def get_event(self, event_id, *args):
        cursor = self.db.cursor()

        projection = ''
        for arg in args:
            projection = str(projection)+str(arg)+" ,"
        projection = projection[:-2]  # Remove trailing comma and space
        print('{} get_event projection => {}'.format(self.LOG_TAG, projection))
        sql = "SELECT %s FROM events JOIN type_master ON events.type_id = type_master.type_id JOIN cam_master ON events.cam_id = cam_master.cam_id WHERE event_id = %d " % (projection, event_id)
        try:
            cursor.execute(sql)
            results = cursor.fetchone()
            print('{} fetch data successfull! {}'.format(self.LOG_TAG, results))
            return results
        except:
            print('{} Error fetching data!'.format(self.LOG_TAG))
            return list()


class EmployeeHelper:
    LOG_TAG = '[EMPLOYEE_HELPER]'

    def __init__(self, db):
        self.db = db

    def add_employee(self, name, clearance_level, recog_data='NULL'):
        cursor = self.db.cursor()

        sql = "INSERT INTO employee(name, recog_data, clearance_level) VALUES('%s', '%s', %d)" % (name, recog_data, clearance_level)
        try:
            cursor.execute(sql)
            self.db.commit()
            print('{} Add Successful!'.format(self.LOG_TAG))
            sql = "SELECT emp_id FROM employee WHERE name = '%s' ORDER BY emp_id DESC LIMIT 1" % (name)# fetch the inserted emp_id
            cursor.execute(sql)
            results = cursor.fetchone()
            return results[0]
        except:
            self.db.rollback()
            print('{} Error: Add Unsuccessful!'.format(self.LOG_TAG))

    def update_employee_details(self, emp_id, **kwargs):
        cursor = self.db.cursor()
        updates = ''
        for k, v in kwargs.items():
            updates = updates + str(" %s = '%s', " % (k, v))
        # Remove trailing comma and space
        sql = "UPDATE employee SET" + str(updates[:-2])
        
        try:
            sql = sql + str(" WHERE emp_id = %d" % (emp_id))

            #print('{} Update Query => {}'.format(self.LOG_TAG, sql))

            cursor.execute(sql)
            self.db.commit()
            print('{} Update Successful!'.format(self.LOG_TAG))
        except:
            self.db.rollback()
            print('{} Error: Update Unsuccessful!'.format(self.LOG_TAG))
        
    def fire_employee(self, emp_id):
        cursor = self.db.cursor()
        sql = "DELETE FROM employee WHERE emp_id = %d" % (emp_id)
        try:
            cursor.execute(sql)
            self.db.commit()
            print('{} firing Successful!'.format(self.LOG_TAG))
        except:
            self.db.rollback()
            print('{} Error: firing Unsuccessful!'.format(self.LOG_TAG))

    def get_employee_details(self, emp_id, *args):
        cursor = self.db.cursor()
        projection = '*'
        if len(args) > 0:
            for arg in args:
                projection = str(projection)+str(arg)+" ,"
                projection = projection[:-2]  # Remove trailing comma and space

        print('{} get_employee projection = {}'.format(self.LOG_TAG, projection))

        sql = "SELECT %s FROM employee JOIN clearance_level_master ON employee.clearance_level = clearance_level_master.level WHERE emp_id = %d" % (projection, emp_id)
        try:
            cursor.execute(sql)
            results = cursor.fetchone()
            print('{} fetching Successful!'.format(self.LOG_TAG))
            if results == None:
                results = list()
            return results
        except:
            print('{} Error fetching data'.format(self.LOG_TAG))
            return list()


class AdminHelper:
    LOG_TAG = '[ADMIN_HELPER]'

    def __init__(self, db):
        self.db = db

    def add_admin(self, emp_id, privilege_level, username, password):
        cursor = self.db.cursor()
        password_hashed = hashlib.sha256(password.encode()).hexdigest()
        sql = "INSERT INTO admin(emp_id, privilege_level, username, password) values(%d, %d, '%s', '%s')" % (emp_id, privilege_level, username, password_hashed)
        try:
            cursor.execute(sql)
            self.db.commit()
            print('{} add Successful!'.format(self.LOG_TAG))
            return True
        except:
            self.db.rollback()
            print('{} Error: add Unsuccessful!'.format(self.LOG_TAG))
            return False

    def update_admin_details(self, admin_id, **kwargs):
        cursor = self.db.cursor()

        updates = ''
        for k, v in kwargs:
            updates = updates.join(' %s = %s, ' % (k, v))
        # Remove trailing comma and space
        sql = "UPDATE admin SET".join(updates[:-2])

        try:
            sql = sql.join(" WHERE admin_id = %d" % (admin_id))

            print('{} Update Query => {}'.format(self.LOG_TAG, sql))

            cursor.execute(sql)
            self.db.commit()
            print('{} update Successful!'.format(self.LOG_TAG))
        except:
            self.db.rollback()
            print('{} Error: update Unsuccessful!'.format(self.LOG_TAG))

    def remove_admin(self, admin_id):
        cursor = self.db.cursor()
        sql = "DELETE FROM admin WHERE admin_id = %d" % (admin_id)
        try:
            cursor.execute(sql)
            self.db.commit()
            print('{} removing Successful!'.format(self.LOG_TAG))
        except:
            self.db.rollback()
            print('{} Error: removing Unsuccessful!'.format(self.LOG_TAG))

    def get_admin_details(self, admin_id, *args):
        cursor = self.db.cursor()
        projection = ''
        for arg in args:
            projection = str(projection)+str(arg)+" ,"
        projection = projection[:-2]  # Remove trailing comma and space

        print('{} get_event projection = {}'.format(self.LOG_TAG, projection))

        sql = "SELECT %s FROM admin JOIN employee ON admin.emp_id = employee.emp_id JOIN privilege_master ON admin.privilege_level = privilege_master.plvl WHERE admin_id = %d" % (projection, admin_id)
        try:
            cursor.execute(sql)
            results = cursor.fetchone()
            print('{} fetching Successful!'.format(self.LOG_TAG))
            return results
        except:
            print('{} Error fetching data'.format(self.LOG_TAG))
            return list()
    
    def verify_admin(self, username, password):
        cursor = self.db.cursor()
        password_hashed = hashlib.sha256(password.encode()).hexdigest()
        sql = "SELECT admin_id, emp_id, privilege_level FROM admin WHERE username = '%s' AND password = '%s'" % (username, password_hashed)

        try:
            cursor.execute(sql)
            results = cursor.fetchone()
            print('{} fetching Successful!'.format(self.LOG_TAG))
            if len(results) > 0:
                return [True]
            else:
                return [False]
        except:
            print('{} Error fetching data'.format(self.LOG_TAG))
            return list()


class RoomHelper:
    LOG_TAG = '[ROOM_HELPER]'

    def __init__(self, db):
        self.db = db

    def add_room(self, room_id, accessiblity):
        cursor = self.db.cursor()
        sql = "INSERT INTO room(room_id, accessiblity) values(%d, '%d')" % (room_id, accessiblity)
        try:
            cursor.execute(sql)
            self.db.commit()
            print('{} Add Successful!'.format(self.LOG_TAG))
            return json.dumps({"status":1, "message":'Add Successful'})
        except:
            self.db.rollback()
            print('{} Error: Add Unsuccessful!'.format(self.LOG_TAG))
            return json.dumps({"status":-1, "message":'Add Unsuccessful. Please check validity of input data'})

    def update_room_details(self, room_id, **kwargs):
        cursor = self.db.cursor()

        updates = ''
        for k, v in kwargs:
            updates = updates.join(' %s = %s, ' % (k, v))
        # Remove trailing comma and space
        sql = "UPDATE room SET".join(updates[:-2])

        try:
            sql = sql.join(" WHERE room_id = %d" % (room_id))

            print('{} Update Query => {}'.format(self.LOG_TAG, sql))

            cursor.execute(sql)
            self.db.commit()
            print('{} Update Successful!'.format(self.LOG_TAG))
        except:
            self.db.rollback()
            print('{} Error: Update Unsuccessful!'.format(self.LOG_TAG))

    def delete_room(self, room_id):
        cursor = self.db.cursor()
        sql = "DELETE FROM room WHERE room_id = %d" % (room_id)
        try:
            cursor.execute(sql)
            self.db.commit()
            print('{} removal Successful!'.format(self.LOG_TAG))
            return True
        except:
            self.db.rollback()
            print('{} Error: removal Unsuccessful!'.format(self.LOG_TAG))
            return False
    def get_room_ids(self):
        cursor = self.db.cursor()
        # projection = ''
        # for arg in args:
        #     projection = str(projection)+str(arg)+" ,"
        # projection = projection[:-2]  # Remove trailing comma and space

        # print('{} get_event projection = {}'.format(self.LOG_TAG, projection))

        sql = "SELECT %s FROM room " % ('room_id')
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            res=[]
            for ele in results:
                res.append(ele[0])
            print('{} fetching Successful!'.format(self.LOG_TAG))
            return res
        except:
            print('{} Error fetching data'.format(self.LOG_TAG))
            return list()

    def get_room_details(self, room_id=None, *args):
        cursor = self.db.cursor()
        projection = ""
        for arg in args:
            projection = str(projection)+str(arg)+" ,"
        projection = projection[:-2]  # Remove trailing comma and space
        type_of_fetch = 1
        print('{} get_event projection = {}'.format(self.LOG_TAG, projection))
        sql = "SELECT %s FROM room JOIN clearance_level_master clm ON room.accessiblity = clm.level" % (projection)
        if room_id != None:
            type_of_fetch = 2
            sql = "SELECT %s FROM room JOIN clearance_level_master clm ON room.accessiblity = clm.level WHERE room_id = %d" % (projection, room_id)
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            print(results)
            print('{} fetching Successful!'.format(self.LOG_TAG))
            if type_of_fetch == 1:
                return dict((x,y) for x,y in results)
            return results
        except:
            print('{} Error fetching data'.format(self.LOG_TAG))
            return list()
    

class ClearanceLevelMasterHelper:
    LOG_TAG = '[CLEARANCE_MASTER_HELPER]'

    def __init__(self, db):
        self.db = db

    def add_clearance_level(self, level, description):
        cursor = self.db.cursor()
        sql = "INSERT INTO clearance_level_master(level, description) values(%d, '%s')" % (level, description)
        try:
            cursor.execute(sql)
            self.db.commit()
            print('{} Add Successful!'.format(self.LOG_TAG))
            return json.dumps({"status":1, "message":'Add Successful'})
        except:
            self.db.rollback()
            print('{} Error: Add Unsuccessful!'.format(self.LOG_TAG))
            return json.dumps({"status":-1, "message":'Add Unsuccessful. Please check validity of input data'})

    def update_clearance_level(self, level, description):
        cursor = self.db.cursor()

        sql = "UPDATE clearance_level_master SET description = '%s' WHERE level = %d" % (description, level)
        
        try:
            cursor.execute(sql)
            self.db.commit()
            print('{} Update Successful!'.format(self.LOG_TAG))
        except:
            self.db.rollback()
            print('{} Error: Update Unsuccessful!'.format(self.LOG_TAG))

    def remove_clearance_level(self, level):
        cursor = self.db.cursor()
        sql = "DELETE FROM clearance_level_master WHERE level = %d" % (level)
        try:
            cursor.execute(sql)
            self.db.commit()
            print('{} removal Successful!'.format(self.LOG_TAG))
        except:
            self.db.rollback()
            print('{} Error: removal Unsuccessful!'.format(self.LOG_TAG))

    def get_clearance_details(self, level=None):
        cursor = self.db.cursor()
        type_of_fetch = 1
        sql = "SELECT level, description from clearance_level_master"
        if level != None:
            type_of_fetch = 2
            sql = "SELECT * FROM clearance_level_master WHERE level = %d" % (level)
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            print('{} fetching Successful!'.format(self.LOG_TAG))
            if type_of_fetch == 1:
                return dict((x,y) for x,y in results)
            return results
        except:
            print('{} Error fetching data'.format(self.LOG_TAG))
            return list()


class CamMasterHelper:
    LOG_TAG = '[CAM_MASTER_HELPER]'

    def __init__(self, db):
        self.db = db

    def add_cam(self, cam_id, room_id, resolution, model, rtsp_link):
        cursor = self.db.cursor()
        sql = "INSERT INTO cam_master(cam_id, room_id, resolution, model, rtsp_link) values(%d, %d, '%s', '%s', '%s')" % (cam_id, room_id, resolution, model, rtsp_link)
        try:
            cursor.execute(sql)
            self.db.commit()
            print('{} Add Successful!'.format(self.LOG_TAG))
            return json.dumps({"status":1, "message":'Add Successful'})
        except:
            self.db.rollback()
            print('{} Error: Add Unsuccessful!'.format(self.LOG_TAG))
            return json.dumps({"status":-1, "message":'Add Unsuccessful. Please check validity of input data'})

    def update_cam_details(self, cam_id, **kwargs):
        cursor = self.db.cursor()

        updates = ''
        for k, v in kwargs:
            updates = updates.join(' %s = %s, ' % (k, v))
        # Remove trailing comma and space
        sql = "UPDATE cam_master SET".join(updates[:-2])

        try:
            sql = sql.join(" WHERE cam_id = %d" % (cam_id))

            print('{} Update Query => {}'.format(self.LOG_TAG, sql))

            cursor.execute(sql)
            self.db.commit()
            print('{} Update Successful!'.format(self.LOG_TAG))
        except:
            self.db.rollback()
            print('{} Error: Update Unsuccessful!'.format(self.LOG_TAG))

    def remove_camera(self, cam_id):
        cursor = self.db.cursor()
        sql = "DELETE FROM cam_master WHERE cam_id = %d" % (cam_id)
        try:
            cursor.execute(sql)
            self.db.commit()
            print('{} removal Successful!'.format(self.LOG_TAG))
        except:
            self.db.rollback()
            print('{} Error: removal Unsuccessful!'.format(self.LOG_TAG))

    def get_cam_details(self, cam_id=None):
        cursor = self.db.cursor()
        type_of_fetch = 1
        sql = "SELECT cam_id, rtsp_link FROM cam_master"
        if cam_id != None:
            type_of_fetch = 2
            sql = "SELECT * FROM cam_master JOIN room ON cam_master.room_id = room.room_id WHERE cam_id = %d" % (cam_id)
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            print('{} fetching Successful!'.format(self.LOG_TAG))
            if type_of_fetch == 1:
                return dict((x,y) for x,y in results)
            return results
        except:
            print('{} Error fetching data'.format(self.LOG_TAG))
            return list()

class TypeMasterHelper:
    LOG_TAG = '[TYPE_MASTER_HELPER]'

    def __init__(self, db):
        self.db = db

    def add_type(self, type_id, risk_level, description):
        cursor = self.db.cursor()
        sql = "INSERT INTO type_master(type_id, risk_level, description) values(%d, %d, '%s')" % (type_id, risk_level, description)
        try:
            cursor.execute(sql)
            self.db.commit()
            print('{} Add Successful!'.format(self.LOG_TAG))
            return json.dumps({"status":1, "message":'Add Successful'})
        except:
            self.db.rollback()
            print('{} Error: Add Unsuccessful!'.format(self.LOG_TAG))
            return json.dumps({"status":-1, "message":'Add Unsuccessful. Please check validity of input data'})

    def update_type_details(self, type_id, **kwargs):
        cursor = self.db.cursor()

        updates = ''
        for k, v in kwargs:
            updates = updates.join(' %s = %s, ' % (k, v))
        # Remove trailing comma and space
        sql = "UPDATE type_master SET".join(updates[:-2])

        try:
            sql = sql.join(" WHERE type_id = %d" % (type_id))

            print('{} Update Query => {}'.format(self.LOG_TAG, sql))

            cursor.execute(sql)
            self.db.commit()
            print('{} Update Successful!'.format(self.LOG_TAG))
        except:
            self.db.rollback()
            print('{} Error: Update Unsuccessful!'.format(self.LOG_TAG))

    def remove_type(self, type_id):
        cursor = self.db.cursor()
        
        sql = "DELETE FROM type_master WHERE type_id = %d" % (type_id)
        try:
            cursor.execute(sql)
            self.db.commit()
            print('{} removal Successful!'.format(self.LOG_TAG))
        except:
            self.db.rollback()
            print('{} Error: removal Unsuccessful!'.format(self.LOG_TAG))

    def get_type_details(self, type_id=None):
        cursor = self.db.cursor()
        type_of_fetch = 1
        sql = "SELECT type_id, description FROM type_master"
        if type_id != None:
            type_of_fetch = 2
            sql = "SELECT * FROM type_master JOIN risk_level_master rlm ON type_master.risk_level = rlm.risk_level WHERE type_id = %d" % (type_id)
        try:
            cursor.execute(sql)
            results = cursor.fetchone()
            print('{} fetching Successful!'.format(self.LOG_TAG))
            if type_of_fetch == 1:
                return dict((x,y) for x,y in results)
            return results

        except:
            print('{} Error fetching data'.format(self.LOG_TAG))
            return list()

class RiskLevelMasterHelper:
    LOG_TAG = '[RISK_LEVEL_MASTER_HELPER]'

    def __init__(self, db):
        self.db = db

    def add_risk_level(self, risk_level, description):
        cursor = self.db.cursor()
        sql = "INSERT INTO risk_level_master(risk_level, description) values(%d, '%s')" % (risk_level, description)
        try:
            cursor.execute(sql)
            self.db.commit()
            print('{} add Successful!'.format(self.LOG_TAG))
            return json.dumps({"status":1, "message":'Add Successful'})
        except:
            self.db.rollback()
            print('{} Error: add Unsuccessful!'.format(self.LOG_TAG))
            return json.dumps({"status":-1, "message":'Add Unsuccessful. Please check validity of input data'})

    def update_risk_level(self, description):
        cursor = self.db.cursor()
        sql = "UPDATE risk_level_master SET description = '%s'" % (description)
        try:
            cursor.execute(sql)
            self.db.commit()
            print('{} update Successful!'.format(self.LOG_TAG))
        except:
            self.db.rollback()
            print('{} Error: update Unsuccessful!'.format(self.LOG_TAG))

    def remove_risk_level(self, risk_level):
        cursor = self.db.cursor()
        sql = "DELETE FROM risk_level_master WHERE risk_level = %d" % (risk_level)
        try:
            cursor.execute(sql)
            self.db.commit()
            print('{} removal Successful!'.format(self.LOG_TAG))
        except:
            self.db.rollback()
            print('{} Error: removal Unsuccessful!'.format(self.LOG_TAG))

    def get_risk_level(self, risk_level=None):
            cursor = self.db.cursor()
            type_of_fetch = 1
            sql = "SELECT risk_level, description FROM risk_level_master"
            if risk_level != None:
                type_of_fetch = 2
                sql = "SELECT * FROM risk_level_master WHERE risk_level = %d" % (risk_level)
            try:
                cursor.execute(sql)
                results = cursor.fetchall()
                print('{} fetching Successful!'.format(self.LOG_TAG))
                if type_of_fetch == 1:
                    return dict((x,y) for x,y in results)
                return results
            except:
                print('{} Error fetching data'.format(self.LOG_TAG))
                return list()
        
class PrivilegeMasterHelper:
    LOG_TAG = '[PRIVILEGE_MASTER_HELPER]'

    def __init__(self, db):
        self.db = db

    def add_privilege_level(self, plvl, description):
        cursor = self.db.cursor()
        sql = "INSERT INTO privilege_master(plvl, description) values(%d, '%s')" % (plvl, description)
        try:
            cursor.execute(sql)
            self.db.commit()
            print('{} add Successful!'.format(self.LOG_TAG))
            return json.dumps({"status":1, "message":'Add Successful'})
        except:
            self.db.rollback()
            print('{} Error: add Unsuccessful!'.format(self.LOG_TAG))
            return json.dumps({"status":-1, "message":'Add Unsuccessful. Please check validity of input data'})

    def update_privilege_description(self, description):
        cursor = self.db.cursor()
        sql = "UPDATE privilege_master SET description = '%s'" % (description)
        try:
            cursor.execute(sql)
            self.db.commit()
            print('{} update Successful!'.format(self.LOG_TAG))
        except:
            self.db.rollback()
            print('{} Error: update Unsuccessful!'.format(self.LOG_TAG))

    def remove_privilege(self, plvl):
        cursor = self.db.cursor()
        sql = "DELETE FROM privilege_master WHERE plvl = %d" % (plvl)
        try:
            cursor.execute(sql)
            self.db.commit()
            print('{} removal Successful!'.format(self.LOG_TAG))
        except:
            self.db.rollback()
            print('{} Error: removal Unsuccessful!'.format(self.LOG_TAG))

    def get_privileges(self, plvl=None):
        cursor = self.db.cursor()
        type_of_fetch = 1
        sql = "SELECT plvl, description from privilege_master"
        if plvl != None:
            type_of_fetch = 2
            sql = "SELECT * FROM privilege_master WHERE plvl = %d" % (plvl)
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            print('{} fetching Successful!'.format(self.LOG_TAG))
            if type_of_fetch == 1:
                return dict((x,y) for x,y in results)
            return results

        except:
            print('{} Error fetching data'.format(self.LOG_TAG))
            return list()

# This is the class you should import
class DatabaseHelper:
    LOG_TAG = '[DATABASE_HELPER]'

    def __init__(self):
        username = os.environ.get('DB_USER')
        if username == None:
            raise Exception('environment variable DB_USER not set')
        password = os.environ.get('DB_PASS')
        if password == None:
            raise Exception('environment variable DB_PASS not set')
        db_name = os.environ.get('DB_NAME')
        '''
        if db_name == None:
            raise Exception('environment variable DB_NAME not set')
        '''
        db_name ='surveillance'
        self.db = pms.connect('localhost', username, password, db_name)
        self.test_db_connection()

    def test_db_connection(self):
        cursor = self.db.cursor()
        try:
            cursor.execute("SELECT 1+1 AS RESULT")
            results = cursor.fetchone()
            if len(results) > 0:
                print('{} Connected to database successfully!'.format(self.LOG_TAG))
        except:
            print('{} Error: Not connected to database'.format(self.LOG_TAG))

    
    def events(self, intent):
        e = EventsHelper(self.db)
        return {
            'insert': e.insert_event,
            'delete': e.delete_event,
            'get': e.get_event
        }.get(intent, None)

    def room(self, intent):
        r = RoomHelper(self.db)
        return {
            'insert': r.add_room,
            'update': r.update_room_details,
            'delete': r.delete_room,
            'get': r.get_room_details,
            'get_ids': r.get_room_ids
        }.get(intent, None)

    def employee(self, intent):
        e = EmployeeHelper(self.db)
        return {
            'insert': e.add_employee,
            'update': e.update_employee_details,
            'delete': e.fire_employee,
            'get': e.get_employee_details
        }.get(intent, None)

    def admin(self, intent):
        a = AdminHelper(self.db)
        return {
            'insert': a.add_admin,
            'update': a.update_admin_details,
            'delete': a.remove_admin,
            'get': a.get_admin_details,
            'verify': a.verify_admin
        }.get(intent, None)

    def clearance_master(self, intent):
        c = ClearanceLevelMasterHelper(self.db)
        return {
            'insert': c.add_clearance_level,
            'update': c.update_clearance_level,
            'delete': c.remove_clearance_level,
            'get': c.get_clearance_details
        }.get(intent, None)

    def cam_master(self, intent):
        c = CamMasterHelper(self.db)
        return {
            'insert': c.add_cam,
            'update': c.update_cam_details,
            'delete': c.remove_camera,
            'get': c.get_cam_details
        }.get(intent, None)

    def type_master(self, intent):
        t = TypeMasterHelper(self.db)
        return {
            'insert': t.add_type,
            'update': t.update_type_details,
            'delete': t.remove_type,
            'get': t.get_type_details
        }.get(intent, None)
    
    def risk_level_master(self, intent):
        r = RiskLevelMasterHelper(self.db)
        return {
            'insert': r.add_risk_level,
            'update': r.update_risk_level,
            'delete': r.remove_risk_level,
            'get': r.get_risk_level
        }.get(intent, None)
    
    def privilege_master(self, intent):
        p = PrivilegeMasterHelper(self.db)
        return {
            'insert': p.add_privilege_level,
            'update': p.update_privilege_description,
            'delete': p.remove_privilege,
            'get': p.get_privileges
        }.get(intent, None)