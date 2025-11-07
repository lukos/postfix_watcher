# Postfix Watcher

> This has only just been started and is not ready for use or feedback yet!

A lightweight Python daemon to monitor Postfix mail logs and trigger API and Postfix actions on matching messages.

## Install
Download the latest installer tarball from [Github](https://github.com/lukos/postfix_watcher/releases)

You will also need to give sudo privileges for `postsuper` to the user running the service if you want to use the `delete_message` configuration option. This can be done
by making sure that `sudoers.d` directory is imported into `/etc/sudoers` which is done automatically in the latest Debian/Ubuntu releases. You should edit a config file
using `visudo` so that it can check the format is correct or you can run something like `echo 'postfixwatcher ALL=(ALL) NOPASSWD: /usr/sbin/postsuper' | sudo tee /etc/sudoers.d/postfixwatcher`

```sh
sudo useradd --system postfixwatcher
sudo usermod -aG adm postfixwatcher

sudo mkdir -p /var/lib/postfix-watcher
sudo chown postfixwatcher:postfixwatcher /var/lib/postfix-watcher

tar -xzf postfix-watcher-v0.1.4-linux-x64.tar.gz
sudo cp bin/postfix-watcher /usr/local/bin/
# Optional depending on whether you already have a config file
sudo mkdir /etc/postfix-watcher.d
sudo cp config/postfix-watcher.yaml.dist /etc/postfix-watcher.d/00-postfix-watcher.yaml

sudo cp systemd/postfix-watcher.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now postfix-watcher
```

## Configure
The default location for configuration is `/etc/postfix-watcher.d/` and follows the usual rules of applying the rule files in alphabetical order. If you change this location, you need to pass the new path to the executable using `--config-dir` and/or change the service unit file to suit. Dictionaries are deep-merged, lists are concatenated and scalars are overwritten by later files.

This yaml file has some defaults that you can modify but the general idea is that all settings in the default section can be overridden inside each individual rule except rule name and pattern.

Auth can be set either with `endpoint_token` to use bearer token auth (you don't need to include "Bearer") or otherwise you can set `endpoint_username` and `endpoint_password` to use basic auth. If
you set both the token and the username/password, it will pass both so be careful since that is likely to cause a problem.

The `endpoint_message` is the json passed to the API endpoint. You can use environment variable embedding just like bash e.g. `${MY_VAR}` and if the variable is not defined, you will simply get an empty
string in that location. 

The rule names are just for ease-of-use and are added to some of the logging messages but their exact value is not important.

Patterns for each rule are Python regexes but since they are regexes, they can also just use normal text as long as you escape any special regex chars `. ^ $ * + ? { } [ ] \ | ( )` with a backslash. If you want capture any data from the log line to use in the `endpoint_message` you can use Python named capture groups e.g. `pattern: "to=<(?P<to_email>[^>]+)> The recipient's inbox is out of storage space"` which will allow you to use `${to_email}` in the endpoint message.


## Run
```sh
postfix-watcher --config /etc/postfix-watcher.yaml
```

## Ansible
Use the included Ansible playbook to deploy.

## Systemd
The unit file in the package can be used to run as a service. Check the `User` if you are planning to change it from the default.
