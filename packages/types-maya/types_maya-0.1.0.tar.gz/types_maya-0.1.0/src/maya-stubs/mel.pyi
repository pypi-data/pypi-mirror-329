import typing

def eval(string: str, /) -> typing.Any: ...
def createMelWrapper(
    fn: typing.Callable,
    types: list[str] = [],
    retType: str = "void",
    ignoreDefaultArgs: bool = True,
    returnCmd: bool = False,
    outDir: str | None = None,
) -> str: ...
