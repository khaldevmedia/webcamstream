# Python standard libraries
import sqlite3
from sqlite3 import Error

class Logger:
    def __init__(self, db_file):
        self.conn = None
        try:
            self.conn = sqlite3.connect(db_file)
        except Error as e:
            print(e)


    def __del__(self):
        self.conn.close()
        

    def close_conn(self):
        self.conn.close()
        

    def create_table(self):
        if self.conn is not None:
            try:
                c = self.conn.cursor()
                c.execute('''CREATE TABLE IF NOT EXISTS logs (
                                log_id INTEGER PRIMARY KEY,
                                user_ip TEXT NOT NULL,
                                date_time TEXT NOT NULL
                            );''')
            except Error as e:
                print(e)


    def create_log(self, log):
        sql = '''INSERT INTO logs(user_ip, date_time)
                 VALUES(?,?)'''
        cur = self.conn.cursor()
        cur.execute(sql, log)
        self.conn.commit()
        return cur.lastrowid


    def get_log_by_id(self, log_id):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM logs WHERE log_id=?", (log_id,))
        rows = cur.fetchall()
        return rows


    def get_all_logs(self):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM logs")
        logs = cur.fetchall()
        return logs


    def get_unique_ips(self):
        sql = '''SELECT user_ip,COUNT(*) as count 
                FROM logs 
                GROUP BY user_ip 
                ORDER BY count DESC;
                '''
        cur = self.conn.cursor()
        cur.execute(sql)
        ips = cur.fetchall()
        return ips
 

    def update_log(self, log):
        sql = '''UPDATE logs
                 SET user_ip = ? ,
                     date_time = ?
                 WHERE id = ?'''
        cur = self.conn.cursor()
        cur.execute(sql, log)
        self.conn.commit()


    def delete_log(self, id):
        sql = 'DELETE FROM logs WHERE log_id=?'
        cur = self.conn.cursor()
        cur.execute(sql, (log_id,))
        self.conn.commit()


def main():
    logger = Logger("test2_db.db")
    logger.create_table()

    # create a new log
    log = ('10.206.7.100', '2023-10-08 15:12:26')
    log_id = logger.create_log(log)
    print(log_id)

    # get a log by id
    log = logger.get_log_by_id(log_id)
    print(log)

    # update a log
    updated_log = ('2023-10-08 15:12:26', '10.206.7.100', log_id)
    logger.update_log(updated_log)

    # get the updated log
    log = logger.get_log_by_id(log_id)
    print(log)

    # delete a log
    logger.delete_log(log_id)

    # gat all the logs
    logs = logger.get_all_logs()
    print(logs)

if __name__ == '__main__':

    connection = sqlite3.connect('./log.db')
    # connection.row_factory = sqlite3.Row
    cursor = connection.execute('select * from logs')
    # instead of cursor.description:
    # row = cursor.fetchone()
    # names = row.keys()
    # print(names)

    logs = cursor.fetchall()
    print(logs)
    
    connection.close()

    # pass
    # main()
