## Decision Environment Creation

In order to create a Execution Envionrment or in this case a Decision Enviornment, you will use the libary called `ansible-builder`. This is a abstraction layer to build a Docker container.

For full details on Execution Enviornments visit the Ansible documentation. 

https://ansible.readthedocs.io/projects/builder/en/latest/

### Create and Install Dependencies

1. Create a virutalenv directory to store python virtual environments.

```
root@cookbook-lab-droplet:~/cookbook-lab/chapters/ch14/decision_environment# mkdir ~/.virtualenv
```

2. Create the virtual environment and Activate it

```
root@cookbook-lab-droplet:~/cookbook-lab/chapters/ch14/decision_environment# python3 -m venv ~/.virtualenv/ansible-builder
```

```
root@cookbook-lab-droplet:~/cookbook-lab/chapters/ch14/decision_environment# source ~/.virtualenv/ansible-builder/bin/activate
(ansible-builder) root@cookbook-lab-droplet:~/cookbook-lab/chapters/ch14/decision_environment#
```

3. Install the dependencies into the virtual environment.

```
(ansible-builder) root@cookbook-lab-droplet:~/cookbook-lab/chapters/ch14/decision_environment# pip install -r venv_requirements.txt 
Collecting ansible-builder==3.1.0 (from -r venv_requirements.txt (line 1))
  Downloading ansible_builder-3.1.0-py3-none-any.whl.metadata (2.8 kB)
... omitted output ...
Installing collected packages: Parsley, typing_extensions, setuptools, rpds-py, PyYAML, packaging, distro, attrs, referencing, pbr, jsonschema-specifications, bindep, jsonschema, ansible-builder
Successfully installed Parsley-1.3 PyYAML-6.0.2 ansible-builder-3.1.0 attrs-25.3.0 bindep-2.12.0 distro-1.9.0 jsonschema-4.23.0 jsonschema-specifications-2024.10.1 packaging-24.2 pbr-6.1.1 referencing-0.36.2 rpds-py-0.23.1 setuptools-77.0.3 typing_extensions-4.12.2
```

4. Build the Decision Environment using Ansible Builder

```
(ansible-builder) root@cookbook-lab-droplet:~/cookbook-lab/chapters/ch14/decision_environment# ansible-builder build -f decision-environment.yml -t ghcr.io/jeffkala/awx_sample_project:latest
Running command:
  docker build -f context/Dockerfile -t ghcr.io/jeffkala/awx_sample_project:latest context
Complete! The build context can be found at: /root/cookbook-lab/chapters/ch14/decision_environment/context
```

5. Login to Docker Registry

```
export CR_PAT=ghp_<personal access token>
echo $CR_PAT | docker login ghcr.io -u jeffkala --password-stdin
```

6. Push the Container image to a registry.

```
docker push ghcr.io/jeffkala/awx_sample_project:latest
```

Once Ansible Builder is executed all the required context is saved into the directory and can be reused as needed. This includes the rendered Dockerfile.

These files have been committed to the repostiory for review as needed.
