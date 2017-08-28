from bottle import route, request, response, template, run, error

@route('/login')
def login():
    return '''
        <form action="/login" method="post">
            Username: <input name="username" type="text" />
            Password: <input name="password" type="password" />
            <input value="Login" type="submit" />
        </form>
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

# we need a data structure to store login information
def check_login(username,pwd):
    if username == 'hi' and pwd == '123':
        return True
    else:
        return False

@error(404)
def error404(error):
    return 'Nothing here, sorry'

run(host='localhost', port=8080, debug=True)