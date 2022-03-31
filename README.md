# pyleo

Experimental project to assess feasibility of moving the
[pyleoclim](https://github.com/LinkedEarth/Pyleoclim_util) project to an
[extension type](https://pandas.pydata.org/pandas-docs/stable/development/extending.html#extension-types)
architecture.

## develop

To setup a development environment, with an activated virtual environment,
and in the root of the project (where `setup.cfg` lives) you can run:

```bash
$ python -m pip -e $(pwd)[dev]
```

This will install the dependencies required by the project, and the tools
needed for development (such as pytest).
