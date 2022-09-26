import mysql.connector
from dotenv import dotenv_values


class MySQLClient:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host="mysql",
            user=dotenv_values("MYSQL_USERNAME"),
            password=dotenv_values("MYSQL_PASSWORD"),
            database='db'
        )

        self.cursor = self.connection.cursor()

    def read_common_data(key):
        sql = "SELECT * FROM common WHERE key = %s"
        self.cursor.execute(sql, key)

        res = []
        for item in self.cursor.fetchall():
            res.append({
                "key": item[0],
                "value": item[1]
            })

        return res

    def write_common_data(key, value):
        sql = "INSERT INTO common (key, value) VALUES (%s, %s) ON DUPLICATE KEY UPDATE value = %s"
        val = (key, value, value)
        self.cursor.execute(sql, val)

        self.connection.commit()
