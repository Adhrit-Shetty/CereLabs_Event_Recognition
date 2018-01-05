import pymysql as pms
import time
import datetime
import os
import hashlib

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
            projection = projection.join(arg + ' ,')
        projection = projection[:-2]  # Remove trailing comma and space
        print('{} get_event projection => {}'.format(self.LOG_TAG, projection))
        sql = "SELECT %s FROM events WHERE event_id = %d" % (projection, event_id)
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

    def add_employee(self, name, recog_data, clearance_level):
        cursor = self.db.cursor()
        sql = "INSERT INTO `employee` (`name`, `recog_data`, `clearance_level`) VALUES (%s, %s, %d)"
        try:
            cursor.execute(sql, ('Adhs', 'dsa', 1))
            self.db.commit()
            print('{} Add Successful!'.format(self.LOG_TAG))
        except:
            self.db.rollback()
            print('{} Error: Add Unsuccessful!'.format(self.LOG_TAG))

    def update_employee_details(self, emp_id, **kwargs):
        cursor = self.db.cursor()

        updates = ''
        for k, v in kwargs:
            updates = updates.join(' %s = %s, ' % (k, v))
        # Remove trailing comma and space
        sql = "UPDATE employee SET".join(updates[:-2])

        try:
            sql = sql.join(" WHERE emp_id = %d" % (emp_id))

            print('{} Update Query => {}'.format(self.LOG_TAG, sql))

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
        projection = ''
        for arg in args:
            projection = projection.join(arg + ' ,')
        projection = projection[:-2]  # Remove trailing comma and space

        print('{} get_event projection = {}'.format(self.LOG_TAG, projection))

        sql = "SELECT %s FROM employee WHERE emp_id = %d" % (projection, emp_id)
        try:
            cursor.execute(sql)
            results = cursor.fetchone()
            print('{} fetching Successful!'.format(self.LOG_TAG))
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
        except:
            self.db.rollback()
            print('{} Error: add Unsuccessful!'.format(self.LOG_TAG))

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
            projection = projection.join(arg + ' ,')
        projection = projection[:-2]  # Remove trailing comma and space

        print('{} get_event projection = {}'.format(self.LOG_TAG, projection))

        sql = "SELECT %s FROM admin JOIN employee ON admin.emp_id = employee.emp_id WHERE admin_id = %d" % (projection, admin_id)
        try:
            cursor.execute(sql)
            results = cursor.fetchone()
            print('{} fetching Successful!'.format(self.LOG_TAG))
            return results
        except:
            print('{} Error fetching data'.format(self.LOG_TAG))
            return list()


class RoomHelper:
    LOG_TAG = '[ROOM_HELPER]'

    def __init__(self, db):
        self.db = db

    def add_room(self, room_id, accessiblity):
        cursor = self.db.cursor()
        sql = "INSERT INTO room(room_id, accessiblity) values(%d, '%s')" % (room_id, accessiblity)
        try:
            cursor.execute(sql)
            self.db.commit()
            print('{} Add Successful!'.format(self.LOG_TAG))
        except:
            self.db.rollback()
            print('{} Error: Add Unsuccessful!'.format(self.LOG_TAG))

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
        except:
            self.db.rollback()
            print('{} Error: removal Unsuccessful!'.format(self.LOG_TAG))

    def get_room_details(self, room_id, *args):
        cursor = self.db.cursor()
        projection = ''
        for arg in args:
            projection = projection.join(arg + ' ,')
        projection = projection[:-2]  # Remove trailing comma and space

        print('{} get_event projection = {}'.format(self.LOG_TAG, projection))

        sql = "SELECT %s FROM employee WHERE room_id = %d" % (projection, room_id)
        try:
            cursor.execute(sql)
            results = cursor.fetchone()
            print('{} fetching Successful!'.format(self.LOG_TAG))
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
        except:
            self.db.rollback()
            print('{} Error: Add Unsuccessful!'.format(self.LOG_TAG))

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

    def get_clearance_details(self, level):
        cursor = self.db.cursor()

        sql = "SELECT * FROM clearance_level_master WHERE level = %d" % (level)
        try:
            cursor.execute(sql)
            results = cursor.fetchone()
            print('{} fetching Successful!'.format(self.LOG_TAG))
            return results
        except:
            print('{} Error fetching data'.format(self.LOG_TAG))
            return list()


class CamMasterHelper:
    LOG_TAG = '[CAM_MASTER_HELPER]'

    def __init__(self, db):
        self.db = db

    def add_cam(self, cam_id, room_id, resolution, model):
        cursor = self.db.cursor()
        sql = "INSERT INTO cam_master(cam_id, room_id, resolution, model) values(%d, %d, '%s', '%s')" % (cam_id, room_id, resolution, model)
        try:
            cursor.execute(sql)
            self.db.commit()
            print('{} Add Successful!'.format(self.LOG_TAG))
        except:
            self.db.rollback()
            print('{} Error: Add Unsuccessful!'.format(self.LOG_TAG))

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

    def get_cam_details(self, cam_id):
        cursor = self.db.cursor()

        sql = "SELECT * FROM cam_master WHERE cam_id = %d" % (cam_id)
        try:
            cursor.execute(sql)
            results = cursor.fetchone()
            print('{} fetching Successful!'.format(self.LOG_TAG))
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
        except:
            self.db.rollback()
            print('{} Error: Add Unsuccessful!'.format(self.LOG_TAG))

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

    def get_type_details(self, type_id):
        cursor = self.db.cursor()

        sql = "SELECT * FROM type_master WHERE type_id = %d" % (type_id)
        try:
            cursor.execute(sql)
            results = cursor.fetchone()
            print('{} fetching Successful!'.format(self.LOG_TAG))
            return results
        except:
            print('{} Error fetching data'.format(self.LOG_TAG))
            return list()

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

    
    def  events(self, intent):
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
            'get': r.get_room_details
        }.get(intent, None)

    def employee(self, intent):
        print(intent)
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
            'get': a.get_admin_details
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