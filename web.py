from bottle import route, request, response, template, run, error

users = {'hi':'123'}

@route('/login')
def login():
    return '''
        <form action="/login" method="post">
            Username: <input name="username" type="text" />
            Password: <input name="password" type="password" />
            <input value="Login" type="submit" />
        </form>
        <br>
        <a href="/register">register</a>
    '''

#unhashed login
@route('/login', method='POST')
def do_login():
    username = request.forms.get('username')
    password = request.forms.get('password')
    print(username, password)
    if check_login(username, password):
        response.set_cookie("account", username, secret='some-secret-key')
        return "<p>Your login information was correct.</p>"
    else:
        return "<p>Login failed.</p>"

@route('/register')
def register():
    return '''
        <form action="/register" method="post">
            Username: <input name="username" type="text" />
            Password: <input name="password" type="password" />
            <input value="Register" type="submit" />
        </form>
        <br>
        <a href="/login">go back to login</a>
    '''

@route('/register', method='POST')
def do_register():
    username = request.forms.get('username')
    password = request.forms.get('password')
    print(username, password)
    return check_register(username, password)

# we need a data structure to store login information
def check_login(username,pwd):
    if users.get(username) == pwd:
        return True
    else:
        return False

def check_register(username,pwd):
    if users.get(username) != None:
        return '''<p>Username exists</p><br><a href="/register">go back</a>'''
    else:
        users.update({username:pwd})
        return '''<p>Your have registered.</p><br><a href="/login">go back</a>'''

@error(404)
def error404(error):
    return 'Nothing here, sorry'

run(host='localhost', port=8080, debug=True)