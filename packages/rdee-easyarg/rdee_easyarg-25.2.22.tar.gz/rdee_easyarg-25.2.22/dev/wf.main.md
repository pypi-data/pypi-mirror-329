# workflow

# Motivation
+ fire的ui反人类, typer的很优雅, 但是感觉完全为了CLI app服务, 并不想兼容一般函数, 要设置函数参数的默认值为各种typer自己的类型, 也不好
+ So, 拟开发一个相对简单, 但是兼容性好的CLI app wrapper: easyarg
+ 初始阶段就是针对python, 未来或许可以搞成跨语言的东东...
+ Slogan: Less is More, Simple is Better!


# WorkFlow

## easyarg

*@2024-11-28 22:45:31*
+ 加一个对任意generic参数函数包装命令行接口的功能, 仍然强需求显示类型声明

*@2024-11-23 14:25:27*
+ ok, 实现了一版极简的, 完全依托于标准argparse的东西
+ argument仅支持python的intrinsic type: int, float, str & bool
+ 测试似乎是可用的了, 然后想想后续的更新方向:
    + 1. customized help information, 这个可以参考typer的, 人家那个确实挺好看
    + 2. 实现无接触式的直接执行, 即不需要什么decorator之类的, 直接强制执行你这个函数

*@2024-11-22 22:18:22*
+ 先找GPT写一版简单的, 然后再改吧...