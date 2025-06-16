# Postfix Watcher

> This has only just been started and is not ready for use or feedback yet!

A lightweight Python daemon to monitor Postfix mail logs and trigger API and Postfix actions on matching messages.

## Install
Download the latest installer tarball from [Github](https://github.com/lukos/postfix_watcher/releases)

```sh
sudo useradd --system postfixwatcher
sudo usermod -aG adm postfixwatcher

sudo mkdir -p /var/lib/postfix-watcher
sudo chown postfixwatcher:postfixwatcher /var/lib/postfix-watcher

tar -xzf postfix-watcher-v0.1.3-linux-x64.tar.gz
sudo cp bin/postfix-watcher /usr/local/bin/
# Optional depending on whether you already have a config file
sudo cp config/postfix-watcher.yaml.dist /etc/postfix-watcher.yaml
sudo cp systemd/postfix-watcher.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now postfix-watcher
```

## Run
```sh
postfix-watcher --config /etc/postfix-watcher.yaml
```

## Ansible
Use the included Ansible playbook to deploy.

## Systemd
Included unit file to run as a service.
