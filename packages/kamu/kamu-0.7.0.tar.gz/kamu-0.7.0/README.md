<div align="center">

<img alt="Kamu: Planet-scale data pipeline" src="https://raw.githubusercontent.com/kamu-data/kamu-client-python/refs/heads/master/docs/readme-files/kamu_logo.png" width=300/>

[Website] | [Docs] | [Demo] | [Tutorials] | [Examples] | [FAQ] | [Chat]

[![Crates.io](https://img.shields.io/pypi/v/kamu?logo=python&style=for-the-badge
)](https://pypi.org/project/kamu/)
[![Docs](https://img.shields.io/static/v1?logo=gitbook&logoColor=white&label=&message=Docs&color=gray&style=for-the-badge)](https://docs.kamu.dev/)
[![CI](https://img.shields.io/github/actions/workflow/status/kamu-data/kamu-client-python/build.yaml?logo=githubactions&label=CI&logoColor=white&style=for-the-badge&branch=master)](https://github.com/kamu-data/client-python/actions)
[![Chat](https://shields.io/discord/898726370199359498?style=for-the-badge&logo=discord&label=Discord)](https://discord.gg/nU6TXRQNXC)


</p>
</div>

- [About](#about)
- [Installing](#installing)
  - [Extras](#extras)
- [Using in plain Python scripts](#using-in-plain-python-scripts)
- [Authentication](#authentication)
- [Using in Jupyter](#using-in-jupyter)
  - [Other Notebook Environmnets](#other-notebook-environmnets)
- [Serving data from a local Kamu workspace](#serving-data-from-a-local-kamu-workspace)
- [Using with Spark](#using-with-spark)


## About
Python client library for Kamu.

Start with [`kamu-cli`](https://github.com/kamu-data/kamu-cli) repo if you are not familiar with the project.

## Installing
Install the library:
```bash
pip install kamu
```

Consider installing with extra features:
```bash
pip install kamu[jupyter-autoviz,jupyter-sql,spark]
```

### Extras
- `jupyter-autoviz`- Jupyter auto-viz for Pandas data frames
- `jupyter-sql` - Jupyter `%%sql` cell magic
- `spark` - extra libraries temporarily required to communicate with Spark engine


## Using in plain Python scripts
```python
import kamu

con = kamu.connect("grpc+tls://node.demo.kamu.dev:50050")

# Executes query on the node and returns result as Pandas DataFrame
df = con.query(
    """
    select
        event_time, open, close, volume
    from 'kamu/co.alphavantage.tickers.daily.spy'
    where from_symbol = 'spy' and to_symbol = 'usd'
    order by event_time
    """
)

print(df)
```

By default the connection will use `DataFusion` engine with Postgres-like SQL dialect.

The client library is based on modern [ADBC](https://arrow.apache.org/docs/format/ADBC.html) standard and the underlying connection can be used directly with other libraries supporting ADBC data sources:

```python
import kamu
import pandas

con = kamu.connect("grpc+tls://node.demo.kamu.dev:50050")

df = pandas.read_sql_query(
    "select 1 as x",
    con.as_adbc(),
)
```

## Authentication
You can supply an access token via `token` parameter:

```python
kamu.connect("grpc+tls://node.demo.kamu.dev:50050", token="<access-token>")
```

When token is not provided the library will authenticate as `anonymous` user. If node allows anonymous access the client will get a session token assigned during the handshake procedure and will use it for all subsequent requests.


## Using in Jupyter
Load the extension in your notebook:

```python
%load_ext kamu
```

Create connection:

```python
con = kamu.connect("grpc+tls://node.demo.kamu.dev:50050")
```

Extension provides a convenience `%%sql` magic:

```sql
%%sql
select
    event_time, open, close, volume
from 'kamu/co.alphavantage.tickers.daily.spy'
where from_symbol = 'spy' and to_symbol = 'usd'
order by event_time
```

The above is equivalent to:

```python
con.query("...")
```

To save the query result into a variable use:
```sql
%%sql -o df
select * from x
```

The above is equivalent to:

```python
df = con.query("...")
df
```

To silence the output add `-q`:
```sql
%%sql -o df -q
select * from x
```

The `kamu` extension automatically registers [`autovizwidget`](https://github.com/jupyter-incubator/sparkmagic) to offer some options to visualize your data frames.

![Jupyter extension](https://raw.githubusercontent.com/kamu-data/kamu-client-python/refs/heads/master/docs/readme-files/jupyter.png)


### Other Notebook Environmnets
This library should work with most Python-based notebook environments.

Here's an example [Google Colab Notebook](https://colab.research.google.com/drive/1WQqZJsPQpipU4kW6SPea9H2qmHH4rF8k).


## Serving data from a local Kamu workspace
If you have [`kamu-cli`](https://github.com/kamu-data/kamu-cli) you can serve data directly from a local workspace like so:

```python
con = kamu.connect("file:///path/to/workspace")
```

This will automatically start a `kamu sql server` sub-process and connect to it using an appropriate protocol.

Use `file://` to start the server in the current directory.


## Using with Spark
You can specify a different engine when connecting:

```python
con = kamu.connect("http://livy:8888", engine="spark")
```

Note that currently Spark connectivity relies on Livy HTTP gateway but in future will be unified under ADBC.

You can also provide extra configuration to the connection:

```python
con = kamu.connect(
    "http://livy:8888",
    engine="spark",
    connection_params=dict(
        driver_memory="1000m",
        executor_memory="2000m",
    ),
)
```


[Tutorials]: https://docs.kamu.dev/cli/learn/learning-materials/
[Examples]: https://docs.kamu.dev/cli/learn/examples/
[Docs]: https://docs.kamu.dev/welcome/
[Demo]: https://demo.kamu.dev/
[FAQ]: https://docs.kamu.dev/cli/get-started/faq/
[Chat]: https://discord.gg/nU6TXRQNXC
[Contributing]: https://docs.kamu.dev/contrib/
[Developer Guide]: ./DEVELOPER.md
[License]: https://docs.kamu.dev/contrib/license/
[Website]: https://kamu.dev
