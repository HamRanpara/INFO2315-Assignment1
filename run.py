from bottle import route, get, run, post, request, redirect, static_file
from Crypto.Hash import MD5
import re
import string
import numpy as np

#-----------------------------------------------------------------------------
# This class loads html files from the "template" directory and formats them using Python.
# If you are unsure how this is working, just
class FrameEngine:
    def __init__(this,
        template_path="templates/",
        template_extension=".html",
        **kwargs):
        this.template_path = template_path
        this.template_extension = template_extension
        this.global_renders = kwargs

    def load_template(this, filename):
        path = this.template_path + filename + this.template_extension
        file = open(path, 'r')
        text = ""
        for line in file:
            text+= line
        file.close()
        return text

    def simple_render(this, template, **kwargs):
        template = template.format(**kwargs)
        return  template

    def render(this, template, **kwargs):
        keys = this.global_renders.copy()
        #Not the best way to do this
        # but backwards compatible from PEP448, in Python 3.5+ use keys = {**this.global_renters, **kwargs}
        keys.update(kwargs)
        template = this.simple_render(template, **keys)
        return template

    def load_and_render(this, filename, header="header", tailer="tailer", **kwargs):
        template = this.load_template(filename)
        rendered_template = this.render(template, **kwargs)
        rendered_template = this.load_template(header) + rendered_template
        rendered_template = rendered_template + this.load_template(tailer)
        return rendered_template

#-----------------------------------------------------------------------------

# Allow image loading
@route('/img/<picture>')
def serve_pictures(picture):
    return static_file(picture, root='src/')

# Allow CSS
@route('css/<css>')
def serve_css(css):
    return static_file(css, root='static/css/')

# Allow javascript
@route('js/<js>')
def serve_js(js):
    return static_file(js, root='static/js/')

#-----------------------------------------------------------------------------

# Check the login credentials
def check_login(username, password):
    login = False
    err_str = "Incorrect credentials"
    logins = open("fake_database/logins")
    #passwords are hashed using part of the password as salt
    hashed_password = ""
    if len(password) < 5:
        hashed_password = password
    else:
        hashed_password = MD5.new(password[1:4].encode()).hexdigest()
        hashed_password = hashed_password + password
        hashed_password = MD5.new(hashed_password.encode()).hexdigest()
    for account in logins:
        #get username and passwords from file
        uname, pword = account.split(',', 1)
        pword = pword.rstrip()
        #approve login if username and passwords match
        if username == uname and hashed_password == pword:
            err_str = "Logged in as " + username
            login = True

    logins.close()
    return err_str, login

#-----------------------------------------------------------------------------

# Check if the username is taken
def check_valid_username(username):
    valid = True
    msg = "Registerd successfully!"
    if username == "" or ',' in username or '\\' in username:
        valid = False
        msg = "Invalid username: May contain illegal characters"
        return msg, valid
    logins = open("fake_database/logins")
    for login in logins:
        uname = login.split(',', 1)[0]
        if username == uname:
            msg = "Username taken"
            valid = False

    logins.close()
    return msg, valid

# Check if password is strong enough to be used
def check_valid_password(username, password):
    valid = True
    msg = "Registered successfully!"
    if len(password) < 8:
        valid = False
        msg = "Password must be at least 8 characters"
    elif username in password:
        valid = False
        msg = "Password and username are too similar"
    elif ',' in password or '\\' in password:
        valid = False
        msg = "Password contains invalid characters"
    else:
        lowercase = False
        uppercase = False
        number = False
        for character in password:
            if character in string.ascii_lowercase:
                lowercase = True
            elif character in string.ascii_uppercase:
                uppercase = True
            elif character in string.digits:
                number = True
        if not lowercase or not uppercase or not number:
            valid = False
            msg = "Password must contain at least: 1 uppercase character, 1 lowercase character, and 1 number"

    return msg, valid

#-----------------------------------------------------------------------------
# Redirect to login
@route('/')
@route('/home')
def index():
    return fEngine.load_and_render("index")

# Display the login page
@get('/login')
def login():
    return fEngine.load_and_render("login")

# Attempt the login
@post('/login')
def do_login():
    username = request.forms.get('username')
    password = request.forms.get('password')
    err_str, login = check_login(username, password)
    if login:
        return fEngine.load_and_render("valid", flag=err_str)
    else:
        return fEngine.load_and_render("invalid", reason=err_str)

# Register an account
@get('/register')
def register():
    return fEngine.load_and_render("register")

# Validate, and add (if valid) user to "database"
@post('/register')
def do_register():
    username = request.forms.get('username')
    password = request.forms.get('password')
    confirm_password = request.forms.get('confirm')
    # Default successful values
    msg = "Registerd successfully!"
    valid = True
    # Validate password
    msg, valid = check_valid_password(username, password)
    if not valid:
        return fEngine.load_and_render("invalid", reason=msg)
    valid = (password == confirm_password)
    if not valid:
        msg = "Passwords do not match"
        return fEngine.load_and_render("invalid", reason=msg)
    # Validate username
    msg, valid = check_valid_username(username)
    if not valid:
        return fEngine.load_and_render("invalid", reason=msg)

    # Add the user to the database
    logins = open("fake_database/logins", "a")
    hashed_password = MD5.new(password[1:4].encode()).hexdigest()
    hashed_password = hashed_password + password
    hashed_password = MD5.new(hashed_password.encode()).hexdigest()
    logins.write(username + "," + hashed_password + "\n")
    logins.close()
    # Display a success message
    return fEngine.load_and_render("valid", flag=msg)

@get('/about')
def about():
    garble = ["leverage agile frameworks to provide a robust synopsis for high level overviews.",
    "iterate approaches to corporate strategy and foster collaborative thinking to further the overall value proposition.",
    "organically grow the holistic world view of disruptive innovation via workplace diversity and empowerment.",
    "bring to the table win-win survival strategies to ensure proactive domination.",
    "ensure the end of the day advancement, a new normal that has evolved from generation X and is on the runway heading towards a streamlined cloud solution.",
    "provide user generated content in real-time will have multiple touchpoints for offshoring."]
    return fEngine.load_and_render("about", garble=np.random.choice(garble))

#-----------------------------------------------------------------------------

fEngine = FrameEngine()
run(host='localhost', port=8080, debug=True)
