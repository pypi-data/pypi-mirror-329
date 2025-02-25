from termcolor import colored
from colorama import init as colorama_init

from .common.constants import (
    LOGGER_LEVELS,
    LOGGER_INFO,
    LOGGER_FORMAT,
)
from .common.decorators import check_now_log_level


class Logger:
    """
    Класс Logger — используется для логирования сообщений с возможностью задания уровня логов,
    сохранения в файл и добавления имени логгера.
    """
    logger_level = LOGGER_INFO  # Уровень логирования по умолчанию

    def __init__(
            self,
            name: str | None = None,  # Имя логгера, может быть None
            level: int = LOGGER_INFO,  # Уровень логирования (по умолчанию LOGGER_INFO)
            save_file: bool = False  # Флаг сохранения логов в файл
    ):
        self.name = name  # Имя логгера, отображается в сообщениях
        self.level = level  # Уровень логирования
        self.save_file = save_file  # Флаг для сохранения логов в файл

        colorama_init(autoreset=True)

    def __send(self, message: str, name: str, now_log_level: int) -> None:
        """
        Отправляет сообщение в лог с заданным уровнем и именем.
        Форматирует сообщение согласно LOGGER_FORMAT.

        :param message: Сообщение для логирования.
        :param name: Имя логгера или метода.
        :param now_log_level: Текущий уровень логирования.
        """
        # Формирует строку для логирования, используя заданный формат
        arg_string = (
            LOGGER_LEVELS[now_log_level].upper(),  # Уровень логирования в верхнем регистре
            self.name,  # Имя логгера
            name,  # Имя метода или дополнительная информация
            message,  # Сообщение для логирования
        )

        # Форматирование сообщения
        message = LOGGER_FORMAT.format(*arg_string)

        # Вывод сообщения в консоль
        if now_log_level == 0:
            print(colored(message, 'white'))

        elif now_log_level == 1:
            print(colored(message, 'white'))

        elif now_log_level == 2:
            print(colored(message, 'yellow'))

        elif now_log_level == 3:
            print(colored(message, 'red'))

        elif now_log_level == 4:
            print(colored(message, 'red'))

        # Опционально: сохранение сообщения в файл
        if self.save_file:
            pass  # Здесь нужно реализовать логику записи в файл

    @check_now_log_level(user_level=0)
    def debug(self, message: str, name: str) -> None:
        """
        Логирование информации на уровне 1
        Проверка уровня выполняется декоратором `check_now_log_level`.

        :param message: Сообщение для логирования.
        :param name: Дополнительное имя (опционально).
        """

        self.__send(message, name, 0)

    @check_now_log_level(user_level=1)
    def info(self, message: str, name: str | None = None) -> None:
        """
        Логирование информации на уровне 1
        Проверка уровня выполняется декоратором `check_now_log_level`.

        :param message: Сообщение для логирования.
        :param name: Дополнительное имя (опционально).
        """

        self.__send(message, name, 1)

    @check_now_log_level(user_level=2)
    def warning(self, message: str, name: str | None = None) -> None:
        """
        Логирование предупреждений на уровне 2 (например, WARNING).
        Проверка уровня выполняется декоратором `check_now_log_level`.

        :param message: Сообщение для логирования.
        :param name: Дополнительное имя (опционально).
        """

        self.__send(message, name, 2)

    @check_now_log_level(user_level=3)
    def error(self, message: str, name: str | None = None) -> None:
        """
        Логирование ошибок на уровне 3 (например, ERROR).
        Проверка уровня выполняется декоратором `check_now_log_level`.

        :param message: Сообщение для логирования.
        :param name: Дополнительное имя (опционально).
        """

        self.__send(message, name, 3)

    @check_now_log_level(user_level=4)
    def critical(self, message: str, name: str | None = None) -> None:
        """
        Логирование ошибок на уровне 4 (например, CRITICAL).
        Проверка уровня выполняется декоратором `check_now_log_level`.

        :param message: Сообщение для логирования.
        :param name: Дополнительное имя (опционально).
        """

        self.__send(message, name, 4)
        exit(1)
