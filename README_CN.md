# nonebot_plugin_pjsekaibot

Read in [English](./README.md) | 简体中文

这是一个自用的Project Sekai简单查分插件。

如果您不了解此插件，部署前请三思。因为它部署起来比较麻烦，且运行效果可能不及你的想象。

## 环境

此插件在Ubuntu 20.04上经过测试。如果您在其他系统上运行，可能需要修改一点代码细节。如果您使用Windows服务器，更推荐部署[Unibot分布式](https://docs.unipjsk.com/distributed/)，其功能远优于此插件。

此插件基于 [nonebot2](nb2.baka.icu) 和 [go-cqhttp](https://github.com/Mrs4s/go-cqhttp)。

此插件几乎完全依赖[Unibot](https://docs.unipjsk.com/) api。请多多支持[Unibot](https://github.com/watagashi-uni/Unibot)！

## 安装

1. 你应首先有一个能正常运行的nonebot2 QQ机器人。

2. 安装 [poetry](https://python-poetry.org/)，若你的设备上尚未安装过。

3. 前往您bot的插件目录，并确保您已经激活虚拟环境。

4. ```
   $ git clone https://github.com/CuSO4Deposit/nonebot_plugin_pjsekaibot
   
   $ poetry install
   ```

## 配置 & 初始化

接下来, 将 `bot.py` 所在的目录称作 `(root)`， 将插件目录 (即`(yourPluginDir)/pjsekaibot/`) 称作 `(plugin)`。

1. 此插件通过 [loguru](https://loguru.readthedocs.io/) 实现自定义日志. 将下面的代码插入`bot.py` 中 `nonebot.init()` 一行的前面（您也可以自定义其中的参数）。
   
   ```python
   from nonebot.log import logger
   logger.add("./data/ProjectSekai/log/debug.log",
           rotation="50MB",
           level="DEBUG",
           format="[{time:YY-MM-DD HH:mm:ss.SS UTC!UTC}] [PJSK/{level}] {message}"
           filter=lambda x : x["extra"].get("name") == "pjsk"
           )
   ```

2. 运行bot，发送消息 `/pjadmin init1`  (假设您命令的提示符为 `/` )。这一步将生成 data 目录。如果您需要重复执行此命令，需要手动删除`(root)/data/ProjectSekai/config.json`.

3. 这个插件依赖很多外部资源和api。有一些api可以任意使用，但也有一些需要你自行向开发者申请。因此您需要手动配置api url。
   
   打开  `(root)/data/ProjectSekai/config.json`。您可以参考 [这个列表](https://depoze.xyz/sayoribot/apilist/) 来填写`config.json`。如果留空，插件会自动关闭对应的功能模块。

4. 填写api后（这也意味着您已经指定了资源库和masterDB的url），您就可以下载谱面等资源到本地。向bot发送 `/pjadmin update`。注意，首次运行时这里将下载大量的图片文件，甚至可能会超过1小时。

5. 将 `(plugin)/assets/`下的 *.ttf 文件移动到 `(root)/data/ProjectSekai/assets/`下。

6. 若你不希望任何人随意唤起`/pjadmin`更新资源，可以前往`(plugin)/handler/admin.py`，修改rule函数中的白名单。从此只有白名单中的QQ号可以唤起 `/pjadmin`。

7. 在`(plugin)/modules/ntfy.py`中配置您的notify服务器信息。如果不配置此项，你需要注释掉调用`Notify()`函数的相关代码。

8. 一切都调试好后，您可以修改 `bot.py`中logger的日志记录level到 "WARNING"。实际使用时不应该使用debug level，这容易泄露敏感信息。

## 命令

下面的命令中， `()` 是可选参数。

`bind`, `sk`, `profile` 支持台服、国际服。将 `pj` 替换为 `twpj` 或 `enpj` 使用对应功能。

| Command                   | Description                            |
| ------------------------- | -------------------------------------- |
| `/pj alias <song>`        | 返回 \<song\> 的别名集合                      |
| `/pj bind <id>`           | 将 \<id\> 绑定到 QQ号                       |
| `/pj chart <song> (ex)`   | 获取 \<song\>的谱面。若带 "ex" 参数，则返回EXPERT谱面。 |
| `/pj (fc/ap)难度排行 <level>` | 获取\<level\>级歌曲的难度排行 / fc难度排行 / ap难度排行  |
| `/pj help`                | 获取命令列表                                 |
| `/pj sk`                  | 获取当期活动目前的排名和pt                         |
| `/pj profile`             | 获取个人信息                                 |
| `/pj rk`                  | 获取当期排位信息                               |
| `/pj ycx`                 | 获取当期活动的预测线                             |

## 支持 & 贡献

欢迎联系我们、提issue或pull request。

## 许可

使用 the GNU Affero General Public License 3.0-or-later.

## 特别感谢

- [UniPJSKApi](docs.unipjsk.com)

- [33 Kit](https://3-3.dev/)

- [ぷろせかもえ！](https://profile.pjsekai.moe/)

- [Sekai Viewer](sekai.best)
