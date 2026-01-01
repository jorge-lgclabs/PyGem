
def bg_num_generator():
    while True:
        yield 1
        yield 2

result = bg_num_generator()

print(result)