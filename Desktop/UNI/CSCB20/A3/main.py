from flask import Flask, render_template, request, redirect, url_for, flash, session

import sqlite3
from datetime import timedelta
import functions as fcn
from flask_bcrypt import Bcrypt
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = 'saohfaosif[jsdkvmmaas;'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(
  minutes=10000)  # configure how long to keep session
bcrypt = Bcrypt(app)  #  Python library for password hashing
ALLOWED_EXTENSIONS = set(['png', 'PNG', 'jpg', 'JPG'])
UPLOAD_FOLDER = 'static/images/user_icon/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
fcn.createTables()


@app.route('/', methods=['POST', 'GET'])
def home():
  if (request.method == 'POST'):
    # login
    if ('login_username' in request.form):
      # get data from the form
      login_username = request.form['login_username']
      login_password = request.form['login_password']
      # get data from the database
      rows = fcn.signin(login_username)
      # if no data received from the database
      if (len(rows) == 0):
        flash('User not found')
        return redirect(url_for('home'))
      # rows[0] is the row containing the username/password so rows[0][1] is the password value; check the hashed password with the password passed in
      elif (bcrypt.check_password_hash(rows[0][1], login_password) == False):
        flash('Your password is incorrect')
        return redirect(url_for('home'))
      # all good
      else:
        session['user'] = login_username
        session['userid'] = fcn.getUserId(login_username)
        # remember me
        checked = request.form.getlist('remember_me')
        if len(checked) > 0:
          session.permanent = True
        else:
          session.permanent = False
        return redirect(url_for('user', username=login_username))
    # signup
    else:
      # get data from the form
      signup_username = request.form['signup_username']
      if (fcn.getUserId(signup_username) != -1):
        flash('Username already exists')
        return redirect(url_for('home'))
      signup_password = request.form['signup_password']
      signup_confirm_password = request.form['signup_confirm_password']
      if signup_confirm_password == signup_password:
        # hash the password before storing it (get a byte string that represents the password)
        hashed_password = bcrypt.generate_password_hash(signup_password)
        # decode the byte string into a Unicode string to store in SQL; 'utf-8' is the character encoding
        hashed_password_str = hashed_password.decode('utf-8')
        # add the user to the database
        fcn.signup(signup_username, hashed_password_str)
        session['user'] = signup_username
        session['userid'] = fcn.getUserId(signup_username)
        return redirect(url_for('user', username=signup_username))
      else:
        flash('Your passwords do not match')
        return redirect(url_for('home'))
  else:
    # if the user is not signed in
    if 'user' not in session:
      # hide user and logout links and the welcome box
      status = 'display: none;'
      welcome_box = 'display: none;'
      return render_template('home.html',
                             status=status,
                             welcome_box=welcome_box)
    # if the user is signed in
    # hide the account system (sign in/sign out area)
    account_system = 'display: none;'
    return render_template('home.html', account_system=account_system)


@app.route('/logout')
def logout():
  # clear the session
  session.clear()
  return redirect(url_for('home'))


@app.route('/user/<username>', methods=['POST', 'GET'])
def user(username):
  # redirect to home page if not login
  if "user" not in session or "userid" not in session:
    return redirect(url_for('home'))
  cur_user = session['user']
  cur_userid = session['userid']
  # after successful authentication
  icon_url = fcn.getIcon(cur_userid)
  session['cur_icon'] = icon_url

  if (request.method == 'POST'):
    # if creating group
    if "create_group_button" in request.form:
      fcn.createGroup(cur_userid)
      flash("Group created below")
    # change status when user clicks between options
    elif 'group_button' in request.form:
      group = request.form['group_id']  # group identifier
      groupname = request.form['group_button']
      session['group'] = group
      session['groupname'] = groupname
      session.pop('friend', None)
    elif 'friend_button' in request.form:
      friend = request.form['friend_button']  # friend identifier
      session['friend'] = friend
      session.pop('group', None)
      session.pop('groupname', None)
    # if inputted message
    elif 'messageInput' in request.form:
      # send messages
      message = request.form['messageInput']
      message = message.replace("'", "''")
      # private chat
      if 'friend' in session:
        try:
          fcn.writeMessage(cur_userid, fcn.getUserId(session['friend']),
                           message)
        except sqlite3.IntegrityError:
          flash("Sorry we could not send this message to " + session['friend'])
      # group chat
      elif 'group' in session:
        try:
          fcn.writeGroupMessage(session['group'], cur_userid, message)
        except sqlite3.IntegrityError:
          flash("Sorry we could not send this message in " + session['group'])
    # if accepting/refusing a friend request
    elif 'friend_req_button' in request.form:
      # get whether the user clicked accept or refuse
      answer = request.form['friend_req_button']
      if answer == 'Accept':
        flash(request.form["request"] + " is now your friend")
      else:
        flash("You refuse to be friends with " + request.form["request"])
      fcn.acceptOrRefuse(fcn.getUserId(request.form["request"]), cur_userid,
                         answer)

    # if sending friend request
    elif 'searchInput' in request.form:
      searchInput = request.form['searchInput']
      # can not find the user in database
      if (fcn.search(searchInput) == 0):
        flash("No such user")
      elif searchInput == session['user']:
        flash("Cannot add yourself")
      # already friends
      elif fcn.notFriend(fcn.getUserId(searchInput), cur_userid) == False:
        flash("Already in friend list")
      # found user and not friends, then send request
      else:
        try:
          # try to send it
          fcn.sendRequest(cur_userid, fcn.getUserId(searchInput))
          flash("Sent request")
        except sqlite3.IntegrityError:
          # already sent request
          flash("Sent request already")
    # invite someone into group
    elif 'inviteInput' in request.form:
      inviteInput = request.form['inviteInput']
      # verify that the users are friends
      if fcn.notFriend(fcn.getUserId(inviteInput), cur_userid) == True:
        flash("Not in friend list")
      elif fcn.notInGroup(session['group'],
                          fcn.getUserId(inviteInput)) == False:
        flash(f"{inviteInput} is in the group already")
      else:
        fcn.invite(session['group'], fcn.getUserId(inviteInput))
        flash("Sent invitation")
    elif 'renameInput' in request.form:
      renameInput = request.form['renameInput']
      fcn.rename(session['group'], renameInput)
      session['groupname'] = renameInput
    elif 'delete_Button' in request.form:
      renameInput = request.form['delete_Button']
      if renameInput == 'Yes':
        fcn.delete(session['group'])
        session.pop('group', None)
        session.pop('groupname', None)
    return redirect(url_for('user', username=username))
  # request.method == 'GET'
  else:
    # load stuff
    requests = fcn.loadRequests(cur_userid)
    friends = fcn.loadFriends(cur_userid)
    groups = fcn.loadGroups(cur_userid)
    action = "/user/" + cur_user
    return render_template('user.html',
                           action=action,
                           requests=requests,
                           friends=friends,
                           groups=groups,
                           icon_url=icon_url)


@app.route('/user/profile', methods=["GET", "POST"])
def upload_profile():
  cur_icon = ''
  # get userid from session
  userid = session['userid']
  # get icon_url by userid
  cur_icon = fcn.getIcon(userid)
  if request.method == "POST":
    if 'icon_upload' in request.files:
      file = request.files.get('icon_upload')
      # if there's a file and have file name
      if file and file.filename != '':
        # rename the file with username
        filename = session['user'] + '_icon_' + secure_filename(file.filename)
        # save the file to folder with its absolute path
        path = os.path.abspath(
          os.path.join(app.config['UPLOAD_FOLDER'], filename))
        file.save(path)
        # save the path in session
        session['cur_icon'] = f'/images/user_icon/{filename}'
        # get the latest icon from session
        cur_icon = session.get('cur_icon', '')
        # update the icon to database
        fcn.updateProfile(userid, cur_icon)
  return redirect(url_for('user', username=session['user']))


@app.route("/get_data")
def get_data():

  cur_user = session['user']
  cur_userid = session['userid']

  msgs = []
  is_group = False

  if 'friend' in session:
    # get messages and icon
    msgs = fcn.loadMessages(cur_userid, fcn.getUserId(session['friend']))
  elif 'group' in session:
    # get messages
    msgs = fcn.loadGroupMessages(session['group'])
    is_group = True

  output = ''
  for messageblock in msgs:
    if cur_user == messageblock[0]:
      # user_sent section
      output += f'''
      <div class="msg" id="user_sent">
        <div>
          <span class="sender_name" id="user_name">{cur_user} - {messageblock[2]}</span>
        </div>
        <div class="icon_and_message">
          <img id="user_icon" src="../static{fcn.getIcon(cur_userid)}">
      '''
    elif is_group == True:
      # group_sent section
      output += f'''
      <div class="msg" id="group_sent">
        <div>
          <span class="sender_name" id="member_name">{messageblock[0]} - {messageblock[2]}</span>
        </div>
        <div class="icon_and_message">
          <img id="member_icon" src="../static{messageblock[3]}">
      '''
    else:
      # friend_sent section
      output += f'''
      <div class="msg" id="friend_sent">
        <div>
          <span class="sender_name" id="friend_name">{messageblock[0]} - {messageblock[2]}</span>
        </div>
        <div class="icon_and_message">
          <img id="friend_icon" src="../static{fcn.getIcon(fcn.getUserId(session['friend']))}">
      '''
    output += f'''
        <ul>{messageblock[1]}</ul>
      </div>
    </div>
    '''

  return output


# *******************************************************************
# ALL CODE BELOW IS TEMPORARY
# *******************************************************************


@app.route('/userinfo')
def userinfo():
  con = sqlite3.connect("database.db")
  cur = con.cursor()
  sql_query = "SELECT * FROM User"
  rows = cur.execute(sql_query).fetchall()
  output = "<html><ul>"
  for next_user in rows:
    output += "<li>" + str(next_user[0]) + " - " + str(
      next_user[1]) + " - " + str(next_user[2]) + " - " + str(
        next_user[3]) + "</li>"
  output += "</ul></html>"
  return output  # print the data to the user


@app.route('/groups')
def groups():
  con = sqlite3.connect("database.db")
  cur = con.cursor()
  sql_query = "SELECT * FROM Groups"
  rows = cur.execute(sql_query).fetchall()
  output = "<html><ul>"
  for next_group in rows:
    output += "<li>" + str(next_group[0]) + " - " + str(
      next_group[1]) + "</li>"
  output += "</ul></html>"
  return output  # print the data to the user


@app.route('/groupinfo')
def groupinfo():
  con = sqlite3.connect("database.db")
  cur = con.cursor()
  sql_query = "SELECT * FROM GroupInfo"
  rows = cur.execute(sql_query).fetchall()
  output = "<html><ul>"
  for next_group in rows:
    output += "<li>" + str(next_group[0]) + " - " + str(
      next_group[1]) + "</li>"
  output += "</ul></html>"
  return output


@app.route('/friends')
def friends():
  con = sqlite3.connect("database.db")
  cur = con.cursor()
  sql_query = "SELECT * FROM Friends"
  rows = cur.execute(sql_query).fetchall()
  output = "<html><ul>"
  for next_group in rows:
    output += "<li>" + str(next_group[0]) + " - " + str(
      next_group[1]) + "</li>"
  output += "</ul></html>"
  return output  # print the data to the user


# used for reset some table in the database
@app.route('/reset_database')
def reset():
  fcn.dropTable()
  fcn.createTables()
  return redirect(url_for('home'))


app.run()
