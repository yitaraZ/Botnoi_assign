def print_triangle(n):
    for i in range(1, n+1):
        print('*' * i)

    for i in range(n-1, 0, -1):
        print('*' * i)

x = int(input("์input x : "))
print_triangle(x)