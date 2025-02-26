# f5xc-tops-py-client

## 👋🏻 About
This package is low level python client to interact with the F5 Distributed Cloud API.


## 👷 Build and Version
Package is built via [Github Action](./.github/workflows/package.yml) and published to [pypi](https://pypi.org/project/f5xc_tops_py_client/).
Versioning is currently ad-hoc.

## 📋 Usage Examples
```shell
>>> from f5xc_tops_py_client import session, ns
>>> api = session(tenant_url="https://tenant.console.ves.volterra.io", api_token="dLsJqnSsgxxxxxxxxxxxxxxr=")
>>> r = ns(api).list()
>>> print(r)
```

## Reference
- Based on the [uplink](https://uplink.readthedocs.io/en/stable/user/quickstart.html) library


## 🛢️ XC Resource Coverage
