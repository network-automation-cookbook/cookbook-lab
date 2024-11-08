
Random:
Droplet ID is 453392670
Public IPv4 is 143.198.111.43


```
root@cookbook-lab-droplet:~# clab inspect -t cookbook-lab/containerlab/lab.yml 
INFO[0000] Parsing & checking topology file: lab.yml    
+---+---------+--------------+---------------------------------+---------------+---------+------------------+--------------+
| # |  Name   | Container ID |              Image              |     Kind      |  State  |   IPv4 Address   | IPv6 Address |
+---+---------+--------------+---------------------------------+---------------+---------+------------------+--------------+
| 1 | ceos-01 | fd4796dd87d2 | ceos:image                      | arista_ceos   | running | 198.51.100.11/24 | N/A          |
| 2 | ceos-02 | 208f7aa307f8 | ceos:image                      | arista_ceos   | running | 198.51.100.12/24 | N/A          |
| 3 | client1 | 9a9664b094b4 | ghcr.io/hellt/network-multitool | linux         | running | 198.51.100.2/24  | N/A          |
| 4 | client2 | c5ff7c372e0d | ghcr.io/hellt/network-multitool | linux         | running | 198.51.100.3/24  | N/A          |
| 5 | crpd-01 | c44630d454fd | crpd:24.2R1.14                  | juniper_crpd  | running | 198.51.100.21/24 | N/A          |
| 6 | crpd-02 | 733cc1cbc531 | crpd:24.2R1.14                  | juniper_crpd  | running | 198.51.100.22/24 | N/A          |
| 7 | srl-01  | 93311be4f162 | ghcr.io/nokia/srlinux           | nokia_srlinux | running | 198.51.100.31/24 | N/A          |
| 8 | srl-02  | 7152d9f522f5 | ghcr.io/nokia/srlinux           | nokia_srlinux | running | 198.51.100.32/24 | N/A          |
+---+---------+--------------+---------------------------------+---------------+---------+------------------+--------------+
```

```ini
[linux]
client1 ansible_host=198.51.100.2
client2 ansible_host=198.51.100.3

[arista_ceos]
ceos-01 ansible_host=198.51.100.11
ceos-02 ansible_host=198.51.100.12

[juniper_crpd]
crpd-01 ansible_host=198.51.100.21
crpd-02 ansible_host=198.51.100.22

[nokia_srlinux]
srl-01 ansible_host=198.51.100.31
srl-02 ansible_host=198.51.100.32
```

```yaml
---
network_equipment:
  children:
    arista_ceos:
    juniper_crpd:
    nokia_srlinux:

linux:
  hosts:
    client1:
      ansible_host: 198.51.100.2
    client2:
      ansible_host: 198.51.100.3
arista_ceos:
  hosts:
    ceos-01:
      ansible_host: 198.51.100.11
    ceos-02:
      ansible_host: 198.51.100.12
juniper_crpd:
  hosts:
    crpd-01:
      ansible_host: 198.51.100.21
    crpd-02:
      ansible_host: 198.51.100.22
nokia_srlinux:
  hosts:
    srl-01:
      ansible_host: 198.51.100.31
    srl-02:
      ansible_host: 198.51.100.32
...
```

```
root@cookbook-lab-droplet:~# ansible --version
ansible [core 2.17.5]
  config file = None
  configured module search path = ['/root/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']
  ansible python module location = /root/miniconda/lib/python3.12/site-packages/ansible
  ansible collection location = /root/.ansible/collections:/usr/share/ansible/collections
  executable location = /root/miniconda/bin/ansible
  python version = 3.12.4 | packaged by Anaconda, Inc. | (main, Jun 18 2024, 15:12:24) [GCC 11.2.0] (/root/miniconda/bin/python)
  jinja version = 3.1.4
  libyaml = True
```


▶ ansible-inventory -i tmp/hosts.yml --graph
@all:
  |--@ungrouped:
  |--@network_equipment:
  |  |--@arista_ceos:
  |  |  |--ceos-01
  |  |  |--ceos-02
  |  |--@juniper_crpd:
  |  |  |--crpd-01
  |  |  |--crpd-02
  |  |--@nokia_srlinux:
  |  |  |--srl-01
  |  |  |--srl-02
  |--@linux:
  |  |--client1
  |  |--client2


Notes:

```
root@cookbook-lab-droplet:~# clab inspect -t cookbook-lab/containerlab/lab.yml 
INFO[0000] Parsing & checking topology file: lab.yml    
+---+---------+--------------+---------------------------------+---------------+---------+------------------+--------------+
| # |  Name   | Container ID |              Image              |     Kind      |  State  |   IPv4 Address   | IPv6 Address |
+---+---------+--------------+---------------------------------+---------------+---------+------------------+--------------+
| 1 | ceos-01 | fd4796dd87d2 | ceos:image                      | arista_ceos   | running | 198.51.100.11/24 | N/A          |
| 2 | ceos-02 | 208f7aa307f8 | ceos:image                      | arista_ceos   | running | 198.51.100.12/24 | N/A          |
| 3 | client1 | 9a9664b094b4 | ghcr.io/hellt/network-multitool | linux         | running | 198.51.100.2/24  | N/A          |
| 4 | client2 | c5ff7c372e0d | ghcr.io/hellt/network-multitool | linux         | running | 198.51.100.3/24  | N/A          |
| 5 | crpd-01 | c44630d454fd | crpd:24.2R1.14                  | juniper_crpd  | running | 198.51.100.21/24 | N/A          |
| 6 | crpd-02 | 733cc1cbc531 | crpd:24.2R1.14                  | juniper_crpd  | running | 198.51.100.22/24 | N/A          |
| 7 | srl-01  | 93311be4f162 | ghcr.io/nokia/srlinux           | nokia_srlinux | running | 198.51.100.31/24 | N/A          |
| 8 | srl-02  | 7152d9f522f5 | ghcr.io/nokia/srlinux           | nokia_srlinux | running | 198.51.100.32/24 | N/A          |
+---+---------+--------------+---------------------------------+---------------+---------+------------------+--------------+
```

```ini
[linux]
client1 ansible_host=198.51.100.2
client2 ansible_host=198.51.100.3

[arista_ceos]
ceos-01 ansible_host=198.51.100.11
ceos-02 ansible_host=198.51.100.12

[juniper_crpd]
crpd-01 ansible_host=198.51.100.21
crpd-02 ansible_host=198.51.100.22

[nokia_srlinux]
srl-01 ansible_host=198.51.100.31
srl-02 ansible_host=198.51.100.32
```

```yaml
---
network_equipment:
  children:
    arista_ceos:
    juniper_crpd:
    nokia_srlinux:

linux:
  hosts:
    client1:
      ansible_host: 198.51.100.2
    client2:
      ansible_host: 198.51.100.3
arista_ceos:
  hosts:
    ceos-01:
      ansible_host: 198.51.100.11
    ceos-02:
      ansible_host: 198.51.100.12
juniper_crpd:
  hosts:
    crpd-01:
      ansible_host: 198.51.100.21
    crpd-02:
      ansible_host: 198.51.100.22
nokia_srlinux:
  hosts:
    srl-01:
      ansible_host: 198.51.100.31
    srl-02:
      ansible_host: 198.51.100.32
...
```

```
root@cookbook-lab-droplet:~# ansible --version
ansible [core 2.17.5]
  config file = None
  configured module search path = ['/root/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']
  ansible python module location = /root/miniconda/lib/python3.12/site-packages/ansible
  ansible collection location = /root/.ansible/collections:/usr/share/ansible/collections
  executable location = /root/miniconda/bin/ansible
  python version = 3.12.4 | packaged by Anaconda, Inc. | (main, Jun 18 2024, 15:12:24) [GCC 11.2.0] (/root/miniconda/bin/python)
  jinja version = 3.1.4
  libyaml = True
```


▶ ansible-inventory -i tmp/hosts.yml --graph
@all:
  |--@ungrouped:
  |--@network_equipment:
  |  |--@arista_ceos:
  |  |  |--ceos-01
  |  |  |--ceos-02
  |  |--@juniper_crpd:
  |  |  |--crpd-01
  |  |  |--crpd-02
  |  |--@nokia_srlinux:
  |  |  |--srl-01
  |  |  |--srl-02
  |--@linux:
  |  |--client1
  |  |--client2

```bash
▶ tree .
.
├── ansible.cfg
├── group_vars
│   ├── all.yml
│   └── nokia_srlinux.yml
├── host_vars
│   └── client2.yml
└── pb1.yml

2 directories, 5 files
```

# all.yml
---
ntp:
  - 192.168.1.10
  - 192.168.2.10
# nokia_srlinux.yml
---
ntp:
  - 192.168.1.10
  - 192.168.3.10
# client2.yml
---
ntp:
  - 192.168.2.10
  - 192.168.3.10


▶ ansible-inventory -i hosts.yml --graph --vars
@all:
  |--@ungrouped:
  |--@network_equipment:
  |  |--@arista_ceos:
  |  |  |--ceos-01
  |  |  |  |--{ansible_host = 198.51.100.11}
  |  |  |  |--{ntp = ['192.168.1.10', '192.168.2.10']}
  |  |  |--ceos-02
  |  |  |  |--{ansible_host = 198.51.100.12}
  |  |  |  |--{ntp = ['192.168.1.10', '192.168.2.10']}
  |  |--@juniper_crpd:
  |  |  |--crpd-01
  |  |  |  |--{ansible_host = 198.51.100.21}
  |  |  |  |--{ntp = ['192.168.1.10', '192.168.2.10']}
  |  |  |--crpd-02
  |  |  |  |--{ansible_host = 198.51.100.22}
  |  |  |  |--{ntp = ['192.168.1.10', '192.168.2.10']}
  |  |--@nokia_srlinux:
  |  |  |--srl-01
  |  |  |  |--{ansible_host = 198.51.100.31}
  |  |  |  |--{ntp = ['192.168.1.10', '192.168.3.10']}
  |  |  |--srl-02
  |  |  |  |--{ansible_host = 198.51.100.32}
  |  |  |  |--{ntp = ['192.168.1.10', '192.168.3.10']}
  |  |  |--{ntp = ['192.168.1.10', '192.168.3.10']}
  |--@linux:
  |  |--client1
  |  |  |--{ansible_host = 198.51.100.2}
  |  |  |--{ntp = ['192.168.1.10', '192.168.2.10']}
  |  |--client2
  |  |  |--{ansible_host = 198.51.100.3}
  |  |  |--{ntp = ['192.168.2.10', '192.168.3.10']}
  |--{ntp = ['192.168.1.10', '192.168.2.10']}



▶ ansible-playbook -i hosts.yml ch2_pb1.yml

PLAY [Initial Playbook] ****************************************************************************************************************************************************************************************************

TASK [Display Hostname] ****************************************************************************************************************************************************************************************************
ok: [client1] => {
    "msg": "Router name is client1"
}
ok: [client2] => {
    "msg": "Router name is client2"
}
ok: [ceos-01] => {
    "msg": "Router name is ceos-01"
}
ok: [ceos-02] => {
    "msg": "Router name is ceos-02"
}
ok: [crpd-01] => {
    "msg": "Router name is crpd-01"
}
ok: [crpd-02] => {
    "msg": "Router name is crpd-02"
}
ok: [srl-01] => {
    "msg": "Router name is srl-01"
}
ok: [srl-02] => {
    "msg": "Router name is srl-02"
}

TASK [Display the NTP Variables] *******************************************************************************************************************************************************************************************
ok: [client1] => {
    "msg": "client1 has NTP servers ['192.168.1.10', '192.168.2.10']"
}
ok: [client2] => {
    "msg": "client2 has NTP servers ['192.168.2.10', '192.168.3.10']"
}
ok: [ceos-01] => {
    "msg": "ceos-01 has NTP servers ['192.168.1.10', '192.168.2.10']"
}
ok: [ceos-02] => {
    "msg": "ceos-02 has NTP servers ['192.168.1.10', '192.168.2.10']"
}
ok: [crpd-01] => {
    "msg": "crpd-01 has NTP servers ['192.168.1.10', '192.168.2.10']"
}
ok: [crpd-02] => {
    "msg": "crpd-02 has NTP servers ['192.168.1.10', '192.168.2.10']"
}
ok: [srl-01] => {
    "msg": "srl-01 has NTP servers ['192.168.1.10', '192.168.3.10']"
}
ok: [srl-02] => {
    "msg": "srl-02 has NTP servers ['192.168.1.10', '192.168.3.10']"
}

PLAY RECAP *****************************************************************************************************************************************************************************************************************
ceos-01                    : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
ceos-02                    : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
client1                    : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
client2                    : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
crpd-01                    : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
crpd-02                    : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
srl-01                     : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
srl-02                     : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   




▶ ansible-playbook -i hosts.yml ch2_pb2.yml

PLAY [Initial Playbook] ****************************************************************************************************************************************************************************************************

TASK [Display Hostname] ****************************************************************************************************************************************************************************************************
ok: [client1] => {
    "msg": "Router name is client1"
}
ok: [client2] => {
    "msg": "Router name is client2"
}
skipping: [ceos-01]
skipping: [ceos-02]
skipping: [crpd-01]
skipping: [crpd-02]
skipping: [srl-01]
skipping: [srl-02]

TASK [Display the NTP Variables] *******************************************************************************************************************************************************************************************
skipping: [client1]
skipping: [client2]
ok: [ceos-01] => {
    "msg": "ceos-01 has NTP servers ['192.168.1.10', '192.168.2.10']"
}
ok: [ceos-02] => {
    "msg": "ceos-02 has NTP servers ['192.168.1.10', '192.168.2.10']"
}
ok: [crpd-01] => {
    "msg": "crpd-01 has NTP servers ['192.168.1.10', '192.168.2.10']"
}
ok: [crpd-02] => {
    "msg": "crpd-02 has NTP servers ['192.168.1.10', '192.168.2.10']"
}
ok: [srl-01] => {
    "msg": "srl-01 has NTP servers ['192.168.1.10', '192.168.3.10']"
}
ok: [srl-02] => {
    "msg": "srl-02 has NTP servers ['192.168.1.10', '192.168.3.10']"
}

PLAY RECAP *****************************************************************************************************************************************************************************************************************
ceos-01                    : ok=1    changed=0    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0   
ceos-02                    : ok=1    changed=0    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0   
client1                    : ok=1    changed=0    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0   
client2                    : ok=1    changed=0    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0   
crpd-01                    : ok=1    changed=0    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0   
crpd-02                    : ok=1    changed=0    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0   
srl-01                     : ok=1    changed=0    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0   
srl-02                     : ok=1    changed=0    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0   
