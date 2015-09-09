# Two-factor Flask

![QR Code](http://chart.apis.google.com/chart?cht=qr&chs=250x250&chl=https%3A%2F%2Fgithub.com%2Fjosephabrahams%2Ftwo-factor-flask)

## Overview

Use the QR code on the home page to authenticate with your two-factor device.

Submit a POST request to `/` with a JSON payload using the two-factor code as your username.

If you successfully logged in, you should see a response that looks like:

```json
{
  "message": "Success",
  "request": {
    "foo": "bar"
  }
}
```

## Demo

Visit [two-factor-flask.herokuapp.com](https://two-factor-flask.herokuapp.com/):

    curl --data '{"foo":"bar"}' -u {{ code }}:'' https://two-factor-flask.herokuapp.com

## Development

### Requirements

- [Foreman](https://github.com/ddollar/foreman) or similar

### Setup Local Environment

    $ pip install -r requirements.txt

    $ echo "DEBUG=True" >> .env
    $ echo "DEVEL=True" >> .env
    $ echo "PORT=5000" >> .env
    $ echo "SECRET=`python app.py generatesecrete`" >> .env
    $ echo "WEB_CONCURRENCY=2" >> .env

### Local Development

    $ foreman start
    $ open http://localhost:5000
