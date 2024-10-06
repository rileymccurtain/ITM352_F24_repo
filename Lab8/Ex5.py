#Debugging exercise # 5
def fibonacci(n):
    fib_sequence = [0, 1]
    for i in range(2, n):
        next_fib = fib_sequence[i - 1] + fib_sequence[i - 2]
        fib_sequence.append(next_fib)
    return fib_sequence[:n]

my_list = [1, 2, 3, 4, 5]
n = len(my_list)  
print(fibonacci(n))