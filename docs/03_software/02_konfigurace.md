# Konfigurace software

## Systémová konfigurace
1. **Základní nastavení**
   ```bash
   sudo raspi-config
   # Nastavit časové pásmo
   # Nastavit lokalizaci
   # Povolit SSH
   # Povolit SPI/I2C
   ```

2. **Síťové nastavení**
   ```bash
   sudo nano /etc/dhcpcd.conf
   # Statická IP adresa
   interface eth0
   static ip_address=192.168.1.100/24
   static routers=192.168.1.1
   static domain_name_servers=8.8.8.8
   ```

3. **Firewall**
   ```bash
   sudo apt install ufw
   sudo ufw allow ssh
   sudo ufw allow http
   sudo ufw enable
   ```

## SDR konfigurace
1. **RTL-SDR**
   ```bash
   sudo nano /etc/modprobe.d/rtl-sdr-blacklist.conf
   blacklist dvb_usb_rtl28xxu
   blacklist rtl2832
   blacklist rtl2830
   ```

2. **GNU Radio**
   ```bash
   sudo nano /etc/gnuradio/conf.d/rtl-sdr.conf
   [rtl-sdr]
   device=0
   sample_rate=2.4e6
   ```

3. **SDR++**
   ```bash
   sudo nano /etc/sdrpp/config.json
   {
     "device": "rtl-sdr",
     "frequency": 433e6,
     "sample_rate": 2.4e6
   }
   ```

## WiFi konfigurace
1. **Monitorovací režim**
   ```bash
   sudo airmon-ng check kill
   sudo airmon-ng start wlan0
   ```

2. **Kismet**
   ```bash
   sudo nano /etc/kismet/kismet.conf
   source=rtl433
   source=wlan0
   ```

3. **Wireshark**
   ```bash
   sudo usermod -a -G wireshark $USER
   sudo setcap cap_net_raw,cap_net_admin+eip /usr/bin/dumpcap
   ```

## Monitorovací konfigurace
1. **Prometheus**
   ```bash
   sudo nano /etc/prometheus/prometheus.yml
   global:
     scrape_interval: 15s
   scrape_configs:
     - job_name: 'node'
       static_configs:
         - targets: ['localhost:9100']
   ```

2. **Grafana**
   ```bash
   sudo nano /etc/grafana/grafana.ini
   [server]
   http_port = 3000
   domain = localhost
   ```

3. **Node Exporter**
   ```bash
   sudo nano /etc/default/prometheus-node-exporter
   ARGS="--collector.textfile.directory /var/lib/node_exporter/textfile_collector"
   ```

## Webové rozhraní
1. **Flask**
   ```bash
   nano app/config.py
   SECRET_KEY = 'your-secret-key'
   DEBUG = False
   ```

2. **Nginx**
   ```bash
   sudo nano /etc/nginx/sites-available/default
   server {
       listen 80;
       server_name localhost;
       location / {
           proxy_pass http://localhost:5000;
       }
   }
   ```

3. **SSL**
   ```bash
   sudo apt install certbot python3-certbot-nginx
   sudo certbot --nginx -d your-domain.com
   ```

## Automatizace
1. **Systemd služby**
   ```bash
   sudo nano /etc/systemd/system/monitoring.service
   [Unit]
   Description=Monitoring Service
   After=network.target
   
   [Service]
   ExecStart=/usr/local/bin/monitoring.py
   Restart=always
   
   [Install]
   WantedBy=multi-user.target
   ```

2. **Cron úlohy**
   ```bash
   crontab -e
   0 * * * * /path/to/backup.sh
   5 * * * * /path/to/cleanup.sh
   ```

3. **Logování**
   ```bash
   sudo nano /etc/rsyslog.d/monitoring.conf
   local0.*    /var/log/monitoring.log
   ``` 