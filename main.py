#!/usr/bin/env python
import funnel


def my_function(a, b=10):
    return {"result": a + b}


parser = funnel.api.parser()
parser.add_argument("a", type=int, help="First param", location="json")
parser.add_argument("b", type=int, help="Second param", location="json")


funnel.register(my_function, "My_Function", "/", doc={"expect": [parser]})


if __name__ == "__main__":
    funnel.create_app().run(debug=True)
