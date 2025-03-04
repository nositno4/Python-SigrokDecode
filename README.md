## 重要提醒!

该仓库脚本仅仅为了熟悉 `libsigrokdecode`
个人练习测试 API 用的, 不具有实际意义.
请使用官方实现的解析器.

## 关于本仓库

仓库内 `bak` 文件夹内是 `PulseView` 自带的解析器脚本.
放在此处是为了代码编写时参考使用.
相关编写教程参考:

https://sigrok.org/wiki/Protocol_decoder_HOWTO

https://sigrok.org/wiki/Protocol_decoder_API

https://sigrok.org/wiki/Protocol_decoder_API/Queries

## 处理pd文件.py

为了把脚本喂给 AI 当知识库, 对 pd 文件进行了处理.
这个 `python` 文件就是把所有 `pd.py` 文件重命名成了对应解析器名称.
然后把开头的 `license` 删掉了(因为对AI来说没有实际意义).
