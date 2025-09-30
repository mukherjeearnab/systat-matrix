systemctl stop systat.timer
systemctl disable systat.timer
systemctl stop systat.service
systemctl disable systat.service

rm /etc/systemd/system/systat.timer
rm /etc/systemd/system/systat.service

systemctl daemon-reload

systemctl list-timers --all | grep systat
systemctl status systat.service