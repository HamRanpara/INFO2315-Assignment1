from bottle import route, run, Bottle, template, request, get, post
from bottle import static_file,error

app = Bottle()

@route('/')
@route('/hello/<name>')
def greeting():
    return template('Hello {{name}}, how are you?')

@get('/login')
def login():
    return '''
    <form action="/login" method="post">
        Username: <input name="username" type="text"/>
        Password: <input name="password" type="password"/>
    <input value="Login" type="submit"/>
    </form>
    '''

@post('/login')
def do_login():
    username = request.forms.get('username')
    password = request.forms.get('password')
    if check_login(username, password):
        return "<p>Your login information is valid.</p>"
    else:
        return "<p>Login fail.</p>"

@error(404)
def error404(error):
    return 'Nothing here, sorry'

# @route('/static/<filename>')
# def server_static(filename):
#     return static_file(filename, root='')
#
run(host='localhost', port=8080, debug=True)