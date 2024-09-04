/*
    A Terraform module to create EC2 Instance Web Servers
*/

// VPC
resource "aws_vpc" "vpc" {
  cidr_block = "10.0.0.0/16"
  tags = {
    Name = "vpc-${var.suffix}"
  }
}

// Internet Gateway
resource "aws_internet_gateway" "vpc_ig" {
  
  vpc_id = aws_vpc.vpc.id

  tags = {
    Name = "vpc-ig-${var.suffix}"
  }
}

// Route Table
resource "aws_route_table" "vpc_route_table" {
  vpc_id = aws_vpc.vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.vpc_ig.id
  }

  tags = {
    Name = "vpc-route-table-${var.suffix}"
  }
}

// Subnet
resource "aws_subnet" "vpc_subnet" {

  assign_ipv6_address_on_creation = false
  vpc_id = aws_vpc.vpc.id
  availability_zone = "us-east-1c"
  map_public_ip_on_launch = true
  cidr_block = "10.0.0.0/24"

  tags = {
    Name = "vpc-subnet-${var.suffix}"
  }
}

// Route Table Association to Subnet
resource "aws_route_table_association" "rt_association" {
  
  route_table_id = aws_route_table.vpc_route_table.id
  subnet_id = aws_subnet.vpc_subnet.id
}

// Security Group
resource "aws_security_group" "security_group" {
  vpc_id = aws_vpc.vpc.id
  description = "Allow all HTTP(s) and private ssh traffic to EC2 Instance"

  tags = {
    Name = "vpc-sg-${var.suffix}"
  }
}

// Security Group Ingress Rules
resource "aws_vpc_security_group_ingress_rule" "sg_ingress_rule_tcp_443" {
  security_group_id = aws_security_group.security_group.id
  cidr_ipv4 = "0.0.0.0/0"
  from_port = 443
  to_port = 443
  ip_protocol = "tcp"
  description = "Allow https traffic to instance."
}

resource "aws_vpc_security_group_ingress_rule" "sg_ingress_rule_tcp_80" {
  security_group_id = aws_security_group.security_group.id
  cidr_ipv4 = "0.0.0.0/0"
  from_port = 80
  to_port = 80
  ip_protocol = "tcp"
  description = "Allow http traffic to instance."
}

resource "aws_vpc_security_group_ingress_rule" "sg_ingress_rule_ssh" {
  security_group_id = aws_security_group.security_group.id
  cidr_ipv4 = "10.0.0.0/24"
  from_port = 22
  to_port = 22
  ip_protocol = "tcp"
  description = "Allow ssh traffic to instance from private ips in subnet."
}

resource "aws_vpc_security_group_ingress_rule" "sg_ingress_rule_ics" {
  security_group_id = aws_security_group.security_group.id
  cidr_ipv4 = "18.206.107.24/29"
  from_port = 22
  to_port = 22
  ip_protocol = "tcp"
  description = "Allow ssh traffic to instance from EC2 Instance Connect service."
}

// Security Group Egress Rules
resource "aws_vpc_security_group_egress_rule" "sg_egress_rule" {
  security_group_id = aws_security_group.security_group.id
  cidr_ipv4 = "0.0.0.0/0"
  from_port = 0
  to_port = 65535
  ip_protocol = "tcp"
  description = "Allow our instances to send TCP traffic to the internet."
}

// AMI Lookup
data "aws_ami" "ami" {
  most_recent = true
  filter {
    name = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }

  filter {
    name = "virtualization-type"
    values = ["hvm"]
  }

  owners = ["amazon"]
}

// EC2 Instance
resource "aws_instance" "web_server" {
  ami = data.aws_ami.ami.id
  subnet_id = aws_subnet.vpc_subnet.id
  vpc_security_group_ids = [aws_security_group.security_group.id]
  availability_zone = aws_subnet.vpc_subnet.availability_zone
  instance_type = "t3.micro"
  user_data_base64 = base64encode("#!/bin/bash \nsudo aput update \nsudo apt install nginx -y \nsudo ufw allow 'Nginx HTTP'")

  tags = {
    Name = "ec2-instance-${var.suffix}"
  }
}