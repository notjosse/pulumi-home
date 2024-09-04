import pulumi
from pulumi_aws import ec2

# Defines an EC2 instance and necessary resources

class EC2Instance(pulumi.ComponentResource):
     def __init__(self, name, suffix, num, opts = None):
        super().__init__('josse:demo:EC2Instance', name, None, opts)

        ## VPC
        vpc = ec2.Vpc(
            f'ec2-vpc-{suffix}',
            cidr_block='10.0.0.0/16',
            tags={
                "Name": f"ec2-vpc-{suffix}",
            },
        opts=pulumi.ResourceOptions(parent=self))

        ## Internet gateway
        igw = ec2.InternetGateway(
            f'vpc-ig-{suffix}',
            vpc_id=vpc.id,
            tags={
                "Name": f'vpc-ig-{suffix}',
            },
        opts=pulumi.ResourceOptions(parent=self))
        
        ## Route Table
        ec2_route_table = ec2.RouteTable(
            f'vpc-route-table-{suffix}',
            vpc_id=vpc.id,
            routes=[ec2.RouteTableRouteArgs(
                cidr_block='0.0.0.0/0',
                gateway_id=igw.id,
            )],
            tags={
                "Name": f'vpc-route-table-{suffix}',
            },
        opts=pulumi.ResourceOptions(parent=self))

        ## Subnet
        vpc_subnet = ec2.Subnet(
            f'vpc-subnet-{suffix}',
            assign_ipv6_address_on_creation=False,
            vpc_id=vpc.id,
            availability_zone='us-east-1c',
            map_public_ip_on_launch=True,
            cidr_block=f'10.0.{num}.0/24',
            tags={
                "Name": f'vpc-subnet-{suffix}',
            },
        opts=pulumi.ResourceOptions(parent=self))
        
        ## Route Table Association to Subnet
        ec2.RouteTableAssociation(
            f'vpc-route-table-asso-{suffix}',
            route_table_id=ec2_route_table.id,
            subnet_id=vpc_subnet.id,
        opts=pulumi.ResourceOptions(parent=self))
            
        ## Security Group
        ec2_security_group = ec2.SecurityGroup(
            f'ec2-instance-sg-{suffix}',
            vpc_id=vpc.id,
            description='Allow all HTTP(s) traffic to EC2 Instance',
            ingress=[
                ec2.SecurityGroupIngressArgs(
                    cidr_blocks=['0.0.0.0/0'],
                    from_port=443,
                    to_port=443,
                    protocol='tcp',
                    description='Allow https traffic to instance.'
                ),
                
                ec2.SecurityGroupIngressArgs(
                    cidr_blocks=['0.0.0.0/0'],
                    from_port=80,
                    to_port=80,
                    protocol='tcp',
                    description='Allow http traffic to instance.'
                ),

                ec2.SecurityGroupIngressArgs(
                    cidr_blocks=['10.0.0.0/24', '18.206.107.24/29'], # 18.206.107.24/29 is the EC2 Instance Connect service IP addresses for us-east-1
                    from_port=22,
                    to_port=22,
                    protocol='tcp',
                    description='Allow ssh traffic to instance from private ips and EC2 Instance Connect service.'
                ),
            ],
            egress=[
                ec2.SecurityGroupEgressArgs(
                    cidr_blocks=['0.0.0.0/0'],
                    from_port=0,
                    to_port=65535,
                    protocol='tcp',
                    description='Allow our instances to send TCP traffic to the internet.'
                ),
            ],
            tags={
                "Name": f'ec2-instance-sg-{suffix}',
            },
        opts=pulumi.ResourceOptions(parent=self))

        ## AMI Lookup
        ami = ec2.get_ami(
            most_recent=True,
            filters=[
                {
                    "name": "name",
                    "values": ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"],
                },
                {
                    "name": "virtualization-type",
                    "values": ["hvm"],
                },
            ],
            owners=["amazon"])

        ## EC2 Instance                        
        instance = ec2.Instance(
            f'ec2-instance-{suffix}',
            ami=ami.id,
            subnet_id=vpc_subnet.id,
            vpc_security_group_ids=[ec2_security_group.id],
            availability_zone=vpc_subnet.availability_zone,
            instance_type=ec2.InstanceType.T3_MICRO,
            user_data="""#!/bin/bash
sudo apt update
sudo apt install nginx -y
sudo ufw allow 'Nginx HTTP'
            """,
            tags={
                "Name": f'ec2-instance-{suffix}',
            },
        opts=pulumi.ResourceOptions(parent=self))

        self.vpc = vpc.id
        self.subnet_id = vpc_subnet.id
        self.instance_id = instance.id
        self.instance_state = instance.instance_state
        self.public_ip = instance.public_ip


        self.register_outputs({})
