![](docs/source/_static/img/funnel_icon.png)
# Funnel
Pouring functions into the Flask API.

# Installation

```bash
python -m pip install .
```

# Get started

Create a `main.py` as below.

```python
#!/usr/bin/env python
import funnel

def my_function(a, b=10):
    return a + b

funnel.register(my_function, "My_Function", "/")

if __name__ == "__main__":
    funnel.create_app().run(debug=True)
```

Start a Flask server at http://localhost:5000/

```bash
python main.py
```

Send a request.

```bash
curl http://localhost:5000/ --header 'Content-Type: application/json' --data '{"a": 5}'
```