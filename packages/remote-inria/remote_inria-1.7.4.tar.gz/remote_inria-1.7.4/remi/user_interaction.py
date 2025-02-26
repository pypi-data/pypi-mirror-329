"""
Functions to interact with the user through the command line.
"""

from typing import Any

from termcolor import colored


def to_bold(text: str):
    return colored(text, attrs=["bold"])


def print_info(
    text: str,
    newline: bool = False,
    bold: bool = False,
    end: str = "\n",
) -> None:
    prefix: str = ""
    if newline:
        prefix += "\n"
    prefix += colored("[INFO]", "green", attrs=["bold"])

    if bold:
        text = to_bold(text)

    print(prefix, text, end=end)


def print_warning(
    text: str,
    newline: bool = False,
    bold: bool = False,
    end: str = "\n",
) -> None:
    prefix: str = ""
    if newline:
        prefix += "\n"
    prefix += colored("[WARNING]", "yellow", attrs=["bold"])

    if bold:
        text = to_bold(text)

    print(prefix, text, end=end)


def print_error(
    text: str,
    newline: bool = False,
    bold: bool = False,
    end: str = "\n",
) -> None:
    prefix: str = ""
    if newline:
        prefix += "\n"
    prefix += colored("[ERROR]", "red", attrs=["bold"])

    if bold:
        text = to_bold(text)

    print(prefix, text, end=end)


def prompt_user_yes_no(question: str) -> bool:
    answer: str = ""
    while answer not in ["y", "n"]:
        print_warning(question, end="")
        answer = input(" [y/n] ").lower()

    return answer == "y"


def prompt_user_value(
    question: str,
    default_value: Any = None,
) -> Any:
    question: str = question

    if default_value is not None:
        question += f" [{colored(default_value, 'yellow')}]"
    question += ": "

    return input(question).strip() or default_value
