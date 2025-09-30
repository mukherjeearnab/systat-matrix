
echo "Cleaning Previous Files..."
rm -rf /opt/systat-matrix

echo "Cloning Latest Release..."
git clone https://github.com/mukherjeearnab/systat-matrix.git /opt/systat-matrix

echo "Setting Permissions..."
chown -R root:root /opt/systat-matrix

echo "Cleaning Service Files..."
bash /opt/systat-matrix/clean.sh

echo "Setting Permissions..."
chmod +x /opt/systat-matrix/run.sh

echo "Installing Python Dependencies..."
(PKG_MANAGER=$(command -v pip3 || command -v pip) && $PKG_MANAGER install psutil gputil)

echo "Copying Service Files..."
cp /opt/systat-matrix/systat.service /etc/systemd/system/systat.service
cp /opt/systat-matrix/systat.timer /etc/systemd/system/systat.timer

echo "Starting Services..."
systemctl daemon-reload
systemctl enable systat.timer
systemctl start systat.timer


systemctl list-timers | grep systat
journalctl -u systat.service -f
