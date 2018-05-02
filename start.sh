apt-get update
apt-get --assume-yes install cron

echo "Setting the cron actions"
cp /deploy/crontab_scrapper /etc/cron.d
service cron restart

echo "Starting the app"
python /deploy/source/api.py
