
# Run in Development

```
poetry run uvicorn my_api:app --reload --port=3010 --workers=5
```

# Concurrency

## Plain async GET

* Running without `--workers=5`, so there should be one only.
* When running `ab -c 10 -n 100 127.0.0.1:3010/hello`, I get fine concurrency.

