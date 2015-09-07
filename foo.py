from os import environ
from functools import wraps
from urllib.parse import urlencode
import re

from flask import Flask, abort, make_response, render_template, request
import click
import pyotp


# CONFIG

FLASK_ENV = environ.get('FLASK_ENV', 'production')
PORT = environ.get('PORT', '8000')
SECRET = environ.get('SECRET')
APP_HOST = environ.get('APP_HOST')
TOR_HOST = environ.get('TOR_HOST')
AUTH_USERNAME = environ.get('AUTH_USERNAME', 'isl')
AUTH_PASSWORD = environ.get('AUTH_PASSWORD', pyotp.random_base32())

DEBUG = environ.get('DEBUG', 'False').lower() == 'true'


class SettingError(Exception):
    pass

if not SECRET.__len__() == 16 or not re.match('[A-Za-z0-9]+$', SECRET):
    ex = SettingError('$SECRET must be a 16 character base32 encoded string.')
    raise ex


# CREATE THE APPLICATION

app = Flask(__name__)
app.config.from_object(__name__)


# AUTHENTICATION

def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """

    totp = pyotp.TOTP(SECRET)
    code = totp.now()

    return username == AUTH_USERNAME and \
        password == code or password == AUTH_PASSWORD


def authenticate():
    """Sends a 401 response that enables basic auth"""
    response = make_response('', 401)
    response.headers['WWW-Authenticate'] = 'Basic realm="Login Required"'
    return response


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated


# ROUTES

@app.route('/')
def index():
    host = 'http://chart.apis.google.com/chart'
    query = {}
    query['cht'] = 'qr'
    query['chs'] = '250x250'
    if request.host == APP_HOST:
        query['chl'] = 'http://{}/'.format(TOR_HOST)
    elif request.host == TOR_HOST:
        query['chl'] = 'otpauth://totp/POST:{}@{}/apply/?secret={}'\
            .format(AUTH_USERNAME, APP_HOST, SECRET)
    else:
        abort(404)
    url = '{}?{}'.format(host, urlencode(query))
    return render_template('index.html', url=url)


def clean_application(request):
    data = request.data
    print(dir(data))
    if True:
        response = "You're hired!"
    else:
        pass
    return(response)


@app.route('/apply', methods=['POST'])
@requires_auth
def apply_no_slash():
    return(clean_application(request))


@app.route('/apply/', methods=['POST'])
@requires_auth
def apply():
    return(clean_application(request))


# USE CLICK TO CREATE A CLI

@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    if ctx.invoked_subcommand is None:
        runserver()


@cli.command(help='Print a 16 character base32 secret')
def generatesecret():
    click.echo(pyotp.random_base32())


@cli.command(help='Starts a lightweight development server')
def runserver():
    if FLASK_ENV == 'development':
        app.run()
    else:
        """
        meinheld is wicked fast!
        See: https://github.com/methane/meinheld
        """
        from meinheld import server, middleware
        server.listen(("0.0.0.0", int(PORT)))
        server.run(middleware.WebSocketMiddleware(app))

if __name__ == '__main__':
    cli()
