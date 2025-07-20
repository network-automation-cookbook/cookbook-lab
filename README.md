<!-- [![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/network-cookbook-lab/network-cookbook-lab?quickstart=1&devcontainer_path=.devcontainer%2Fbatteries-included%2Fdevcontainer.json) -->

# Network Automation Cookbook Lab

This repository contains the resources for building and managing an network automation stack within a network lab environment, specifically designed for the "Network Automation Cookbook 2nd edition" book.

## Requirements

The lab environments are designed to set up a small network and an attached automation stack. Developed and tested on Debian-based systems, we provide **[setup](setup/README.md) documentation to guide** you through automatic setup on a DigitalOcean droplet. This process will provision, install dependencies, and configure the environment automatically. But if you want to host the lab environment, ensure the following:

- `docker` installed (version `26.1.1` or above)
- `containerlab` for the network lab (version `0.54.2` or above)
- `lab` for managing the network and lab stack
- Arista `cEOS` images for the `containerlab` environment. You can open an account and download them at [arista.com](https://www.arista.com)

For detailed setup instructions, please refer to the [setup README](./setup/README.md). It provides a comprehensive guide on installing the lab environment on a DigitalOcean Droplet.

### Prepare cEOS image

After downloading the image, use the following command to import them as Docker images:

```bash
# Import cEOS images as Docker images
docker import <path-to-image>/cEOS64-lab-<version>.tar.xz ceos:image
```

## Quickstart

To get started with the network lab stack, you need to:

1. Copy the necessary environment variables to configure the components used within the lab scenarios.

```bash
# Setup environment variables (edit the .env file to your liking)
cp example.env .env
```

2. Install the `lab` utility command that helps manage the entire lab environment. Example using `uv`:

```bash
# Install the python dependencies
uv pip install .
```

3. Test everything is working by deploying a lab that has most of the components configured and ready to go.

```bash
# Start the network lab
lab setup deploy
```

---

## Managing Lab Environment with `lab`

The `lab` utility tool simplifies managing and monitoring the network lab and other stack set up within this repository. It provides a suite of commands designed to streamline various tasks associated with your network infrastructure.

### Top-Level Commands

The `lab` utility includes five main commands to help manage the environment:

- **`lab setup`**: Manages the overall setup of a remote DigitalOcean droplet hosting this repository and its lab environment. This command simplifies the process of preparing a hosting environment for users.

- **`lab containerlab`**: Manages the `containerlab` pre-configured setup. All lab scenarios presented in the chapters operate under this network lab configuration.

- **`lab docker`**: Manages the Docker Compose setups for each lab scenario. It ensures the appropriate containers are running for each specific lab exercise.

### Example Usage

For instance, the `lab setup deploy` command builds and starts a `containerlab` environment along with the automation stack. This command sets up the entire lab scenario, ensuring that all necessary components are up and running.

```bash
# Start the network lab
❯ lab setup deploy


  _       _          _ _
 | |     | |        | (_)
 | | __ _| |__   ___| |_
 | |/ _` | '_ \ / __| | |
 | | (_| | |_) | (__| | |
 |_|\__,_|_.__/ \___|_|_| v0.2.0


Running command: ansible-playbook setup/create_droplet.yml -i setup/inventory/localhost.yaml
Enter the droplet image [ubuntu-22-04-x64]:
Enter the droplet size [s-4vcpu-16gb-amd]:
Enter the droplet region [fra1]:

PLAY [Stand up cookbook-droplet] ***************************************************************************

TASK [Create DigitalOcean Droplets] ************************************************************************
ok: [localhost]

TASK [Wait for droplets to be ready] ***********************************************************************
ok: [localhost]

TASK [Show Droplet info] ***********************************************************************************
ok: [localhost] => {}

MSG:

Droplet ID is 123456789
Public IPv4 is 192.0.2.191


PLAY RECAP *************************************************************************************************
localhost                  : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

Successfully ran: create droplets
End of task: create droplets
Droplets created successfully
Proceeding to setup the droplets
Running command: ansible-playbook setup/setup_droplet.yml -i setup/inventory/do_hosts.yaml -i setup/inventory/localhost.yaml
[WARNING]: Invalid characters were found in group names but not replaced, use -vvvv to see details

PLAY [Bootstrap cookbook-lab-droplet] **********************************************************************

TASK [Wait for connection to cookbook-lab-droplet] *********************************************************
ok: [cookbook-lab-droplet]

TASK [Install or upgrade aptitude] *************************************************************************
[WARNING]: Platform linux on host cookbook-lab-droplet is using the discovered Python interpreter at
/usr/bin/python3.10, but future installation of another Python interpreter could change the meaning of that
path. See https://docs.ansible.com/ansible-core/2.18/reference_appendices/interpreter_discovery.html for
more information.
changed: [cookbook-lab-droplet]

TASK [Install or upgrade system dependencies] **************************************************************
changed: [cookbook-lab-droplet]

TASK [Download Docker] *************************************************************************************
changed: [cookbook-lab-droplet]

TASK [Install Docker] **************************************************************************************
ok: [cookbook-lab-droplet]

TASK [Install Python packages] *****************************************************************************
changed: [cookbook-lab-droplet]

TASK [Download Miniconda python environment] ***************************************************************
changed: [cookbook-lab-droplet]

TASK [Install Miniconda] ***********************************************************************************
changed: [cookbook-lab-droplet]

TASK [Remove Miniconda installer] **************************************************************************
changed: [cookbook-lab-droplet]

TASK [Add miniconda bin to path] ***************************************************************************
ok: [cookbook-lab-droplet]

TASK [Create localhost records in /etc/hosts] **************************************************************
changed: [cookbook-lab-droplet] => (item=nautobot)

TASK [Download containerlab] *******************************************************************************
changed: [cookbook-lab-droplet]

TASK [Install containerlab] ********************************************************************************
ok: [cookbook-lab-droplet]

TASK [Copy cEOS container image] ***************************************************************************
changed: [cookbook-lab-droplet]

TASK [Import cEOS container image] *************************************************************************
ok: [cookbook-lab-droplet]

TASK [Copy CRPD container image] ***************************************************************************
changed: [cookbook-lab-droplet]

TASK [Load CPRD container image] ***************************************************************************
ok: [cookbook-lab-droplet]

PLAY [Setup labcli app] ************************************************************************************

TASK [Gathering Facts] *************************************************************************************
ok: [cookbook-lab-droplet]

TASK [Clone cookbook-lab] **********************************************************************************
changed: [cookbook-lab-droplet]

TASK [Copy .env file] **************************************************************************************
changed: [cookbook-lab-droplet]

TASK [Install cookbook-lab] ********************************************************************************
ok: [cookbook-lab-droplet]

TASK [Run lab batteries included] **************************************************************************
ok: [cookbook-lab-droplet]
FAILED - RETRYING: [cookbook-lab-droplet]: Wait for Nautobot to come up (50 retries left).
FAILED - RETRYING: [cookbook-lab-droplet]: Wait for Nautobot to come up (49 retries left).
FAILED - RETRYING: [cookbook-lab-droplet]: Wait for Nautobot to come up (48 retries left).
FAILED - RETRYING: [cookbook-lab-droplet]: Wait for Nautobot to come up (47 retries left).
FAILED - RETRYING: [cookbook-lab-droplet]: Wait for Nautobot to come up (46 retries left).
FAILED - RETRYING: [cookbook-lab-droplet]: Wait for Nautobot to come up (45 retries left).
FAILED - RETRYING: [cookbook-lab-droplet]: Wait for Nautobot to come up (44 retries left).
FAILED - RETRYING: [cookbook-lab-droplet]: Wait for Nautobot to come up (43 retries left).
FAILED - RETRYING: [cookbook-lab-droplet]: Wait for Nautobot to come up (42 retries left).
FAILED - RETRYING: [cookbook-lab-droplet]: Wait for Nautobot to come up (41 retries left).
FAILED - RETRYING: [cookbook-lab-droplet]: Wait for Nautobot to come up (40 retries left).
FAILED - RETRYING: [cookbook-lab-droplet]: Wait for Nautobot to come up (39 retries left).
FAILED - RETRYING: [cookbook-lab-droplet]: Wait for Nautobot to come up (38 retries left).
FAILED - RETRYING: [cookbook-lab-droplet]: Wait for Nautobot to come up (37 retries left).
FAILED - RETRYING: [cookbook-lab-droplet]: Wait for Nautobot to come up (36 retries left).
FAILED - RETRYING: [cookbook-lab-droplet]: Wait for Nautobot to come up (35 retries left).
FAILED - RETRYING: [cookbook-lab-droplet]: Wait for Nautobot to come up (34 retries left).
FAILED - RETRYING: [cookbook-lab-droplet]: Wait for Nautobot to come up (33 retries left).
FAILED - RETRYING: [cookbook-lab-droplet]: Wait for Nautobot to come up (32 retries left).
FAILED - RETRYING: [cookbook-lab-droplet]: Wait for Nautobot to come up (31 retries left).
FAILED - RETRYING: [cookbook-lab-droplet]: Wait for Nautobot to come up (30 retries left).

TASK [Wait for Nautobot to come up] ************************************************************************
ok: [cookbook-lab-droplet]

PLAY RECAP *************************************************************************************************
cookbook-lab-droplet     : ok=23   changed=13   unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

Successfully ran: create droplets
End of task: create droplets
Droplets setup successfully
```

At the end, in the host, you get the following:

```bash

root@cookbook-lab-droplet:~# clab inspect --all
╭───────────────────────────────────┬──────────┬─────────┬─────────────────────────────────┬─────────┬────────────────╮
│              Topology             │ Lab Name │   Name  │            Kind/Image           │  State  │ IPv4/6 Address │
├───────────────────────────────────┼──────────┼─────────┼─────────────────────────────────┼─────────┼────────────────┤
│ cookbook-lab/containerlab/lab.yml │ lab      │ ceos-01 │ arista_ceos                     │ running │ 198.51.100.11  │
│                                   │          │         │ ceos:image                      │         │ N/A            │
│                                   │          ├─────────┼─────────────────────────────────┼─────────┼────────────────┤
│                                   │          │ ceos-02 │ arista_ceos                     │ running │ 198.51.100.12  │
│                                   │          │         │ ceos:image                      │         │ N/A            │
│                                   │          ├─────────┼─────────────────────────────────┼─────────┼────────────────┤
│                                   │          │ client1 │ linux                           │ running │ 198.51.100.2   │
│                                   │          │         │ ghcr.io/hellt/network-multitool │         │ N/A            │
│                                   │          ├─────────┼─────────────────────────────────┼─────────┼────────────────┤
│                                   │          │ client2 │ linux                           │ running │ 198.51.100.3   │
│                                   │          │         │ ghcr.io/hellt/network-multitool │         │ N/A            │
│                                   │          ├─────────┼─────────────────────────────────┼─────────┼────────────────┤
│                                   │          │ crpd-01 │ juniper_crpd                    │ running │ 198.51.100.21  │
│                                   │          │         │ crpd:24.2R1.14                  │         │ N/A            │
│                                   │          ├─────────┼─────────────────────────────────┼─────────┼────────────────┤
│                                   │          │ crpd-02 │ juniper_crpd                    │ running │ 198.51.100.22  │
│                                   │          │         │ crpd:24.2R1.14                  │         │ N/A            │
│                                   │          ├─────────┼─────────────────────────────────┼─────────┼────────────────┤
│                                   │          │ srl-01  │ nokia_srlinux                   │ running │ 198.51.100.31  │
│                                   │          │         │ ghcr.io/nokia/srlinux           │         │ N/A            │
│                                   │          ├─────────┼─────────────────────────────────┼─────────┼────────────────┤
│                                   │          │ srl-02  │ nokia_srlinux                   │ running │ 198.51.100.32  │
│                                   │          │         │ ghcr.io/nokia/srlinux           │         │ N/A            │
╰───────────────────────────────────┴──────────┴─────────┴─────────────────────────────────┴─────────┴────────────────╯
```

---
