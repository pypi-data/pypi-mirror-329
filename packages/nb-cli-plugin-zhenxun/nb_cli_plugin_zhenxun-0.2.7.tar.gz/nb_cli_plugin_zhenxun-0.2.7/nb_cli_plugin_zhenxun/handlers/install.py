import asyncio
from pathlib import Path
from typing import ClassVar

from alibabacloud_devops20210625 import models as devops_20210625_models
from alibabacloud_devops20210625.client import Client as devops20210625Client
from alibabacloud_devops20210625.models import ListRepositoryTreeResponseBodyResult
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tea_util import models as util_models
from nb_cli.handlers import get_default_python
from pydantic import BaseModel
import ujson as json

ORGANIZATION_ID = "67a361cf556e6cdab537117a"

REF = "main"

ACCESS_TOKEN = "pt-UdeUrkTLRJW2GIDKppHA5Jmj_42a501b3-ccc2-47f7-8bb5-3e6cdd7a6a68"

REPOSITORY_ID = "4957429"


class PluginInfo(BaseModel):
    name: str
    """插件名称"""
    module: str
    """插件模块"""
    module_path: str
    """插件模块路径"""
    description: str
    """插件描述"""
    usage: str
    """插件使用方法"""
    author: str
    """插件作者"""
    version: str
    """插件版本"""
    plugin_type: str
    """插件类型"""
    is_dir: bool
    """插件是否为目录"""


class AlySample:
    plugins: ClassVar[list[PluginInfo]] = []

    @classmethod
    def create_client(cls) -> devops20210625Client:
        """
        使用AK&SK初始化账号Client
        @return: Client
        @throws Exception
        """
        config = open_api_models.Config(
            access_key_id="LTAI5tNmf7KaTAuhcvRobAQs",
            access_key_secret="6bwweMEMLDF4OTmFpj2QjvPq7zLRMc",
        )
        config.endpoint = "devops.cn-hangzhou.aliyuncs.com"
        return devops20210625Client(config)

    @classmethod
    async def get_content(cls, file_path: str) -> str:
        client = cls.create_client()
        get_file_blobs_request = devops_20210625_models.GetFileBlobsRequest(
            organization_id=ORGANIZATION_ID,
            ref=REF,
            file_path=file_path,
            access_token=ACCESS_TOKEN,
        )
        runtime = util_models.RuntimeOptions()
        headers = {}
        result = await client.get_file_blobs_with_options_async(
            REPOSITORY_ID, get_file_blobs_request, headers, runtime
        )
        assert result.body.result.content
        return result.body.result.content

    @classmethod
    async def get_plugin_json(cls):
        plugins: dict = json.loads(await cls.get_content("plugins.json"))
        for key in plugins:
            plugins[key]["name"] = key
        return [PluginInfo(**plugin) for plugin in plugins.values()]

    @classmethod
    async def get_plugin_path(cls, plugin_name: str) -> str | None:
        if not cls.plugins:
            cls.plugins = await cls.get_plugin_json()
        return next(
            (
                plugin.module_path
                for plugin in cls.plugins
                if plugin.name == plugin_name or plugin.module == plugin_name
            ),
            None,
        )

    @classmethod
    async def check_exists(cls, plugin_name: str) -> bool:
        return bool(await cls.get_plugin_path(plugin_name))

    @classmethod
    async def get_plugin_tree(
        cls, plugin_path: str
    ) -> list[ListRepositoryTreeResponseBodyResult]:
        client = cls.create_client()
        list_repository_tree_request = devops_20210625_models.ListRepositoryTreeRequest(
            organization_id=ORGANIZATION_ID, access_token=ACCESS_TOKEN, path=plugin_path
        )
        runtime = util_models.RuntimeOptions()
        headers = {}
        result = await client.list_repository_tree_with_options_async(
            REPOSITORY_ID, list_repository_tree_request, headers, runtime
        )
        return result.body.result

    @classmethod
    async def tree_to_plugin_path(
        cls, body_list: list[ListRepositoryTreeResponseBodyResult], data_list: list[str]
    ):
        for body in body_list:
            if body.path:
                if body.type == "tree":
                    await cls.tree_to_plugin_path(
                        await cls.get_plugin_tree(body.path), data_list
                    )
                else:
                    data_list.append(body.path)

    @classmethod
    async def download_plugin(cls, plugin_name: str) -> list[str]:
        plugin_path = await cls.get_plugin_path(plugin_name)
        assert plugin_path
        plugin_path_list = await cls.get_plugin_tree(plugin_path.replace(".", "/"))
        file_path_list: list[str] = []
        await cls.tree_to_plugin_path(plugin_path_list, file_path_list)
        for file_path in file_path_list:
            file = Path(file_path)
            file.parent.mkdir(parents=True, exist_ok=True)
            file.write_text(await cls.get_content(file_path))
        return [file_path for file_path in file_path_list if "requirement" in file_path]

    @classmethod
    async def install_req(
        cls,
        project_path: Path,
        python_path: str,
        req_file: str,
        pip_args: list[str] | None = None,
    ):
        """
        安装包
        """
        if pip_args is None:
            pip_args = []
        return await asyncio.create_subprocess_exec(
            python_path,
            "-m",
            "poetry",
            "run",
            "pip",
            "install",
            "-r",
            req_file,
            *pip_args,
            cwd=project_path.absolute(),
        )

    @classmethod
    async def install_dependencies(
        cls,
        project_name: str,
        python_path: str | None,
        req_file: str,
        pip_args: list[str] | None = None,
    ):
        if pip_args is None:
            pip_args = []
        if python_path is None:
            python_path = await get_default_python()
        project_path = Path() / project_name
        await cls.install_req(project_path, python_path, req_file, pip_args)
