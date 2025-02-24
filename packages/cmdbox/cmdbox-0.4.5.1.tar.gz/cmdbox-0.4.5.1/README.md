# cmdbox

- It is a command line application with a plugin mechanism.
- Documentation is [here](https://hamacom2004jp.github.io/cmdbox/).
- With cmdbox, you can easily implement commands with complex options.
- The implemented commands can be called from the CLI / RESTAPI / Web screen.
- The implemented commands can be executed on a remote server via redis.

# Install

- Install cmdbox with the following command.

```bash
pip install cmdbox
cmdbox -v
```

- Also install the docker version of the redis server.

```bash
docker run -p 6379:6379 --name redis -it ubuntu/redis:latest
```

# Tutorial

- Open the ```.sample/sample_project``` folder in the current directory with VSCode.

![image](https://github.com/hamacom2004jp/cmdbox/raw/main/docs_src/static/ss/readme001.png)

- Install dependent libraries.

```bash
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

- Run the project.

![image](https://github.com/hamacom2004jp/cmdbox/raw/main/docs_src/static/ss/readme002.png)

- The localhost web screen will open.

![image](https://github.com/hamacom2004jp/cmdbox/raw/main/docs_src/static/ss/readme003.png)

- Enter ```user01 / user01``` for the initial ID and PW to sign in.
- Using this web screen, you can easily execute the commands implemented in cmdbox.

![image](https://github.com/hamacom2004jp/cmdbox/raw/main/docs_src/static/ss/readme004.png)

- Let's look at the command to get a list of files as an example.
- Press the plus button under Commands to open the Add dialog.
- Then enter the following.

![image](https://github.com/hamacom2004jp/cmdbox/raw/main/docs_src/static/ss/readme005.png)

- Press the ```Save``` button once and then press the ```Execute``` button.
- The results of the command execution are displayed.

![image](https://github.com/hamacom2004jp/cmdbox/raw/main/docs_src/static/ss/readme006.png)

- Open the saved ```client_time``` and press the ```Raw``` button.
- You will see how to execute the same command on the command line; the RESTAPI URL is also displayed.

![image](https://github.com/hamacom2004jp/cmdbox/raw/main/docs_src/static/ss/readme007.png)


## How to implement a new command using cmdbox

- Under the ```sample/app/features/cli``` folder, you will find an implementation of the ```client_time``` mentioned earlier.
- The implementation is as follows. (Slightly abbreviated display)
- Create the following code and save it in the ```sample/app/features/cli``` folder.

```python
from cmdbox.app import common, feature
from typing import Dict, Any, Tuple, Union, List
import argparse
import datetime
import logging


class ClientTime(feature.Feature):
    def get_mode(self) -> Union[str, List[str]]:
        return "client"

    def get_cmd(self):
        return 'time'

    def get_option(self):
        return dict(
            type="str", default=None, required=False, multi=False, hide=False, use_redis=self.USE_REDIS_FALSE,
            discription_ja="クライアント側の現在時刻を表示します。",
            discription_en="Displays the current time at the client side.",
            choice=[
                dict(opt="timedelta", type="int", default=9, required=False, multi=False, hide=False, choice=None,
                        discription_ja="時差の時間数を指定します。",
                        discription_en="Specify the number of hours of time difference."),
            ])

    def apprun(self, logger:logging.Logger, args:argparse.Namespace, tm:float, pf:List[Dict[str, float]]=[]) -> Tuple[int, Dict[str, Any], Any]:
        tz = datetime.timezone(datetime.timedelta(hours=args.timedelta))
        dt = datetime.datetime.now(tz)
        ret = dict(success=dict(data=dt.strftime('%Y-%m-%d %H:%M:%S')))
        common.print_format(ret, args.format, tm, args.output_json, args.output_json_append, pf=pf)
        if 'success' not in ret:
            return 1, ret, None
        return 0, ret, None
```

- Open the file ```sample/extensions/features.yml```. The file should look something like this.
- This file specifies where new commands are to be read.
- For example, if you want to add a package to read, add a new ```package``` and ```prefix``` to ```features.cli```.
- Note that ```features.web``` can be used to add a new web screen.
- If you only want to call commands added in ```features.cli``` via RESTAPI, no additional implementation is needed in ```features.web```.


```yml
features:
  cli:
    - package: sample.app.features.cli
      prefix: sample_
  web:
    - package: sample.app.features.web
      prefix: sample_web_
args:
  cli:
    - rule:
        mode: web
      default:
      coercion:
        assets:
          - f"{Path(self.ver.__file__).parent / 'web' / 'assets'}"
        doc_root: f"{Path(self.ver.__file__).parent / 'web'}"
    - rule:
        mode: gui
      default:
      coercion:
        assets:
          - f"{Path(self.ver.__file__).parent / 'web' / 'assets'}"
        doc_root: f"{Path(self.ver.__file__).parent / 'web'}"
```

- The following files should also be known when using commands on the web screen or RESTAPI.
- Open the file ```sample/extensions/user_list.yml```. The file should look something like this.
- This file manages the users and groups that are allowed Web access and their rules.
- The rule of the previous command is ```allow``` for users in the ```user``` group in ```cmdrule.rules```.


```yml
users:
- uid: 1
  name: admin
  password: XXXXXXXXXXX
  hash: plain
  groups: [admin]
  email: admin@aaa.bbb.jp
- uid: 101
  name: user01
  password: XXXXXXXXXXX
  hash: md5
  groups: [user]
  email: user01@aaa.bbb.jp
- uid: 102
  name: user02
  password: XXXXXXXXXXX
  hash: sha1
  groups: [readonly]
  email: user02@aaa.bbb.jp
- uid: 103
  name: user03
  password: XXXXXXXXXXX
  hash: sha256
  groups: [editor]
  email: user03@aaa.bbb.jp
groups:
- gid: 1
  name: admin
- gid: 101
  name: user
- gid: 102
  name: readonly
  parent: user
- gid: 103
  name: editor
  parent: user
cmdrule:
  policy: deny # allow, deny
  rules:
  - groups: [admin]
    rule: allow
  - groups: [user]
    mode: client
    cmds: [file_download, file_list, server_info]
    rule: allow
  - groups: [user]
    mode: server
    cmds: [list]
    rule: allow
  - groups: [editor]
    mode: client
    cmds: [file_copy, file_mkdir, file_move, file_remove, file_rmdir, file_upload]
    rule: allow
pathrule:
  policy: deny # allow, deny
  rules:
  - groups: [admin]
    paths: [/]
    rule: allow
  - groups: [user]
    paths: [/signin, /assets, /bbforce_cmd, /copyright, /dosignin, /dosignout,
            /exec_cmd, /exec_pipe, /filer, /gui, /get_server_opt, /usesignout, /versions_cmdbox, /versions_used]
    rule: allow
  - groups: [readonly]
    paths: [/gui/del_cmd, /gui/del_pipe, /gui/save_cmd, /gui/save_pipe]
    rule: deny
  - groups: [editor]
    paths: [/gui/del_cmd, /gui/del_pipe, /gui/save_cmd, /gui/save_pipe]
    rule: allow
oauth2:
  providers:
    google:
      enabled: false
      client_id: XXXXXXXXXXX
      client_secret: XXXXXXXXXXX
      redirect_uri: https://localhost:8443/oauth2/google/callback
      scope: ['email']
      note:
      - https://developers.google.com/identity/protocols/oauth2/web-server?hl=ja#httprest
    github:
      enabled: false
      client_id: XXXXXXXXXXX
      client_secret: XXXXXXXXXXX
      redirect_uri: https://localhost:8443/oauth2/github/callback
      scope: ['user:email']
      note:
      - https://docs.github.com/ja/apps/oauth-apps/building-oauth-apps/authorizing-oauth-apps#scopes
```

- See the documentation for references to each file.
- Documentation is [here](https://hamacom2004jp.github.io/cmdbox/).


# Lisence

This project is licensed under the MIT License, see the LICENSE file for details
