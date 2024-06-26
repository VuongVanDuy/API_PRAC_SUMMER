import sqlite3
import hashlib
import re

class DbManagerUser:
    def __init__(self, database_name):
        try:
            self.conn = sqlite3.connect(database_name)
            self.cursor = self.conn.cursor()
        except Exception as e:
            print(e)
        # self.create_table_user()
        # self.create_table_review_of_user()

    def create_table_user(self):
        try:
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS user(
                                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                    username VARCHAR(20) UNIQUE NOT NULL, 
                                    password VARCHAR(3000) NOT NULL,
                                    link_icon VARCHAR(100) NOT NULL
                                );''')
            self.conn.commit()
        except Exception as e:
            print(e)
        
    def insert_user(self, username, password, link_icon):
        check_name = bool(re.match(r'^[a-zA-Z0-9_]+$', username))
        check_pass = bool(re.match(r'^[a-zA-Z0-9_]+$', password))
        if not check_name or not check_pass:
            return False
        try:
            password_bytes = password.encode('utf-8')
            sha256 = hashlib.sha256()
            sha256.update(password_bytes)
            hash_password = sha256.hexdigest()
    
            self.cursor.execute('''INSERT INTO user(username, password, link_icon) 
                                VALUES (?, ?, ?)''', (username, hash_password, link_icon))
            self.conn.commit()
            return True
        except Exception as e:
            print(e)
            return False
            
    def create_table_review_of_user(self):
        try:
            self.cursor.execute('''CREATE TABLE review_of_user(
                                    id_user	INTEGER,
                                    id_route INTEGER,
                                    star_vote INTEGER NOT NULL,
                                    comment	VARCHAR(100) NOT NULL,
                                    time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                                    PRIMARY KEY("id_user","id_route"),
                                    FOREIGN KEY("id_user") REFERENCES "user"("id")
                                );''')
            self.conn.commit()
        except Exception as e:
            print(e)
        
    def insert_review_of_user(self, id_user, id_route, star_vote, comment):
        check_id_user = isinstance(id_user, int)
        check_id_route = isinstance(id_route, int)
        if not check_id_user or not check_id_route:
            return None
        try:
            self.cursor.execute(''' INSERT INTO review_of_user (id_user, id_route, star_vote, comment, time)
                                    VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
                                    ON CONFLICT(id_user, id_route) 
                                    DO UPDATE SET
                                        star_vote = excluded.star_vote,
                                        comment = excluded.comment,
                                        time = CURRENT_TIMESTAMP;''', (id_user, id_route, star_vote, comment))
            self.conn.commit()
            return True
        except Exception as e:
            print(e)
            return False
    
    def update_link_icon(self, name_user, link_icon):
        check_name = bool(re.match(r'^[a-zA-Z0-9_]+$', name_user))
        if not check_name:
            return False
        try:
            self.cursor.execute("UPDATE user SET link_icon = ? WHERE username = ?", (link_icon, name_user))
            self.conn.commit()
        except Exception as e:
            print(e)
    
    def update_password(self, name_user, password):
        check_name = bool(re.match(r'^[a-zA-Z0-9_]+$', name_user))
        check_pass = bool(re.match(r'^[a-zA-Z0-9_]+$', password))
        if not check_name or not check_pass:
            return False
        try:
            password_bytes = password.encode('utf-8')
            sha256 = hashlib.sha256()
            sha256.update(password_bytes)
            hash_password = sha256.hexdigest()
            self.cursor.execute("UPDATE user SET password = ? WHERE username = ?", (hash_password, name_user))
            self.conn.commit()
            return True
        except Exception as e:
            print(e)
            return False
    
    def get_password(self, name_user):
        check_name = bool(re.match(r'^[a-zA-Z0-9_]+$', name_user))
        if not check_name:
            return None
        try:
            self.cursor.execute("SELECT password FROM user WHERE username = ?", (name_user,))
            return self.cursor.fetchone()[0]
        except Exception as e:
            return None
        
    def get_link_icon(self, name_user):
        check_name = bool(re.match(r'^[a-zA-Z0-9_]+$', name_user))
        if not check_name:
            return None
        try:
            self.cursor.execute("SELECT link_icon FROM user WHERE username = ?", (name_user,))
            return self.cursor.fetchone()[0]
        except Exception as e:
            return None
    
    def get_time_review_route(self, user_name, id_route):
        check_name = bool(re.match(r'^[a-zA-Z0-9_]+$', user_name))
        check_id_route = isinstance(id_route, int)
        if not check_name or not check_id_route:
            return None
        try:
            sql = '''SELECT review_of_user.time
                    FROM review_of_user
                    WHERE review_of_user.id_user = (
                        SELECT id
                        FROM user
                        WHERE username = ?
                    )
                    AND review_of_user.id_route = ?;
                    '''
            self.cursor.execute(sql, (user_name, id_route))
            return self.cursor.fetchone()[0]
        except Exception as e:
            return None
    
    def get_id_user(self, name_user):
        check_name = bool(re.match(r'^[a-zA-Z0-9_]+$', name_user))
        if not check_name:
            return None
        try:
            self.cursor.execute("SELECT id FROM user WHERE username = ?", (name_user,))
            return self.cursor.fetchone()[0]
        except Exception as e:
            return None
    
    # def fetch_all_users(self):
    #     try:
    #         self.cursor.execute("SELECT * FROM user")
    #         users = self.cursor.fetchall()
    #         result = []
    #         for user in users:
    #             info = {
    #                 'id': user[0],
    #                 'username': user[1],
    #                 'password': user[2],
    #                 'link_icon': user[3]
    #             }
    #             result.append(info)
    #         return result
    #     except Exception as e:
    #         print(e)
    #         return None

    def fetch_all_reviews_of_route(self, id_route):
        check_id_route = isinstance(id_route, int)
        if not check_id_route:
            return None
        try:
            sql = '''SELECT user.username, review_of_user.star_vote, review_of_user.comment, review_of_user.time, user.link_icon
                    FROM review_of_user
                    INNER JOIN user ON review_of_user.id_user = user.id
                    WHERE review_of_user.id_route = ?;
                    '''
            self.cursor.execute(sql, (id_route,))
            reviews = self.cursor.fetchall()
            result = []
            for review in reviews:
                info = {
                    'username': review[0],
                    'star_vote': review[1],
                    'comment': review[2],
                    'time': review[3],
                    'link_icon': review[4]
                }
                result.append(info)
            return result
        except Exception as e:
            print(e)
            return None
    
    def fetch_all_reviews_of_user(self):
        try:
            self.cursor.execute("SELECT * FROM review_of_user;")
            reviews = self.cursor.fetchall()
            result = []
            for review in reviews:
                info = {
                    'id_user': review[0],
                    'id_route': review[1],
                    'star_vote': review[2],
                    'comment': review[3],
                    'time': review[4]
                }
                result.append(info)
            return result
        except Exception as e:
            return None

    def close(self):
        self.conn.close()