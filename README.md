# 3D Printed LED Clock

# UNDER CONSTRUCTION

## Instructions
- **SSH into the Pi Zero as root or `sudo su`.  For neopixel to work, it must be ran as root.**

### Install Dependencies
```
apt install -y git python3-pip
pip3 install rpi_ws281x adafruit-circuitpython-neopixel
```

### Clone git repo
```
mkdir -p /root/git
cd /root/git
git clone https://github.com/sn0wfa11/led_clock
```

### Make symbolic Link to the service
`ln -s /root/git/led_clock/code/led_clock /etc/init.d/led_clock`

### Start the clock service
`/etc/init.d/led_clock start`

### Set service to start on boot
`update-rc.d led_clock defaults`

### Setup update cron job
The update script will stop the clock at midnight on Sundays, pull any updates from this repo, then start the clock again.

**Do this as root**

`crontab -e`

- If there is no crontab for root, it will have you select an editor. Nano is the easiest to use.
- Paste the following in as the last line in the crontab file:

`0 0 * * 0 /root/git/led_clock/update.sh`

- Exit and Save in Nano
```
Control+X
Y
<Enter>
```

You can change the time that this executes by changing the crontab entry. See this link for assistance.

https://crontab.guru/

## Parts
### LED Strip
https://www.amazon.com/gp/product/B01MG49QKD

### Rpi Zero W
https://www.amazon.com/gp/product/B06XFZC3BX/

### Power Supply
https://www.amazon.com/gp/product/B01M0KLECZ/

### Power Jack - Female
https://www.amazon.com/gp/product/B01M1D5GIP/

### Wire:
https://www.amazon.com/gp/product/B07PNDL6NT/
