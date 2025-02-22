#!/usr/bin/env python3
# coding=utf-8


def add(x: int, y: int = 0) -> int:
    """Add two numbers"""
    print(f"{x + y=}")


def mul(a: float | str, B: float, c: float = 1.0) -> float:
    """Multiply numbers"""
    print(f"{(a * B * c)=}")
