provider "aws" {
  region = "us-east-1"  # Change to your preferred region
}

# Get the default VPC
data "aws_vpc" "default" {
  default = true
}

data "aws_subnets" "public" {
  filter {
    name   = "map-public-ip-on-launch"
    values = ["true"]
  }
}

data "aws_subnet" "public" {
  id = tolist(data.aws_subnets.public.ids)[0]  # Pick the first matching public subnet
}

# Security Group allowing SSH access
resource "aws_security_group" "ssh_access" {
  name        = "allow_ssh"
  description = "Allow SSH access from the internet"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # WARNING: Open to the internet, restrict in production
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Fetch latest Ubuntu AMI
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"]  # Canonical's AWS account ID
  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-*22.04-amd64-server-*"]
  }
}

# EC2 Instance
resource "aws_instance" "ubuntu" {
  ami                    = data.aws_ami.ubuntu.id
  instance_type          = "t2.micro"
  subnet_id              = data.aws_subnet.public.id
  vpc_security_group_ids = [aws_security_group.ssh_access.id]
  associate_public_ip_address = true
  key_name = "cookbook-key"
}

output "public_ip" {
  value = aws_instance.ubuntu.public_ip
}

resource "null_resource" "ansible" {
  depends_on = [aws_instance.ubuntu]

  provisioner "local-exec" {
    command = <<EOT
      sleep 10
      ANSIBLE_HOST_KEY_CHECKING=False ansible all -i ${aws_instance.ubuntu.public_ip}, -u ubuntu --private-key /tmp/cookbook-key.pem -m ping
    EOT
  }
}

resource "null_resource" "blacklist_ips" {
  depends_on = [aws_instance.ubuntu]

  provisioner "local-exec" {
    command = <<EOT
      ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook -i ${aws_instance.ubuntu.public_ip}, -u ubuntu --private-key /tmp/cookbook-key.pem pb_blacklist_ips.yml
    EOT
  }
}
