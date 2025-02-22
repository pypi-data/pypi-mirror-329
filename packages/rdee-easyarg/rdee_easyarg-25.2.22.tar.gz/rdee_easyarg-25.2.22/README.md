# rdee-python-easyarg

+ Used to run any function with generic arguments from CLI
+ Support two modes: CLI app or CLI executor

# Install

+ `pip install rdee-easyarg`

# Examples

## CLI-app mode

+ In this mode, we use a decorator to generate CLI interface automatically, mimicing typer in general

```python
import easyarg

ea = easyarg.EasyArg()


@ea.command(name="func1", alias="f")
def f1(x: int, y: int, flag1: bool, flag2: bool = False):
    """

    :param x: this info will be read as argument description in -h, --help
    """
    print(x+y)


if __name__ == "__main__":
    ea.parse()
```

+ You can run the script directly, such as `./a.py f1 --x 1 --y 2`, and get 3
+ `-h/--help` for app level and function level are both supported

## CLI-executor mode

+ In this mode, we can run a function without modifying any of its code
+ For instance, given the `funcs.py`

```python
def add(x: int, y: int = 0) -> int:
    print(x + y)

def mul(a: float, B: float, c: float = 1.0) -> float:
    print(a * B * c)
```

+ just run `python -m easyarg funcs.py add --x 1 --y 2` to execute the function "add"
