# Pyleo

Experimental project to assess feasibility of moving the
[pyleoclim](https://github.com/LinkedEarth/Pyleoclim_util) project to an
[extension type](https://pandas.pydata.org/pandas-docs/stable/development/extending.html#extension-types)
architecture.

## Development

To setup a development environment, with an activated virtual environment,
and in the root of the project (where `setup.cfg` lives) you can run:

```bash
$ python -m pip -e $(pwd)[dev]
```

This will install the dependencies required by the project, and the tools
needed for development (such as pytest).

## Design

This module contains three main components.

- A custom pandas data type
- A pandas extension array
- An accessor

## PyleoDatetimeDType

A pandas Series is wrapper around an array of elements of the same type.
This type is defined by what is named a data type or dtype in pandas, numpy
and other libraries of the ecosystem.

A dtype defines the information of what's stored in each position of the array,
so this information doesn't need to be repeated for each value, increasing
the amount of memory used, and CPU consumed when operations are performed.
This is different from regular Python, where each item in a list would contain
its own type.

An example of dtype could be `float64`. In this case, the type would be the same
in Python, in numpy or in pandas, but it'd still contain the information to know
how values in the array are represented.

In some cases, data types can have parameters. The most clear example is
`datetime64[ns]`. Where `ns` (nanoseconds) is the precision in which in which
datetimes will internally be stored, and could potentially be seconds, days,
or other units, even if currently only nanosecond precision is supported.

By using a custom data type for paleoclimate data, we can be explicit on the
data that is represented, add parameters, like the format in which the data
is stored (like thousands of years before the present time), and ensure the
data has the right representation (64 bits, timestamp with second precision,
etc.).

Data types in pandas have two equivalent representations. A class (a subclass
of `PandasExtensionDType`), and a string. The exact naming is something that
we should discuss and find what's the best, but the current prototype uses
the class `PyleoDatetimeDType` and the string `pyleo_dt` with a parameter
format, which currently only supports `kyr BP`.

## PyleoDatetimeArray

Historically, a pandas Series was developed as a wrapper around a numpy
array, which could be organized as dataframes, and with a large amount
of methods not included in numpy. Since not all data types that pandas
wanted to support could be represented as a single numpy array, the
extension array API was implemented. A Series then, is a wrapper around
a numpy array, or an extension array, which can be anything.

The extension array API is not the most mature or clear part of pandas,
but there are a large number of extension arrays already implemented.
For example datetimes with timezones, categories, or strings backed by Apache
Arrow, just to name few.

An extension array, has a data type associated to it, and contains most
of the functionality that pandas provides in a Series. For example, for
a numeric extension array, methods like `sum`, `mean`, `isna`, etc. should
be implemented.

For the use case of paleoclimate data, instead of starting the extension
array from scratch, we subclassed an existing datetime extension array from
pandas. The pandas extension array contains timezones and things that are
not needed, so we can consider abstracting a base class for both the
pandas datetime and the paleoclimate datetime. But we can make this work
either way.

In this first version, the main thing `PyleoDatetimeArray` implements is
the parsing of the input data, into the internal representation. Since the
format is known, as a parameter of the data type, this can be implemented
in the extension array. There are other ways to implement this, which are
worth considering. Like using a single format in the extension array,
and managing the formats externally (for example in functions like
`read_lipd(format='kyr BP')`). The current prototype doesn't fully
implement different formats, but contains code to illustrate the idea.

Since we are subclassing a working datetime extension array, functionality
like pandas `resample`, or any other pandas operation with datetimes
should also work for our custom array.

## PyleoAccessor

An accessor is just an API to organize functionality. For a pandas Series
there are around 200 methods and attributes, which are probably already
too many. For this reason, pandas implemented accessors, which help
group methods and attributes that are related. The most known example is
`dt`. For example, in `df['birthday'].dt.year`. While pandas makes use
of those accessors itself, creating accessors is something third-party
libraries are expected to implement when needed.

For the prototype, the accessor `pyleo` has been created. Functions could
be implemented as:

```python
import pyleo

pyleo.standardize(df['temperature'])
```

But with accessors, this becomes:

```python
df['temperature'].pyleo.standardize()
```

There is no functional difference, but code using accessors has two main
advantages:

- Syntax is more familiar to users of pandas
- It works with method chaining

Method chaining makes complex pipelines more readable by sorting them in
the order they are executed, not the reverse. For example:

```python
pyleo.spectral(pyleo.standardize(df['temperature']))
```

Could be written as:

```python
(df['temperature'].pyleo.standardize()
                  .pyleo.spectral())
```

The current prototype implements only accessors for Series, but
they can also be implemented for DataFrame.
