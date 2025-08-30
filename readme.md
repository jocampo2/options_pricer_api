# Options prices API

Uses a vectorized approach to price hundreds of thousands of options in milliseconds.

Currently bottlenecked by I/O of prices and options files.

## How to run

**Locally** with python 3.12

```
pip install -r requirements.txt
uvicorn app.main:app --reload
```
