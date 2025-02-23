# NeqSimAPI-client-python [![SNYK dependency check](https://github.com/equinor/NeqSimAPI-client-python/actions/workflows/snyk.yml/badge.svg?branch=main)](https://github.com/equinor/NeqSimAPI-client-python/actions/workflows/snyk.yml)
A python package to simplify calling NeqSimAPI for end-users handling authentication.  

See https://neqsimapi.app.radix.equinor.com/docs for available endpoints.

# Usage
See [https://github.com/equinor/neqsimapi-client-python/blob/main/example/demo.py](/example/demo.py) for a simple demo that connects and gets data from NeqSimAPI.

A short snippet is seen below
```python
from neqsimapi_connector.Connector import Connector as neqsim_api_connector

data = {
          "fluid": "CO2",
          "initial_temperature": 25,
          "initial_pressure": 15
        }


c = neqsim_api_connector()
res = c.post_result("DEMO/demo-process", data=data)
print(res)
```

# Install using pip
Usage of NeqSimAPI is limited to equinor users, but the package is available on pip.  
```python -m pip install neqsimapi_connector```
