rm -rf /opt/systat-matrix

git clone https://github.com/mukherjeearnab/systat-matrix.git /opt/systat-matrix

chown -R root:root /opt/systat-matrix

bash /opt/systat-matrix/clean.sh

chmod +x /opt/systat-matrix/run.sh

pip3 install psutil gputil

cp /opt/systat-matrix/systat.service /etc/systemd/system/systat.service

cp /opt/systat-matrix/systat.timer /etc/systemd/system/systat.timer

systemctl daemon-reload
systemctl enable systat.timer
systemctl start systat.timer


systemctl list-timers | grep systat
journalctl -u systat.service -f
