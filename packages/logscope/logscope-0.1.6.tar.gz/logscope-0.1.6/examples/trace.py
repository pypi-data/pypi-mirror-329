
from logscope import trace

@trace
def f():
    x = 5
    y = 10
    return x + y

f()