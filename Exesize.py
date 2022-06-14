n = 63
x = 1
sum = 0

while x < n:
    if x == n:
        print(sum)
    elif x / 2 == 0:
        x += 1
    else:
        sum += x
        x += 1
        if x == n:
            print(sum)
            break

