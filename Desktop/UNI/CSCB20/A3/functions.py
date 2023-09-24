import sqlite3
from datetime import datetime
import pytz


def createTables():
  # connect to the database
  con = sqlite3.connect("database.db")
  cur = con.cursor()
  # create tables
  sql_query = """
      CREATE TABLE IF NOT EXISTS User 
      (
          userid integer PRIMARY KEY,
          username TEXT NOT NULL, 
          password TEXT NOT NULL,
          icon TEXT
      );
  """
  # execute the query
  cur.execute(sql_query)

  sql_query = """
      CREATE TABLE IF NOT EXISTS FriendRequests 
      (
          sender_id integer PRIMARY KEY, 
          receiver_id integer NOT NULL
      );
  """
  # execute the query
  cur.execute(sql_query)

  sql_query = """
      CREATE TABLE IF NOT EXISTS Friends 
      (
          userid1 integer, 
          userid2 integer
      );
  """
  # execute the query
  cur.execute(sql_query)

  sql_query = """
      CREATE TABLE IF NOT EXISTS Messages 
      (
          userid1 INTEGER, 
          userid2 INTEGER,
          message TEXT,
          timestamp TIMESTAMP PRIMARY KEY,
          actual_timestamp TEXT
      );
  """
  # execute the query
  cur.execute(sql_query)

  # sql_query = """

  # """
  # cur.execute(sql_query)

  sql_query = """
      CREATE TABLE IF NOT EXISTS Groups
      (
          groupid integer,
          userid integer FORIEGN KEY
      );
  """
  # execute the query
  cur.execute(sql_query)

  sql_query = """
      CREATE TABLE IF NOT EXISTS GroupInfo
      (
          groupid integer,
          groupname text FORIEGN KEY
      );
  """
  # execute the query
  cur.execute(sql_query)

  sql_query = """
      CREATE TABLE IF NOT EXISTS GroupMessages
      (
          groupid integer,
          userid text FORIEGN KEY,
          message TEXT,
          timestamp TIMESTAMP PRIMARY KEY,
          actual_timestamp TEXT
      );
  """
  # execute the query
  cur.execute(sql_query)


# uncomment if needed
# def resetTables():
#   TABLE_PARAMETER = "{TABLE_PARAMETER}"
#   DROP_TABLE_SQL = f"DROP TABLE {TABLE_PARAMETER};"
#   GET_TABLES_SQL = "SELECT name FROM sqlite_schema WHERE type='table';"
#   con = sqlite3.connect("database.db")

#   def delete_all_tables(con):
#     tables = get_tables(con)
#     delete_tables(con, tables)

#   def get_tables(con):
#     cur = con.cursor()
#     cur.execute(GET_TABLES_SQL)
#     tables = cur.fetchall()
#     cur.close()
#     return tables

#   def delete_tables(con, tables):
#     cur = con.cursor()
#     for table, in tables:
#       sql = DROP_TABLE_SQL.replace(TABLE_PARAMETER, table)
#       cur.execute(sql)
#     cur.close()

#   delete_all_tables(con)
#   createTables()

# def dropTable():
#   con = sqlite3.connect("database.db")
#   cur = con.cursor()
#   cur.execute("Drop table Groups")
#   cur.execute("Drop table GroupInfo")
#   cur.execute("Drop table GroupMessages")


def signin(login_username):
  # connect to the database
  con = sqlite3.connect("database.db")
  cur = con.cursor()
  # query
  sql_query = "SELECT username, password FROM User WHERE "
  sql_query += "username = '" + login_username + "';"
  # execute the query to fetch all the results as a list of tuples
  rows = cur.execute(sql_query).fetchall()
  # return the result
  return rows


def signup(signup_username, signup_password):
  # connect to the database
  con = sqlite3.connect("database.db")
  cur = con.cursor()
  # query
  sql_query = "INSERT INTO User(username, password, icon) VALUES ('"
  sql_query += signup_username + "','" + signup_password + "','" + "/images/default_icon.jpeg'" + ")"
  # execute the query
  cur.execute(sql_query)
  # commit the changes to the database
  con.commit()


def getUserId(username):
  # connect to the database
  con = sqlite3.connect("database.db")
  cur = con.cursor()
  # query
  sql_query = "SELECT userid FROM User WHERE "
  sql_query += "username = '" + username + "';"
  # execute the query to fetch all the results as a list of tuples
  output = cur.execute(sql_query).fetchall()
  # return the result
  if len(output) == 0:
    return -1
  return output[0][0]


def search(username):
  # connect to the database
  con = sqlite3.connect("database.db")
  cur = con.cursor()
  # query
  sql_query = "SELECT count(username) FROM User WHERE "
  sql_query += "username = '" + username + "';"
  # execute the query to fetch all the results as a list of tuples
  output = cur.execute(sql_query).fetchall()
  # return the result
  return output[0][0]


def notFriend(userid1, userid2):
  # connect to the database
  con = sqlite3.connect("database.db")
  cur = con.cursor()
  # query
  sql_query = "SELECT * FROM Friends WHERE "
  sql_query += "userid1 = " + str(userid1) + " and userid2 = " + str(
    userid2) + ";"
  # execute the query to fetch all the results as a list of tuples
  output1 = cur.execute(sql_query).fetchall()
  sql_query = "SELECT * FROM Friends WHERE "
  sql_query += "userid2 = " + str(userid1) + " and userid1 = " + str(
    userid2) + ";"
  output2 = cur.execute(sql_query).fetchall()
  # if not friends (0 relationship found)
  if len(output1) == 0 and len(output2) == 0:
    return True  # true that the users are NOT friends
  return False


def sendRequest(sender_id, receiver_id):
  # connect to the database
  con = sqlite3.connect("database.db")
  cur = con.cursor()
  # query
  sql_query = "INSERT INTO FriendRequests(sender_id, receiver_id) Values(" + str(
    sender_id) + ", " + str(receiver_id) + ");"
  # execute the query
  cur.execute(sql_query)
  # commit the changes to the database
  con.commit()


def loadRequests(receiver_id):
  # connect to the database
  con = sqlite3.connect("database.db")
  cur = con.cursor()
  # query
  sql_query = "SELECT U.username FROM FriendRequests FR join User U on FR.sender_id = U.userid WHERE "
  sql_query += "FR.receiver_id = " + str(receiver_id) + ";"
  # execute the query to fetch all the results as a list of tuples
  row = cur.execute(sql_query).fetchall()
  output = []
  # make requests box in Python and return it
  for sender in row:
    output.append(sender[0])
  return output


def acceptOrRefuse(sender_id, receiver_id, answer):
  # connect to the database
  con = sqlite3.connect("database.db")
  cur = con.cursor()
  # query
  sql_query = ''
  if answer == "Accept":
    # query
    sql_query = "INSERT INTO Friends(userid1, userid2) VALUES ("
    sql_query += str(sender_id) + ", " + str(receiver_id) + ");"
    # execute the query
    cur.execute(sql_query)
    # commit the changes to the database
    con.commit()
    cur = con.cursor()
  # query
  sql_query = "Delete FROM FriendRequests WHERE sender_id = "
  sql_query += str(sender_id) + " and receiver_id = " + str(receiver_id) + ";"
  # execute the query
  cur.execute(sql_query)
  # commit the changes to the database
  con.commit()


def loadFriends(cur_userid):
  # connect to the database
  con = sqlite3.connect("database.db")
  cur = con.cursor()
  # query
  sql_query = "SELECT U.username FROM Friends F join User U on F.userid1 = U.userid WHERE "
  sql_query += "F.userid2 = " + str(cur_userid) + ";"
  # execute the query to fetch all the results as a list of tuples
  row1 = cur.execute(sql_query).fetchall()
  # query
  sql_query = "SELECT U.username FROM Friends F join User U on F.userid2 = U.userid WHERE "
  sql_query += "F.userid1 = " + str(cur_userid) + ";"
  # execute the query to fetch all the results as a list of tuples
  row2 = cur.execute(sql_query).fetchall()
  output = []
  for friend in row1:
    output.append(friend[0])
  for friend in row2:
    output.append(friend[0])
  return output


def loadMessages(friend_id, user_id):
  # connect to the database
  con = sqlite3.connect("database.db")
  cur = con.cursor()
  # query
  sql_query = "SELECT U1.username, message, actual_timestamp FROM Messages M join User U1 on M.userid1 = U1.userid join User U2 on M.userid2 = U2.userid WHERE "
  sql_query += "userid1 = " + str(friend_id) + " and userid2 = " + str(
    user_id) + " or userid1 = " + str(user_id) + " and userid2 = " + str(
      friend_id) + " Order by timestamp ASC;"

  # execute the query to fetch all the results as a list of tuples
  messages = cur.execute(sql_query).fetchall()
  return messages


def writeMessage(user_id, friend_id, message):
  # get current time
  est = pytz.timezone('US/Eastern')
  now = datetime.now(est)
  current_date_time = now.strftime("%Y-%m-%d %H:%M:%S")
  # connect to the database
  con = sqlite3.connect("database.db")
  cur = con.cursor()
  # query
  sql_query = "INSERT INTO Messages VALUES ('"
  sql_query += str(user_id) + "','" + str(
    friend_id) + "','" + message + "', CURRENT_TIMESTAMP, '" + current_date_time + "');"
  # execute the query
  cur.execute(sql_query)
  # commit the changes to the database
  con.commit()


def createGroup(creator_id):
  # connect to the database
  con = sqlite3.connect("database.db")
  cur = con.cursor()
  # query
  sql_query = "SELECT count(groupid) from Groups"
  # execute the query to fetch all the results as a list of tuples
  result = cur.execute(sql_query).fetchall()
  # if there are existing groups
  if result[0][0] > 0:
    # query
    sql_query = "INSERT INTO Groups(groupid, userid) values((select max(groupid) from Groups) + 1, "
    sql_query += str(creator_id) + ");"
    # execute the query
    cur.execute(sql_query)
    # commit the changes to the database
    con.commit()
  # if there are no groups
  else:
    # query
    sql_query = "INSERT INTO Groups(groupid, userid) values(0, "
    sql_query += str(creator_id) + ");"
    # execute the query
    cur.execute(sql_query)
    # commit the changes to the database
    con.commit()

  #initialize a default name for a group
  sql_query = '''INSERT INTO GroupInfo(groupid, groupname) values((select max(groupid) from Groups),(select max(groupid) from Groups));'''
  # execute the query
  cur.execute(sql_query)
  # commit the changes to the database
  con.commit()


def writeGroupMessage(groupid, userid, message):
  # get current time
  est = pytz.timezone('US/Eastern')
  now = datetime.now(est)
  current_date_time = now.strftime("%Y-%m-%d %H:%M:%S")
  # connect to the database
  con = sqlite3.connect("database.db")
  cur = con.cursor()
  # query
  sql_query = "INSERT INTO GroupMessages VALUES ("
  sql_query += str(groupid) + "," + str(
    userid) + ",'" + message + "', CURRENT_TIMESTAMP, '" + current_date_time + "');"
  # execute the query
  cur.execute(sql_query)
  # commit the changes to the database
  con.commit()


def loadGroups(userid):
  # connect to the database
  con = sqlite3.connect("database.db")
  cur = con.cursor()
  # query
  sql_query = "SELECT G.groupid, GI.groupname FROM Groups G join GroupInfo GI on G.groupid = GI.groupid WHERE "
  sql_query += "userid = " + str(userid) + ";"
  # execute the query to fetch all the results as a list of tuples
  result = cur.execute(sql_query).fetchall()
  return result


def loadGroupMessages(groupid):
  con = sqlite3.connect("database.db")
  cur = con.cursor()
  # query
  sql_query = "SELECT U.username, G.message, G.actual_timestamp, U.icon FROM GroupMessages G join User U on G.userid = U.userid WHERE "
  sql_query += "G.groupid = " + str(groupid) + " Order by G.timestamp ASC;"
  # execute the query to fetch all the results as a list of tuples
  row = cur.execute(sql_query).fetchall()
  return row


def notInGroup(groupid, userid):
  # connect to the database
  con = sqlite3.connect("database.db")
  cur = con.cursor()
  # query
  sql_query = "SELECT * FROM Groups WHERE "
  sql_query += "groupid = " + str(groupid) + " and userid = " + str(
    userid) + ";"
  # execute the query to fetch all the results as a list of tuples
  output = cur.execute(sql_query).fetchall()
  #(0 relationship found)
  if len(output) == 0:
    return True  # true that the users are NOT in Group
  return False


def invite(groupid, userid):
  # connect to the database
  con = sqlite3.connect("database.db")
  cur = con.cursor()
  # query
  sql_query = "INSERT INTO Groups VALUES ("
  sql_query += str(groupid) + "," + str(userid) + ");"
  # execute the query
  cur.execute(sql_query)
  # commit the changes to the database
  con.commit()


def rename(groupid, groupname):
  # connect to the database
  con = sqlite3.connect("database.db")
  cur = con.cursor()
  # query
  sql_query = "UPDATE GroupInfo SET groupname = '" + groupname + "' WHERE groupid = " + str(
    groupid) + ";"
  # execute the query
  cur.execute(sql_query)
  # commit the changes to the database
  con.commit()


def delete(groupid):
  # connect to the database
  con = sqlite3.connect("database.db")
  cur = con.cursor()
  # query
  sql_query = "Delete FROM Groups WHERE groupid = " + str(groupid) + ";"
  # execute the query
  cur.execute(sql_query)
  # commit the changes to the database
  con.commit()
  # query
  sql_query = "Delete FROM GroupInfo WHERE groupid = " + str(groupid) + ";"
  # execute the query
  cur.execute(sql_query)
  # commit the changes to the database
  con.commit()
  # query
  sql_query = "Delete FROM GroupMessages WHERE groupid = " + str(groupid) + ";"
  # execute the query
  cur.execute(sql_query)
  # commit the changes to the database
  con.commit()


def getIcon(userid):
  # connect to the database
  con = sqlite3.connect("database.db")
  cur = con.cursor()
  # query
  sql_query = "SELECT icon FROM User WHERE userid = '" + str(userid) + "';"
  # execute the query to fetch all the results as a list of tuples
  result = cur.execute(sql_query).fetchall()
  icon_url = result[0][0]
  return icon_url


def updateProfile(userid, icon):
  # connect to the database
  con = sqlite3.connect("database.db")
  cur = con.cursor()
  # query
  sql_query = "UPDATE User SET icon = '" + icon + "' WHERE userid = " + str(
    userid) + ";"
  # execute the query
  cur.execute(sql_query)
  # commit the changes to the database
  con.commit()
