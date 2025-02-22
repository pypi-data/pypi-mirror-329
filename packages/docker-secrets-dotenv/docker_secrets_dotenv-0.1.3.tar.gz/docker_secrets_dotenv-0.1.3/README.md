# docker-secrets-dotenv

![docker-secrets-dotenv-ver](https://img.shields.io/pypi/v/docker-secrets-dotenv)
![pythonver](https://img.shields.io/badge/python-3.9%2B-blue.svg)
![license](https://img.shields.io/github/license/mashape/apistatus.svg)

docker-secrets-dotenv takes all your docker secrets files, and sets them up in the environment.

## Getting Started

`pip install docker-secrets-dotenv`

To use docker-secrets-dotenv in your project run `load_secrets` as the start of your application:

```python
from docker_secrets import load_secrets

load_secrets() 
# This will load all secret files found in /run/secrets into the running environment
```

`load_secrets` will take the name of each secret file to set as the variable key and read the file contents as the value. It will overwrite existing environment variables.

There is an optional argument you can pass to remove the suffix of the secret when loading in the the environment:

```python
from docker_secrets import load_secrets

load_secrets(remove_suffix="_FILE") 
# This will load all secret files found in /run/secrets into the running environment 
# after removing "_FILE" from the end of the secrets file name.
# /run/secrets/API_KEY_FILE will exist in the environment as API_KEY
```

This is mostly because I am lazy and don't want to update my existing secrets that follow the _FILE convention set by other docker images, or write my code in a way that checks for both variations with and without the suffix.
