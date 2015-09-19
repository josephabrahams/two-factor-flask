# Two-factor Flask

![QR Code](http://chart.apis.google.com/chart?cht=qr&chs=250x250&chl=https%3A%2F%2Fgithub.com%2Fjosephabrahams%2Ftwo-factor-flask)

## Overview

Use the QR code on the demo site to authenticate with your two-factor device.
Use the form to submit the generated verification code and see the appropriate response.

```json
{
  "message": "Success"
}
```

## Demo

Visit [two-factor-flask.herokuapp.com](https://two-factor-flask.herokuapp.com/).

    curl --data 'code=XXXXXX' https://two-factor-flask.herokuapp.com

## Development

### Requirements

- [Foreman](https://github.com/ddollar/foreman) or similar

### Setup Local Environment

    $ pip install -r requirements.txt

    $ echo "DEBUG=True" >> .env
    $ echo "DEVEL=True" >> .env
    $ echo "PORT=5000" >> .env
    $ echo "WEB_CONCURRENCY=2" >> .env

### Local Development

    $ foreman start
    $ open http://localhost:5000
