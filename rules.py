
def fib(n):
    if n in [0,1]: return n
    return fib(n-1) + fib(n-2)


a = fib(13)
print(a)