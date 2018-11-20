
"""Database models"""
from flask import Flask, jsonify
import psycopg2
import os
from psycopg2.extras import RealDictCursor
from pprint import pprint
import datetime
from app.__init__ import app

class DatabaseConnection:
    """Connect to the database"""
    def __init__(self):
        self.database = "sendit_test_db"

        try:
            self.conn = psycopg2.connect(host="localhost", 
                                            database=self.database, 
                                            user="postgres", 
                                            password="joel",
                                            port="5432")
                                        
            self.cur = self.conn.cursor(cursor_factory=RealDictCursor)
            self.conn.autocommit = True
            pprint ('****INFO****: Database connection successfuly created')

        except psycopg2.DatabaseError as dberror:
            pprint (dberror)

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
                role VARCHAR(15) DEFAULT 'user',
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
            _parcels = self.cur.fetchone()
            return _parcels

        except:
            return False

    def getparcelsbyuser(self, _userid):
        """get one parcel"""

        try:
            self.cur.execute(
                "SELECT * FROM parcels WHERE userid = %s", [_userid]
            )
            _parcels = self.cur.fetchone()
            return _parcels

        except:
            return False

    def updateparcelstatus(self, _orderID, _status):
        """delete one parcel"""
        try:
            self.cur.execute(
                "UPDATE parcels SET status={} , updated_on =CURRENT_TIMESTAMP\
                 WHERE orderID = {}".format(_status, _orderID
                )
            )
        except:
            return False

    def check_parcel_exists_id(self, orderID):
        """check if parcel exists"""

        try:
            self.cur.execute(
                "SELECT * FROM parcels WHERE orderID = %s", [orderID]) 
            return self.cur.fetchone()

        except:
            return False

    def update_parcel(self, destination, pickupLocation, parcelSize,
                       price, status, userid, orderID):
        """update parcel data"""
        try:
            self.cur.execute(
                "UPDATE parcels SET destination='{}', pickupLocation={}, parcelSize = '{}',\
                 price = '{}', status = '{}', userid = '{}',\
                  date_updated=CURRENT_TIMESTAMP WHERE orderID = {}".format(destination,\
                   pickupLocation, parcelSize, price, status, userid, orderID)
            )

        except:
            return False
    
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

    def default_user(self):
        """insert a default user"""

        try:
            self.cur.execute(
                """
                INSERT INTO users(name, username, password)\
                VALUES('admin', 'admin', 'admin');
                """
            )
            return {"msg":"*** Created default user ***"}
        
        except Exception as ex:
            return {"msg":format(ex)}

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
            return {"msg":format(ex), "userid":0}

    def getUserbyUsername(self, _username):
        """get a user"""

        try:
            self.cur.execute(
                "SELECT * FROM users WHERE username = '{}' AND active = TRUE".format(_username)
            )
            _users = self.cur.fetchone()
            return _users

        except Exception as ex:
            return {'msg':format(ex), 'userid':0}

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
