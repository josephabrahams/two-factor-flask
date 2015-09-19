from os import environ
from urllib.parse import urlencode
import re

from flask import Flask, abort, jsonify, render_template, request
import pyotp


# CONFIG

DEBUG = environ.get('DEBUG', 'False').lower() == 'true'
DEVEL = environ.get('DEVEL', 'False').lower() == 'true'
PORT = environ.get('PORT', '5000')
SECRET = environ.get('SECRET')

if not SECRET.__len__() == 16 or not re.match('[A-Za-z0-9]+$', SECRET):
    raise Exception('$SECRET must be a 16 character base32 encoded string.')


# CREATE THE APP

app = Flask(__name__)
app.config.from_object(__name__)


# ROUTES

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        """ process form submission """
        totp = pyotp.TOTP(SECRET)
        code = totp.now()

        if not request.form.get('code') == code:
            abort(401)

        return jsonify(message='Success')

    else:
        """ display the QR code """
        host = 'http://chart.apis.google.com/chart'
        query = {}
        query['cht'] = 'qr'
        query['chs'] = '250x250'
        query['chl'] = 'otpauth://totp/{}?secret={}'.format(request.host, SECRET)
        url = '{}?{}'.format(host, urlencode(query))

        return render_template('index.html', url=url)


# RUN THE APP

if __name__ == '__main__':
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
