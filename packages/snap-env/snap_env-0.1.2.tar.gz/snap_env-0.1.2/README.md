# snap-env
A sassy little env var loader for Python.

## What for?
Because env vars shouldn’t ghost you.

## Install
```bash
pip install snap-env
```

## Use

```
import snap_env

snap_env.load()  # Loads .env file
api_key = snap_env.get("API_KEY")  # "secret123" or bust
port = snap_env.get("PORT", 5000)  # Fallback to 5000 if unset

```