[![Build Status](https://magnum.travis-ci.com/TAKEALOT/business_seconds.svg?token=zDUr6qSiwFsZyyUy1s7p&branch=master)](https://magnum.travis-ci.com/TAKEALOT/business_seconds)

# business_seconds

One Paragraph of project description goes here

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

What things you need to install the software and how to install them

```
Give examples
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
$ pip install --upgrade pip setuptools
```
3. Install all our requirements.
```
$ pip install -e ".[test]"
```

4. Build your project
```
eval $(minikube docker-env)
docker build -t image-registry.ci.env:80/takealot/business_seconds:master -f Dockerfile .
```

5. Run your project in kubernetes.
```
helm install -n business_seconds --set dev.patch=true,dev.hostPath=$PWD charts/business_seconds
```

End with an example of getting some data out of the system or using it for a little demo

## Running the tests

Explain how to run the automated tests for this system

```
export ROLE=TEST
py.test --cov=business_seconds tests/
```

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
curl http://localhost:7000/hello/what
```

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Pyramid](http://docs.pylonsproject.org/projects/pyramid/en/latest/) - The web framework used
* [Swagger](http://swagger.io/) - API description
