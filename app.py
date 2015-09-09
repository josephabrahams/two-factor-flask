from os import environ
from functools import wraps
from urllib.parse import urlencode
import re

from flask import Flask, jsonify, make_response, render_template, request
import click
import pyotp


# CONFIG

DEBUG = environ.get('DEBUG', 'False').lower() == 'true'
DEVEL = environ.get('DEVEL', 'False').lower() == 'true'
PORT = environ.get('PORT', '8000')
SECRET = environ.get('SECRET')


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
    """ Check if a username:password combo is valid. """
    totp = pyotp.TOTP(SECRET)
    code = totp.now()

    return username == code


def authenticate():
    """ Sends a 401 response to enable basic auth """

    response = make_response(jsonify(message='Bad credentials'), 401)
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

@app.route('/', methods=['GET'])
def index_get():
    """ display the QR code """

    host = 'http://chart.apis.google.com/chart'
    query = {}
    query['cht'] = 'qr'
    query['chs'] = '250x250'
    query['chl'] = 'otpauth://totp/{}?secret={}'.format(request.host, SECRET)
    url = '{}?{}'.format(host, urlencode(query))

    return render_template('index.html', url=url)


@app.route('/', methods=['POST'])
@requires_auth
def index_post():
    """ if authenticated, process the POST request """

    response = {}
    response['message'] = 'Success'
    data = request.get_json(silent=True, force=True)
    if data:
        response['request'] = data

    return jsonify(response)


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
    if DEVEL:
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
