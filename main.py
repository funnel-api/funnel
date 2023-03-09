#!/usr/bin/env python
import funnel


def my_function(a, b=10):
    return a + b


funnel.register(my_function, "My_Function", "/")


if __name__ == "__main__":
    funnel.create_app().run(debug=True)
