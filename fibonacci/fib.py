def fib(last_num): 
    if(not last_num): 
        return 0
    if(last_num == 1): 
        return 1
    return fib(last_num - 1) + fib(last_num - 2)
print(fib(5))
