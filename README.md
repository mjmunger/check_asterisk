# check_asterisk

## Summary

This script monitors specific peers as their statuses are reported in `sip show peers`. You can specify which peer to monitor with the required `-p` parameter.

The script will parse the output of `sip show peers` and find the peer with the *name* specified in the `-p` parameter, and then check its status.

- If the status is "OK", it will check to see if the ping time is greater than 199ms, which will cause poor performance. If it is lagged, the script will exit with a `1` to generate a warning. Otheriwse, if the peer is "OK" the script will exit with a code `0` because all is well.
- If the status is "UNREACHABLE", it will exit with a code `2`, which will generate a critical warning.
- If the status is "Unknown", it will exit with a code `3`, which is a status unknown. 

## Requirements
- Python 3.7+  
- docopt  

## Installation

Run the `install.sh` script.

## Monitoring an Asterisk box

In addition to monitoring peers of an Asterisk box, you may also consider installing the `nagios-plugins-basic` package, and then using `check_by_ssh` to monitor:
1. The `/usr/sbin/asterisk` process. In most cases, there should only be one instance of asterisk running.
1. The disk.
1. Server load. Transcoding audio or a lot of concurrent calls can increase CPU load dramatically in some cases.

### Example Commands:

Checking the asterisk process:
`ssh root@voip.example.org "/usr/lib/nagios/plugins/check_procs -a /usr/sbin/asterisk -c 1:1"`

Checking the disk:
`ssh root@voip.example.org "/usr/lib/nagios/plugins/check_disk -w 75 -c 90 -p /"`

Checking CPU load:
`ssh root@voip.example.org "/usr/lib/nagios/plugins/check_load -r -w 0.15,0.10,0.05 -c 0.30,0.25,0.20`