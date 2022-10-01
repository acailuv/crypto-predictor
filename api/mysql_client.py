import mysql.connector
import os


class MySQLClient:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host='db',
            user=os.environ.get("MYSQL_USERNAME"),
            password=os.environ.get("MYSQL_PASSWORD"),
            database='db'
        )

        self.cursor = self.connection.cursor()

    def read_common_data(self, key, cast_to=str):
        sql = "SELECT * FROM common WHERE `key` = %s"
        self.cursor.execute(sql, [key])

        res = []
        for item in self.cursor.fetchall():
            res.append({
                "key": item[0],
                "value": cast_to(item[1])
            })

        if len(res) < 1:
            print(
                f"[WARNING] Key {key} is not found. Making a default value {cast_to()}.")
            self.write_common_data(key, cast_to())
            return {
                "key": key,
                "value": cast_to()
            }

        return res[0]

    def write_common_data(self, key, value):
        sql = "INSERT INTO common (`key`, value) VALUES (%s, %s) ON DUPLICATE KEY UPDATE value = %s"
        val = (key, value, value)
        self.cursor.execute(sql, val)

        self.connection.commit()
