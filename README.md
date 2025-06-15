# Postfix Watcher

> This has only just been started and is not ready for use or feedback yet!

A lightweight Python daemon to monitor Postfix mail logs and trigger API and Postfix actions on matching messages.

## Install
```sh
# Download the latest installer tarball from [Github](https://github.com/lukos/postfix_watcher/releases)
sudo useradd --system postfixwatcher
sudo usermod -aG adm postfixwatcher

tar -xzf postfix-watcher-v0.1.0-linux-x64.tar.gz
sudo cp bin/postfix-watcher /usr/local/bin/
sudo cp config/postfix-watcher.yaml /etc/
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
