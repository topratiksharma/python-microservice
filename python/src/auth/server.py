import jwt
import datetime
import os
from flask import Flask, request
from flask_mysqldb import MySQL

server = Flask(__name__)
mysql = MySQL(server)

# config
server.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST")
server.config["MYSQL_USER"] = os.environ.get("MYSQL_USER")
server.config["MYSQL_PASSWORD"] = os.environ.get("MYSQL_PASSWORD")
server.config["MYSQL_DB"] = os.environ.get("MYSQL_DB")
server.config["MYSQL_PORT"] = os.environ.get("MYSQL_PORT")


@server.route("/login", methods=["POST"])
def login():
    auth = request.authorization
    # auth.username
    # auth.password
    if not auth:
        return "missing credentials", 401

    # check db for username and password
    cur = mysql.connection.cursor()

    res = cur.execute(
        "SELECT email,password FROM users WHERE email = %s", (auth.username,)
    )
    if res > 0:
        user_row = cur.fetchone()
        email = user_row[0]
        password = user_row[1]
        if auth.username == email and auth.password == password:
            createJWT(auth.username, os.environ.get("JWT_SECRET"), True),
        else:
            return "invalid credentials", 401
    else:
        return "invalid credentials", 401



def createJWT(username, secret, authz):
    return jwt.encode(
        {
            "username": username,
            "exp": datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(days=1),
            "admin": authz,
            "iat": datetime.datetime.now(tz=datetime.timezone.utc),
        },
        secret,
        algorithm="HS256",
    )

if __name__ == "__main__":
    print(__name__)