# nonebot_plugin_pjsekaibot

Read in English | [简体中文](./README_CN.md)

This is a simple Project Sekai score prober plugin for my personal use.

If you are not familiar with this project, think twice before deploy it, as it is complicated to deploy and may not work as well as you think.

## Environment

This plugin is tested on Ubuntu 20.04. You may have to modify some details of code to run on a different OS. If you are on Windows, you can run [Unibot distributed](https://docs.unipjsk.com/distributed/), which has a much better performance.

This plugin is based on [nonebot2](nb2.baka.icu) and [go-cqhttp](https://github.com/Mrs4s/go-cqhttp).

This plugin almost entirely relies on [Unibot](https://docs.unipjsk.com/) api. Please support [Unibot](https://github.com/watagashi-uni/Unibot)!

## Installation

1. You should have a bot run on nonebot2.

2. Install [poetry](https://python-poetry.org/) if you don't have it on your device.

3. Go to the plugin directory, activate your virtual environment.

4. ```
   $ git clone https://github.com/CuSO4Deposit/nonebot_plugin_pjsekaibot
   
   $ poetry install
   ```

## Configuration & Initialization

In the following, we refer to the directory where your `bot.py` is at as `(root)`, and refer to the plugin directory (i.e. `(yourPluginDir)/pjsekaibot/`) as `(plugin)`

1. This plugin uses a custom logger from [loguru](https://loguru.readthedocs.io/). Insert the following code (or you can customize the arguments as you like) before `nonebot.init()` into `bot.py`:
   
   ```python
   from nonebot.log import logger
   logger.add("./data/ProjectSekai/log/debug.log",
           rotation="50MB",
           level="DEBUG",
           format="[{time:YY-MM-DD HH:mm:ss.SS UTC!UTC}] [PJSK/{level}] {message}"
           filter=lambda x : x["extra"].get("name") == "pjsk"
           )
   ```

2. Run your bot. Send a message `/pjadmin init1` to your bot. (This assumes your bot's command start with `/` .) This is to generate data directory. If you have to run this command again, you have to remove `(root)/data/ProjectSekai/config.json` manually.

3. This bot relies on many outer sources. While some are free to use, you may need to apply for some APIs yourself. So you have to specify the APIs manually.
   
   Open  `(root)/data/ProjectSekai/config.json`. You can refer to [this list](https://depoze.xyz/sayoribot/apilist/) to fill in `config.json`. If a field is left blank, bot will automatically disable the functions relying on this API.

4. After finishing filling the API (which means you have specified the assets & masterDB url), you can download the assets and charts to the local. Send a message `/pjadmin update` to your bot. Note: There are a lot of images to download, and it may takes ~1 hour or more.

5. Move the *.ttf file from `(plugin)/assets/` to `(root)/data/ProjectSekai/assets/`.

6. Since you don't want others to start an asset update at their will, you can modify `(plugin)/handler/admin.py`, uncomment the commented line in the rule function, and modify the whitelist. Since then, only the ones on your white list can call `/pjadmin`.

7. Configure your notify server in `(plugin)/modules/ntfy.py`. If you don't have one, maybe you have to comment out the code calling `Notify()` function.

8. If everything is OK, you can change the logger settings in `bot.py`, switch the logger level to "WARNING". It's not good to run a bot in production with debug logging level, as it may leak sensitive information.

## Command

In the following, `()` is optional argument.

`bind`, `sk`, `profile` supports Taiwan and English server. Substitute `pj` with `twpj` or `enpj` to use the corresponding command.

| Command                   | Description                                                        |
| ------------------------- | ------------------------------------------------------------------ |
| `/pj alias <song>`        | Get the current name alias of \<song\>                             |
| `/pj bind <id>`           | Bind \<id\> to this QQ id                                          |
| `/pj chart <song> (ex)`   | Get the chart of \<song\>, if specified "ex", return EXPERT chart. |
| `/pj (fc/ap)难度排行 <level>` | Get the difficulty rank of \<level\>.                              |
| `/pj help`                | Get help doc                                                       |
| `/pj sk`                  | Get your current event pt and rank                                 |
| `/pj profile`             | Get your personal profile (i.e. # of songs you clear, fc or ap)    |
| `/pj rk`                  | Get your current rankmatch info                                    |
| `/pj ycx`                 | Get the predicted event line of current event                      |

## Support & Contribute

Feel free to contact us, post an issue or make a pull request!

## License

This project is licenced under the GNU Affero General Public License 3.0-or-later.

## Special Thanks

- [UniPJSKApi](docs.unipjsk.com)

- [33 Kit](https://3-3.dev/)

- [ぷろせかもえ！](https://profile.pjsekai.moe/)

- [Sekai Viewer](sekai.best)
