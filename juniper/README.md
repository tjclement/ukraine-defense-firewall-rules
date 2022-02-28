## Which IP blocklist to use

* If you want to block all non-spoofable IPs reported by [Grey Noise](https://www.greynoise.io/) to be targeting only Ukrainian IP space, use [https://api.greynoise.io/datashots/ukraine/ukraine.txt]().
* If you want to also block spoofable IPs, use [greynoise_spoofable_all.txt](https://tjclement.github.io/ukraine-defense-firewall-rules/palo-alto/greynoise_spoofable_all.txt) from this folder.
* For only IPs marked as scanning for active vulnerabilities, use `*_malicious.txt` from this folder.

## Blocking IPs on Juniper firewalls

Here's how to block IPs from dynamic blocklists on Juniper SRX firewalls:

### Creating a dynamic list
```
set security dynamic-address feed-server Russia-Bad url https://tjclement.github.io/ukraine-defense-firewall-rules/juniper
set security dynamic-address feed-server Russia-Bad update-interval 60
set security dynamic-address feed-server Russia-Bad hold-interval 3600
set security dynamic-address feed-server Russia-Bad feed-name Russia-Bad description Default-IPList
set security dynamic-address feed-server Russia-Bad feed-name Russia-Bad path greynoise_nonspoofed_malicious.txt
set security dynamic-address address-name Russia-Blacklist profile feed-name Russia-Bad
```

### Adding dynamic list to policies
```
set security policies from-zone Untrust to-zone Servers policy 0099-Block-Russia match source-address Russia-Blacklist
set security policies from-zone Untrust to-zone Servers policy 0099-Block-Russia match destination-address any
set security policies from-zone Untrust to-zone Servers policy 0099-Block-Russia match application any
set security policies from-zone Untrust to-zone Servers policy 0099-Block-Russia then deny
```