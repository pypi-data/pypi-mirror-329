# -*- coding: utf-8 -*-
# @time: 2024/2/19 17:25
# @author: Dyz
# @file: t1.py
# @software: PyCharm
import asyncio
from typing import Any

import typer
from typer.main import get_command

app = typer.Typer()


@app.command()
async def aio_1(name):
    print(f"2, {name}! 2:")
    # typer.echo(f"Hello {name}")


@app.command()
def te(name):
    asyncio.run(aio_1(name))


if __name__ == "__main__":
    app()

    # @app.command(async_callback=True)
    # async def te(name: str):
    #     ctx = typer.Context
    #     await asyncio.sleep(1)
    #     print(f"1, {name}! 1: {ctx.command_path}")
    #     # typer.echo(f"1, {name}! 1: {ctx.command_path}")
    #
    #
    # @app.command()
    # def hello(name: str):
    #     ctx = typer.Context
    #     typer.echo(f"Hello, {name}! You invoked the command: {ctx.command_path}")
    #
    #
    # if __name__ == "__main__":
    #     app()
