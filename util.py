import pymysql


def getConnection():
  conn = pymysql.connect(
          host='localhost',
          user='root', 
          password = "cfqUZn7zu0qj1g==",
          db='avalaai',
          )
  return conn