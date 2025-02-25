def add(queue, a, b):
    ret = a + b
    queue.put(ret)


def subtract(queue, a, b):
    ret = a - b
    queue.put(ret)


def divide(queue, a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    ret = a / b
    queue.put(ret)


def multiply(queue, a, b):
    ret = a * b
    queue.put(ret)