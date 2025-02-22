#!/usr/bin/env python3
# coding=utf-8

try:
    import easyarg
except:
    print("Install this package first")
    raise

ea = easyarg.EasyArg()


@ea.command()
def add(x: int, y: int = 0) -> int:
    """Add two numbers"""
    print(f"{x + y=}")


@ea.command()
def mul(a: float | str, B: float, c: float = 1.0) -> float:
    """
    Multiply numbers

    Last Update: @2025-01-15 22:09:36
    """
    print(f"{(a * B * c)=}")


@ea.command(desc="divide calculation")
def div(q1: float | str, Q2: float, q3: float = 1.0) -> float:
    print(f"{(q1 / Q2 / q3)=}")


@ea.command(alias="d2")
def div2(q1: float | str, Q2: float, flag2: bool, q3: float = 1.0, flag1: bool = True) -> float:
    """
    a test div2 function

    :param flag2: required bool flag
    :param Q2: required float Q2
    """
    print(f"{(q1 / Q2 / q3)=}")


if __name__ == "__main__":
    ea.parse()
