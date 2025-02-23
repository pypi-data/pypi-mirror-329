import click
from nb_cli.cli import CLI_DEFAULT_STYLE, ClickAliasedCommand, run_async
from noneprompt import CancelledError, InputPrompt

from ..handlers.create import check_path
from ..handlers.install import AlySample


@click.command(
    cls=ClickAliasedCommand,
    aliases=["add", "plugin"],
    context_settings={"ignore_unknown_options": True},
    help="安装插件.",
)
@click.option(
    "-p",
    "--python-interpreter",
    default=None,
    help="指定Python解释器的路径",
)
@click.option(
    "-i",
    "--index-url",
    "index_url",
    default="https://mirrors.aliyun.com/pypi/simple/",
    help="pip下载所使用的镜像源",
)
@click.pass_context
@run_async
async def install(
    ctx: click.Context,
    python_interpreter: str | None,
    index_url: str,
):
    """在当前目录下安装小真寻."""
    try:
        plugin_name = await InputPrompt(
            "请输入需要安装插件名称或模块名:",
        ).prompt_async(style=CLI_DEFAULT_STYLE)
        if not await AlySample.check_exists(plugin_name):
            click.secho("插件不存在，请重新输入...", fg="yellow")
            ctx.exit()
        click.secho("正在下载插件...", fg="yellow")
        req_file = await AlySample.download_plugin(plugin_name)
        click.secho("插件下载成功...", fg="yellow")
        if req_file:
            click.secho("检测到依赖文件，正在尝试安装...", fg="yellow")
            await AlySample.install_dependencies(
                "", python_interpreter, req_file[0], ["-i", index_url]
            )
            click.secho("安装依赖完成...", fg="yellow")
        click.secho(f"插件 {plugin_name} 安装完成！", fg="yellow")
    except AssertionError:
        click.secho("插件内容或路径不存在...", fg="red")
        ctx.exit()
    except CancelledError:
        ctx.exit()
