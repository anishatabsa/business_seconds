
# business_seconds

This is a Pyramid service which exposes a REST endpoint to get business seconds between a specified start time and end time in ISO format.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

What things you need to install the software and how to install them

```
Python 3.7.2
waitress
pyramid
```

### Installing and running the service

A step by step series of examples that tell you have to get a development env running

1. Create a virtual environment.
```
$ virtualenv -p`which python3.7.2` venv
$ source venv/bin/activate
```
2. Upgrade packaging tools.
```
$ pip install --upgrade pip -e .
```
3. Execute the following script file.
This script should run the pserve command which will run a local Http server using waitress. Once you see the message  Serving on http://0.0.0.0:7000, you will be able to access the endpoint using http://localhost:7000/get_business_seconds?start_time=2021-06-16T17:20:47&end_time=2021-06-17T10:26:47 
```
./scripts/deploy.sh"
```


End with an example of getting some data out of the system or using it for a little demo
```
URL: http://localhost:7000/get_business_seconds?start_time=2021-06-16T17:20:47&end_time=2021-06-17T10:26:47
Method: GET
Query Parameters:
start_time = 2021-06-16T17:20:47
end_time = 2021-06-17T10:26:47

Reponse:
{
    "business_seconds": 8807
}
```
## Running the tests

### Interacting with the service
Using a generated bravado client
```python
from bravado.client import SwaggerClient
business_seconds_client = SwaggerClient.from_url(
    'http://localhost:7000/swagger.json',
    config={'use_models': False}
)
result = business_seconds_client.hello.get_hello(target='what').result()
```
Using curl
```bash
curl http://localhost:7000/get_business_seconds?start_time=2021-06-16T17:20:47&end_time=2021-06-17T10:26:47
```


* [Pyramid](http://docs.pylonsproject.org/projects/pyramid/en/latest/) - The web framework used
* [Swagger](http://swagger.io/) - API description
