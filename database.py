
"""Database models"""
from flask import Flask, jsonify
import psycopg2
import os
from psycopg2.extras import RealDictCursor
import datetime
from app.__init__ import app


class DatabaseConnection:
    """Connect to the database"""
    def __init__(self):

        try:
            self.conn = psycopg2.connect(host=os.environ.get("DB_HOST"),
                                            database=os.environ.get("DB_DATABASE"),
                                            user=os.environ.get("DB_USER"),
                                            password=os.environ.get("DB_PASSWORD"),
                                            port=os.environ.get("DB_PORT"))
                                        
            self.cur = self.conn.cursor(cursor_factory=RealDictCursor)
            self.conn.autocommit = True
            print ('****INFO****: Database connection to successfuly created')

        except psycopg2.DatabaseError as dberror:
            print (dberror)

    def drop_tables(self):
        """drop tables if exist"""
        self.cur.execute(
            "DROP TABLE IF EXISTS parcels, users CASCADE"
        )

    def create_tables(self):
        """create parcels table""" 

        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS parcels (
                orderID SERIAL PRIMARY KEY,
                destination VARCHAR(50) NOT NULL,
                pickupLocation VARCHAR(50) NOT NULL,
                parcelSize VARCHAR(50) NOT NULL,
                price integer NOT NULL,
                status VARCHAR(50) NOT NULL,
                userid SERIAL NOT NULL,
                created_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
            """
        )

        """create user table"""  
        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                userid SERIAL PRIMARY KEY, 
                name VARCHAR(50) NOT NULL,
                username VARCHAR(12) NOT NULL UNIQUE, 
                password VARCHAR(12) NOT NULL, 
                role VARCHAR(50) DEFAULT 'user',
                created_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                active BOOLEAN DEFAULT TRUE);
            """
        )
        
    def insert_data_parcels(self, data):
        """inserts values into table parcels"""

        try:
            self.cur.execute(
                """INSERT INTO parcels(destination, pickupLocation, parcelSize, price, status, userid) VALUES('{}', '{}', '{}', '{}', '{}', {})""".format(data['destination'], data['pickupLocation'], data['parcelSize'], data['price'], data['status'], data['userid'])
            )
            return True

        except Exception as ex:
            return format(ex)

    def getparcels(self):
        """get all parcels"""

        try:
            self.cur.execute(
                "SELECT * FROM parcels"
            )
            _parcels = self.cur.fetchall()
            return _parcels

        except:
            return False

    def getoneparcel(self, _orderID):
        """get one parcel"""

        try:
            self.cur.execute(
                "SELECT * FROM parcels WHERE orderID = %s", [_orderID]
            )
            return self.cur.fetchone()

        except:
            return False

    def getparcelsbyuser(self, _userid):
        """get one parcel"""

        try:
            self.cur.execute(
                "SELECT * FROM parcels WHERE userid = %s", [_userid]
            )
            _parcels = self.cur.fetchall()
            return _parcels

        except:
            return False

    def update_parcel(self, orderID, myorder):
        """update parcel data"""
        try:
            self.cur.execute(
                "UPDATE parcels SET destination='{}', pickupLocation='{}', parcelSize = '{}',\
                 price = '{}', status = '{}',\
                  updated_on=CURRENT_TIMESTAMP WHERE orderID = {}".format(myorder.destination,\
                   myorder.pickupLocation, myorder.parcelSize, myorder.price, myorder.status, orderID)
            )
            return True
        except Exception as ex:
            return format(ex)

    def add_user(self, user):
        """add users"""

        try:
            self.cur.execute(
                """
                INSERT INTO users(name, username, password) \
                VALUES('{}', '{}', '{}')
                """.format(user.name, user.username, user.password)
            )
            return True
        
        except Exception as ex:
            return format(ex)

    def update_user(self, user):
        """update users"""

        try:
            self.cur.execute(
                """UPDATE users set name='{}', username='{}', password='{}', role='{}' WHERE userid = '{}'""".format(user['name'], user['username'], user['password'], user['role'], user['userid'])
            )
            return True
        
        except Exception as ex:
            return format(ex)

    def default_user(self):
        """insert a default user"""

        try:
            self.cur.execute(
                """
                INSERT INTO users(name, username, password, role)\
                VALUES('john', 'hero', 'admin', 'user'),('admin', 'admin', 'admin', 'admin');
                """
            )
            return {"msg":"*** Created default user ***"}
        
        except Exception as ex:
            return {"defusr":format(ex)}

    def getUsers(self):
        """get all users"""
        try:
            self.cur.execute(
                "SELECT * FROM users WHERE active= TRUE"
            )
            _users = self.cur.fetchall()
            return _users

        except:
            return False

    def check_user_exists(self, username, password):
        """check if user exists"""

        try:
            self.cur.execute(
                "SELECT * FROM users WHERE username = '{}' AND password = '{}'\
                 AND active= TRUE" .format(username, password)
            )
            return self.cur.fetchone()
        
        except:
            return False

    def getoneUser(self, _userid):
        """get a user"""
        try:
            self.cur.execute(
                "SELECT * FROM users WHERE userid = %s AND active = TRUE", [_userid]
            )
            _users = self.cur.fetchone()
            return _users

        except Exception as ex:
            return {"gt1usr":format(ex), "userid":0}

    def getUserbyUsername(self, _username):
        """get a user"""

        try:
            self.cur.execute(
                "SELECT * FROM users WHERE username = '{}' AND active = TRUE".format(_username)
            )
            _users = self.cur.fetchone()
            return _users

        except Exception as ex:
            return {'gtsurbyUsrnm':format(ex), 'userid':0}

    def deleteuser(self, _userid):
        """delete user"""

        try:
            self.cur.execute(
                "UPDATE users SET active=FALSE, updated_on= CURRENT_TIMESTAMP WHERE\
                 userid = {}".format(_userid)
            )
        except:
            return False

    def truncate(self, _table):
        """delete user"""

        try:
            self.cur.execute(
                "TRUNCATE {}".format(_table)
            )
            return 'Deleted'
        except:
            return 'False'