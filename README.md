
# Run in Development

```
poetry run uvicorn my_api:app --reload --port=3010 --workers=5
```

# Concurrency

## Plain async GET

* Running without `--workers=5`, so there should be one only.
* When running `ab -c 10 -n 100 127.0.0.1:3010/hello`, I get fine concurrency.

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
