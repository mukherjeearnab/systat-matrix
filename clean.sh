sudo systemctl stop systat.timer
sudo systemctl disable systat.timer
sudo systemctl stop systat.service
sudo systemctl disable systat.service

sudo rm /etc/systemd/system/systat.timer
sudo rm /etc/systemd/system/systat.service

sudo systemctl daemon-reload
