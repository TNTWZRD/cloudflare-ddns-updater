# Cloudflare Dynamic DNS Multiple IP Updater

This script is used to update Multiple dynamic DNS entries for accounts on Cloudflare.

## Installation

```bash
git clone https://github.com/TNTWZRD/cloudflare-ddns-updater
```

## Usage
This script is used with crontab. Specify the frequency of execution through crontab.

```bash
# Recommended once per day
# * 0 * * * /bin/bash pyhton3 {Location of the script}
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Reference
This script was made with reference from [K0p1-Git]https://github.com/K0p1-Git/cloudflare-ddns-updater