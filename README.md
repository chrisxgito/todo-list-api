# todo-list-api

## raspberry Pi einrichten

os version bullseye war bereits auf eigener sd-Karte installiert

Befehl um Betriebssystem zu ermitteln: `hostnamectl`

→ Debian GNU/Linux 11 (Bullseye) Betriebssystem

### statische ip setzen
`sudo nano /etc/dhcpcd.conf`

darin hinzufügen:

```
interface eth0
static ip_address=192.168.24.189/24
static routers=192.168.24.254
static domain_name_servers=8.8.8.8 8.8.4.4
```
Funktionalität mit statischen Standardgateway- und DNS-Einstellungen konnte nicht mehr getestet werden

Ermitteln durch folgende Befehle:
- DNS Server: `sudo nano /etc/resolv.conf`
- Gateway: `ip r`

`sudo reboot`

### user(s) anlegen

`sudo adduser willi`

`sudo adduser fernzugriff`

### admin rechte geben

`sudo usermod -aG sudo fernzugriff`

- alle andere groups `-a`
- und sudo group hinzfügen `-G`

## Docker
`sudo docker build https://github.com/chrisxgito/todo-list-api.git#main  -t todoserver`

`sudo docker run -p 5000:5000 -d todoserver`

Server ist via 192.168.24.189:5000 erreichbar