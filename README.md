# Postfix Watcher

> This has only just been started and is not ready for use or feedback yet!

A lightweight Python daemon to monitor Postfix mail logs and trigger API and Postfix actions on matching messages.

## Install
```sh
sudo useradd --system postfixwatcher
sudo usermod -aG adm postfixwatcher
pip install .

sudo cp ./systemd/postfix-watcher.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable postfix-watcher
sudo systemctl start postfix-watcher
```

## Run
```sh
postfix-watcher --config /etc/postfix-watcher.yaml
```

## Ansible
Use the included Ansible playbook to deploy.

## Systemd
Included unit file to run as a service.
