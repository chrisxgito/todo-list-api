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
```

`sudo reboot`

### user(s) anlegen

`sudo adduser willi`

`sudo adduser fernzugriff`

### admin rechte geben

`sudo usermod -aG sudo fernzugriff`

- alle andere groups `-a`
- und sudo group hunzfügen `-G`

