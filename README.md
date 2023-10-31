
# FastAPI and GraphQL (using Strawberry)

## Problem Statement

[FastAPI](https://fastapi.tiangolo.com/) promises great concurrency, due to its
use of Python's async features.
When using it together with [Strawberry](https://strawberry.rocks/docs/integrations/fastapi#fastapi),
though, it is easy to lose the concurrency and performance gains:
Strawberry, when used naively with FastAPI, will block FastAPI's event loop on
every request, which negates the concurrency gains.
The [integration example of
Strawberry](https://strawberry.rocks/docs/integrations/fastapi#fastapi) at the
time of writing does not mention or warn about it.

This repo shows how I investigated this: The sub sections under 'Concurrency'
below show my experiments, where the last experiment demonstrates the "drop-in"
solution I am using now.


# Run in Development

You need [Poetry](https://python-poetry.org/) installed. Then run `poetry
install` to install dependencies.

For all the tests, run the service on port 3010 like this:

```
poetry run uvicorn my_api:app --reload --port=3010
```


# Concurrency Observations

I use [Apache Bench (ab)](https://httpd.apache.org/docs/2.4/programs/ab.html)
to make concurrent requests to the service.

## Plain async GET

When running `ab -c 10 -n 100 127.0.0.1:3010/hello`, I get fine concurrency.

ab output:

```
...
Percentage of the requests served within a certain time (ms)
  50%   1009
  66%   1010
  75%   1011
  80%   1011
  90%   1011
  95%   1011
  98%   1011
  99%   1012
 100%   1012 (longest request)
```

## Naive GraphQL Query

`ab -p postfile -T 'application/json' -c 10 -n 100 127.0.0.1:3010/graphql`

No concurrency, as expected. ab output:

```
...
Percentage of the requests served within a certain time (ms)
  50%  10068
  66%  10072
  75%  10081
  80%  11075
  90%  11078
  95%  11082
  98%  12085
  99%  18118
```

## Async GraphQL Query

`ab -p postfile_async -T 'application/json' -c 10 -n 100 127.0.0.1:3010/graphql`

We get concurrency:

```
...
Percentage of the requests served within a certain time (ms)
  50%   1012
  66%   1016
  75%   1018
  80%   1018
  90%   1022
  95%   1024
  98%   1025
  99%   1064
 100%   1064 (longest request)
```

## Async GraphQL Query, with sync function run in threadpool

`ab -p postfile_sync -T 'application/json' -c 10 -n 100 127.0.0.1:3010/graphql`

We get concurrency:

```
...
Percentage of the requests served within a certain time (ms)
  50%   1018
  66%   1021
  75%   1023
  80%   1024
  90%   1033
  95%   1035
  98%   1044
  99%   1044
```


## Sync GraphQL Query function, with wrapper to make it async

When we annotate the sync query function with `@make_async`, we get the sync function wrapped as an async function, and the original function is run in the threadpool.

To reproduce this test, remove the comment from the line `# @make_async` in ./my_api/graphql.py.

**SUCCESS!** This approach should work in cases where folks follow [The
Example](https://strawberry.rocks/docs/integrations/fastapi#fastapi) on how to
use Strawberry with FastAPI blindly, and create a practically single-threaded
GraphQL service.

ab's output:

```
...
Percentage of the requests served within a certain time (ms)
  50%   1021
  66%   1023
  75%   1027
  80%   1028
  90%   1031
  95%   1032
  98%   1033
  99%   1034
 100%   1034 (longest request)
```

