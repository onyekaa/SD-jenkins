import sqlite3
import datetime
from jenkinsapi.jenkins import Jenkins

def connectDB():
    # Connect to the DB
    try:
        db = sqlite3.connect('jenkindb')
        cursor = db.cursor()
        # If log table exists, open, else, create it
        cursor.execute('''CREATE TABLE IF NOT EXISTS
                          jenkinslog(id INTEGER PRIMARY KEY, name TEXT, status TEXT, retrieved TIME unique)''')
        db.commit()
        return db
    except Exception as e:
        db.rollback()
        raise e

def connectJenkins(url, username, password):
    # Connect to the server
    server = Jenkins(url, username = username, password = password)
    return server


def logJobs():
    # Your server details here
    server = connectJenkins('http://localhost:8080', '', '')
    conn = connectDB()

    # For each job found, we get its details and save to db

    for j in server.get_jobs():
        instance = j[1]
        job = instance.name
        running = instance.is_running()
        try:
            cursor = conn.cursor()
            conn.execute('''INSERT INTO jenkinslog(name, status, retrieved)
                              VALUES(?,?,?)''', (job, running, datetime.datetime.now()))
            conn.commit()
            print('Job "{}" inserted'.format(job))
        except Exception as e:
            conn.rollback()
            raise e

    conn.close()

if __name__ == '__main__':
    logJobs()
