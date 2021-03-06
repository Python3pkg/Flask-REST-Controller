# Flask-REST-Controller
---
[![Build Status](https://travis-ci.org/teitei-tk/Flask-REST-Controller.svg?branch=master)](https://travis-ci.org/teitei-tk/Flask-REST-Controller)

Flask-REST-Controller is added Class-Based-View(Controller) extension on [Flask](http://flask.pocoo.org/)   


## Features
* Follow the RESTful design
* provide of prepare authentication and request validation
	* other class based view library is not provided of validation
* uniform routing management
	* The existing functional view is difficult to manage. Definition routing Scattered
* JSON Response Validation with JSON Schema
	* It would be useful for creating an API :)


## Installation
```
$ pip install Flask-REST-Controller
```

## Usage

```python
from flask import Flask
from flask_rest_controller import Controller, set_routing

app = Flask(__name__)
app.secret_key = '\xcd\x8f\x10\x8a|\x10\t\xe8g<\xce|\xc7\xe6\xe3h\x8e\xd6\xfa\xc8i|\xee\xb0'


class JsonController(Controller):
    schema = {
        'GET': {
            'type': 'array',
            'properties': {
                'id':   {
                    'type': 'string'
                }
            }
        },
        'POST': {
            'type': 'object',
            'properties': {
                'result':   {
                    'type': 'string'
                },
                'code': {
                    'type': 'integer'
                }
            }
        }
    }

    def get(self):
        return self.render_json(["Hello World"])

    def post(self):
        return self.render_json({'result': "ok", 'code': 200})

ROUTING = [
    ("/", "app.JsonController", "json_controller"),
]

set_routing(app, ROUTING)

if __name__ == "__main__":
    app.run(debug=True)
```

Just save it as app.py and try 

```bash
$ python app.py
```

Now head over to http://127.0.0.1:5000/, and you should see your hello world of json string

You should see a post request result, try this command 

```bash
$ curl --request POST http://127.0.0.1:5000
```

You should see that you json in the post method

see https://github.com/teitei-tk/Flask-REST-Controller/tree/master/example For other examples

## Dependencies
* Python2.6 later
* jsonschema


## Contribute
1. Fork it
2. Create your feature branch (`git checkout -b your-new-feature`)
3. Commit your changes (`git commit -am 'Added some feature'`)
4. Push to the branch (`git push origin your-new-feature`)
5. Create a new Pull Request

## LICENSE
* MIT
