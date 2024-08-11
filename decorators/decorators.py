import time
from typing import Hashable
from functools import wraps


def benchmark(func):
    """
    ### Замер времени выполнения функции
    Декоратор, который замеряет время выполнения функции и выводит его в консоль.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        t1 = time.time()
        result = func(*args, **kwargs)
        print(
            f"Function {func.__name__} took {time.time() - t1:.6f}",
            "seconds  to execute",
        )
        return result

    return wrapper


def logging(func):
    """
    ### Логирование параметров вызова функции
    Декоратор, который печатает параметры вызова функции.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__} with {args}, {kwargs}")
        result = func(*args, **kwargs)
        return result

    return wrapper


def counter(func):
    """
    ### Счетчик вызовов функции
    Декоратор, который считает количество вызовов функции
    и выводит это количество в консоль.
    """
    n_times = 0

    @wraps(func)
    def wrapper(*args, **kwargs):
        nonlocal n_times
        n_times += 1
        print(f"Function {func.__name__} has been called for {n_times} times")
        return func(*args, **kwargs)

    return wrapper


def memo(func):
    """
    ### Кэширование ранее полученных результатов функции
    Если функция вызвана с теми же аргументами, что и ранее, то возвращается сохраненный результат.
    Используется для оптимизации вычислений, когда результаты могут быть повторно использованы.
    В примере ниже показано, как функция fibonacci может использовать кэширование для ускорения вычислений.
    ### Пример использования
    @memo
    def fibonacci(n: int) -> int:
        if n <= 1:
            return n
        return fibonacci(n - 1) + fibonacci(n - 2)
    """
    cache = {}

    @wraps(func)
    def wrapper(*args):
        is_hashable: bool = all(
            map(lambda arg: isinstance(arg, Hashable), args)
        )
        if is_hashable and (args in cache):
            print("Using cached result")
            return cache[args]
        result = func(*args)
        cache[args] = result
        return result

    return wrapper


@memo
@logging
@counter
@benchmark
def fibonacci(n: int) -> int:
    if n <= 1:
        return n
    return fibonacci(n - 1,) + fibonacci(n - 2,)


print(fibonacci(3))
