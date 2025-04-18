# Zálohování

## Konfigurační zálohy
1. **Systémová konfigurace**
   ```bash
   #!/bin/bash
   BACKUP_DIR="/backup/config"
   DATE=$(date +%Y%m%d)
   
   tar -czf $BACKUP_DIR/system_config_$DATE.tar.gz /etc
   ```

2. **Aplikační konfigurace**
   ```bash
   #!/bin/bash
   BACKUP_DIR="/backup/apps"
   DATE=$(date +%Y%m%d)
   
   tar -czf $BACKUP_DIR/apps_config_$DATE.tar.gz \
     /etc/prometheus \
     /etc/grafana \
     /etc/nginx
   ```

3. **Skripty**
   ```bash
   #!/bin/bash
   BACKUP_DIR="/backup/scripts"
   DATE=$(date +%Y%m%d)
   
   tar -czf $BACKUP_DIR/scripts_$DATE.tar.gz /usr/local/bin
   ```

## Datové zálohy
1. **Databáze**
   ```bash
   #!/bin/bash
   BACKUP_DIR="/backup/db"
   DATE=$(date +%Y%m%d)
   
   mysqldump -u user -p database > $BACKUP_DIR/db_$DATE.sql
   ```

2. **Logy**
   ```bash
   #!/bin/bash
   BACKUP_DIR="/backup/logs"
   DATE=$(date +%Y%m%d)
   
   tar -czf $BACKUP_DIR/logs_$DATE.tar.gz /var/log
   ```

3. **Monitorovací data**
   ```bash
   #!/bin/bash
   BACKUP_DIR="/backup/monitoring"
   DATE=$(date +%Y%m%d)
   
   tar -czf $BACKUP_DIR/monitoring_$DATE.tar.gz \
     /var/lib/prometheus \
     /var/lib/grafana
   ```

## Automatické zálohování
1. **Cron úlohy**
   ```bash
   crontab -e
   0 2 * * * /path/to/backup_config.sh
   0 3 * * * /path/to/backup_data.sh
   0 4 * * * /path/to/backup_monitoring.sh
   ```

2. **Rotace záloh**
   ```bash
   #!/bin/bash
   BACKUP_DIR="/backup"
   RETENTION_DAYS=30
   
   find $BACKUP_DIR -type f -mtime +$RETENTION_DAYS -delete
   ```

3. **Kontrola záloh**
   ```bash
   #!/bin/bash
   BACKUP_DIR="/backup"
   
   for file in $BACKUP_DIR/*.tar.gz; do
     if ! tar -tzf "$file" > /dev/null; then
       echo "Chyba v zálohovacím souboru: $file"
     fi
   done
   ```

## Obnova záloh
1. **Konfigurace**
   ```bash
   #!/bin/bash
   BACKUP_FILE="/backup/config/system_config_20230101.tar.gz"
   
   tar -xzf $BACKUP_FILE -C /
   ```

2. **Data**
   ```bash
   #!/bin/bash
   BACKUP_FILE="/backup/db/db_20230101.sql"
   
   mysql -u user -p database < $BACKUP_FILE
   ```

3. **Monitorovací data**
   ```bash
   #!/bin/bash
   BACKUP_FILE="/backup/monitoring/monitoring_20230101.tar.gz"
   
   tar -xzf $BACKUP_FILE -C /
   ```

## Vzdálené zálohování
1. **RSync**
   ```bash
   #!/bin/bash
   REMOTE_HOST="backup.server"
   REMOTE_DIR="/backup"
   LOCAL_DIR="/backup"
   
   rsync -avz $LOCAL_DIR $REMOTE_HOST:$REMOTE_DIR
   ```

2. **SCP**
   ```bash
   #!/bin/bash
   REMOTE_HOST="backup.server"
   REMOTE_DIR="/backup"
   LOCAL_FILE="/backup/backup.tar.gz"
   
   scp $LOCAL_FILE $REMOTE_HOST:$REMOTE_DIR
   ```

3. **SFTP**
   ```bash
   #!/bin/bash
   REMOTE_HOST="backup.server"
   REMOTE_DIR="/backup"
   LOCAL_FILE="/backup/backup.tar.gz"
   
   sftp $REMOTE_HOST << EOF
   put $LOCAL_FILE $REMOTE_DIR
   EOF
   ```

## Šifrování záloh
1. **GPG**
   ```bash
   #!/bin/bash
   BACKUP_FILE="/backup/backup.tar.gz"
   GPG_KEY="backup@example.com"
   
   gpg --encrypt --recipient $GPG_KEY $BACKUP_FILE
   ```

2. **OpenSSL**
   ```bash
   #!/bin/bash
   BACKUP_FILE="/backup/backup.tar.gz"
   ENCRYPTED_FILE="$BACKUP_FILE.enc"
   
   openssl enc -aes-256-cbc -salt -in $BACKUP_FILE -out $ENCRYPTED_FILE
   ```

3. **Dešifrování**
   ```bash
   #!/bin/bash
   ENCRYPTED_FILE="/backup/backup.tar.gz.enc"
   DECRYPTED_FILE="/backup/backup.tar.gz"
   
   openssl enc -aes-256-cbc -d -in $ENCRYPTED_FILE -out $DECRYPTED_FILE
   ```

## Monitoring záloh
1. **Logování**
   ```bash
   #!/bin/bash
   LOG_FILE="/var/log/backup.log"
   
   echo "$(date): Backup started" >> $LOG_FILE
   # Backup commands
   echo "$(date): Backup completed" >> $LOG_FILE
   ```

2. **Notifikace**
   ```bash
   #!/bin/bash
   EMAIL="admin@example.com"
   
   if [ $? -eq 0 ]; then
     echo "Backup successful" | mail -s "Backup Status" $EMAIL
   else
     echo "Backup failed" | mail -s "Backup Status" $EMAIL
   fi
   ```

3. **Kontrola místa**
   ```bash
   #!/bin/bash
   BACKUP_DIR="/backup"
   MIN_SPACE=1000000 # 1GB in KB
   
   if [ $(df -k $BACKUP_DIR | awk 'NR==2 {print $4}') -lt $MIN_SPACE ]; then
     echo "Varování: Málo místa pro zálohy"
   fi
   ``` 