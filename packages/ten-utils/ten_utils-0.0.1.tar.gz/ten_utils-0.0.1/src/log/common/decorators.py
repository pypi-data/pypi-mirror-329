from functools import wraps
import inspect


def check_now_log_level(user_level: int):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Получаем значение атрибута self для проверки
            self = args[0]
            now_level = getattr(self, "level", None)

            # Получаем стек вызовов
            frame = inspect.currentframe()
            # Получаем предыдущий фрейм (вызвавшую функцию/метод)
            caller_frame = frame.f_back
            # Получаем имя вызывающей функции
            caller_name = caller_frame.f_code.co_name

            # Добавление имени функции в аргументы вызываемой функции
            args = list(args)
            args.append(caller_name)
            args = tuple(args)

            if user_level <= now_level:
                result = func(*args, **kwargs)
                return result

            else:
                return None

        return wrapper

    return decorator
