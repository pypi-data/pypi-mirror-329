# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bkpaas_auth', 'bkpaas_auth.core']

package_data = \
{'': ['*']}

install_requires = \
['django>=4.2,<5.0', 'requests', 'six']

setup_kwargs = {
    'name': 'bkpaas-auth',
    'version': '3.1.1',
    'description': 'User authentication django app for blueking internal projects',
    'long_description': '# bkpaas-auth\n\n蓝鲸 PaaS 平台内部服务使用的用户鉴权模块。\n\n## 版本历史\n\n详见 `CHANGES.md`。\n\n## 开发指南\n\n### 发布包\n\n- 在 `bkpaas_auth/__init__.py`  文件中更新 `__version__`\n- 在 `setup.py` 文件中更新 `version`\n- 在 `pyproject.toml` 中更新 `version`\n- 在 `CHANGES.md` 中添加对应的版本日志\n- 执行 `poetry build` 命令在 dist 目录下生成当前版本的包。然后执行 `twine upload dist/* --repository-url {pypi_address} --username {your_name} --password {your_token}` 将其上传到 pypi 服务器上。\n\n### 关于 setup.py\n\n虽然在 [PEP 517](https://python-poetry.org/docs/pyproject/#poetry-and-pep-517) 规范里，Python 包不再需要 `setup.py` 文件。但真正少了 `setup.py` 文件后，会发现有些功能就没法正常使用，比如 pip 的可编辑安装模式、tox 等（[相关文档](https://github.com/python-poetry/poetry/issues/761)）。所以我们仍然需要它。\n\n为了避免维护重复的 `pyproject.toml` 和 `setup.py` 文件，我们使用了 [dephell](https://github.com/dephell/dephell) 工具来自动生成 `setup.py` 文件。\n\n- 安装 dephell\n- 在根目录执行 `dephell deps convert --from pyproject.toml --to setup.py`\n\n## 使用指南\n1. 更新 settings：\n```python\nINSTALLED_APPS = [\n    ...\n    \'bkpaas_auth\',\n    ...\n]\n\nMIDDLEWARE = [\n    ...\n    \'bkpaas_auth.middlewares.CookieLoginMiddleware\',\n    ...\n]\n\nAUTHENTICATION_BACKENDS = [\n    # [推荐] 使用内置的虚拟用户类型，不依赖于数据库表.\n    \'bkpaas_auth.backends.UniversalAuthBackend\',\n    # 如果项目需要保留使用数据库表的方式来设计用户模型, 则需要使用 DjangoAuthUserCompatibleBackend\n    # \'bkpaas_auth.backends.DjangoAuthUserCompatibleBackend\',\n]\n\n# 使用 bkpaas_auth 内置的基于内存的用户模型\n# 如果项目需要保留使用数据库表的方式来设计用户模型, 可阅读 「关于AUTH_USER_MODEL」的部分说明\nAUTH_USER_MODEL = \'bkpaas_auth.User\'\n\n# 用户登录态认证类型\nBKAUTH_BACKEND_TYPE = "bk_token" # 可选值：bk_token/bk_ticket\n# 验证用户登录态的 API，如 蓝鲸统一登录校验登录态的 API\nBKAUTH_USER_COOKIE_VERIFY_URL = "http://bk-login-web/api/v3/is_login/"\n\n# [可选]`BKAUTH_DEFAULT_PROVIDER_TYPE` 的值用于 JWT 校验时获取默认的用户认证类型。\nBKAUTH_DEFAULT_PROVIDER_TYPE = \'RTX\'  # 可选值：RTX/UIN/BK，详见 ProviderType\n```\n\n启用多租户模式时, 需要更新上面的 settings\n```python\n# 启用多租户模式\nBKAUTH_ENABLE_MULTI_TENANT_MODE = True\n\n# 用户登录态认证类型\nBKAUTH_BACKEND_TYPE = "bk_token" # 只能选择：bk_token\n\n# 验证用户信息的网关 API(租户版本)\n# 如 BK_API_URL_TMPL.format(api_name="bk-login") + "/prod/login/api/v3/open/bk-tokens/userinfo/"\nBKAUTH_USER_INFO_APIGW_URL = ""\n\n# [可选]`BKAUTH_DEFAULT_PROVIDER_TYPE` 的值用于 JWT 校验时获取默认的用户认证类型。\nBKAUTH_DEFAULT_PROVIDER_TYPE = \'BK\'  # 只能选择：BK\n```\n\n2. 在 app config 中进行 patch：\n\n配置登录模块的 apps.py\n\n```python\nfrom bkpaas_auth.backends import DjangoAuthUserCompatibleBackend\nfrom bkpaas_auth.models import User\nfrom django.apps import AppConfig\n\n\nclass MyAppConfig(AppConfig):\n    name = \'my_app\'\n\n    def ready(self):\n        from bkpaas_auth.monkey import patch_middleware_get_user\n\n        patch_middleware_get_user()\n```\n\n更新 `__init__.py`，配置 default_app_config\n```\ndefault_app_config = \'xxx.apps.MyAppConfig\'\n```\n\n3. 配置日志（可选）\n在 django settings 的 LOGGING 中，为 sdk 配置 logger，如\n\n```python\nLOGGING = {\n    "handlers": {\n        "root": {\n            ...\n        },\n    },\n    "loggers": {\n        "bkpaas_auth": {\n            "handlers": ["root"],\n            "level": "WARNING",\n            "propagate": True,\n        },\n    },\n}\n```\n\n### 关于 AUTH_USER_MODEL\n\nbkpaas-auth 内置的基于内存的不依赖于数据库表的用户模型, 如果需要复用原有的用户模型, 则需要使用 `DjangoAuthUserCompatibleBackend` 作为用户校验后端.\n\n在默认情况下, `DjangoAuthUserCompatibleBackend` 会从 bkpaas-auth 获取到当前登录的用户信息, 并会根据用户信息尝试创建一个基于数据库的用户模型.\n如果你有以下诉求, 则应当继承 `DjangoAuthUserCompatibleBackend`, 自行实现具体的业务逻辑:\n\n1. 不希望自动创建基于数据库的用户模型:\n```python\n\n\nclass YourDjangoAuthUserCompatibleBackend(DjangoAuthUserCompatibleBackend):\n    create_unknown_user = False\n```\n\n2. 用户模型有与 django `auth.User` 不兼容的字段或其他需要初始化的字段:\n```python\n\nclass YourDjangoAuthUserCompatibleBackend(DjangoAuthUserCompatibleBackend):\n    def configure_user(self, db_user, bk_user: User):\n        """\n        Configure a user after creation and return the updated user.\n        """\n        ...\n        return db_user\n```\n\n> 说明: 启用多租户模式后, user 会增加 tenant_id 和 display_name 两个字段，可以通过 `request.user.tenant_id` 获取租户 ID, 通过 `request.user.display_name` 获取用户展示名。\n\n#### 和 [apigw-manager](../apigw-manager) 集成\n该 SDK 可以和 apigw-manager 集成，完成网关 JWT 的校验，在 settings 中配置：\n```python\nINSTALLED_APPS += ["apigw_manager.apigw"]\nAUTHENTICATION_BACKENDS += ["bkpaas_auth.backends.APIGatewayAuthBackend"]\nMIDDLEWARE += [\n    "apigw_manager.apigw.authentication.ApiGatewayJWTGenericMiddleware",  # JWT 认证\n    "apigw_manager.apigw.authentication.ApiGatewayJWTAppMiddleware",  # JWT 透传的应用信息\n    "apigw_manager.apigw.authentication.ApiGatewayJWTUserMiddleware",  # JWT 透传的用户信息\n]\n```\n\n设置之后，通过 JWT 透传的用户态会验证后，会写入到 `request.user` 中。注意，配置了不认证用户的网关资源透传的请求，会生成一个有对应用户名的匿名用户对象（`is_authenticated` 为 `False`）。\n',
    'author': 'blueking',
    'author_email': 'blueking@tencent.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
