# codyer_agent
codyer agent

# 发布pip库
在 ～/.pypirc 中配置 username password 之后，poetry config http-basic.pypi __token__ {password}
```shell
poetry build -f sdist
poetry publish
```