def strict(func):
    def wrapper(*args):
        annotations = func.__annotations__
        for i, (arg, (name, expected_type)) in enumerate(zip(args, annotations.items())):
            if name == 'return':
                continue
            if not isinstance(arg, expected_type):
                raise TypeError(f"{name} должен быть типа {expected_type.__name__}, а получен {type(arg).__name__}")
        return func(*args)
    return wrapper


@strict
def sum_two(a: int, b: int) -> int:
    return a + b


print(sum_two(1, 2))    # >>> 3
print(sum_two(1, 2.4))  # >>> TypeError
