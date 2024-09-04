output "vpc_id" {
  value = aws_vpc.vpc.id
}

output "vpc_arn" {
  value = aws_vpc.vpc.arn
}

output "subnet_id" {
    value = aws_subnet.vpc_subnet.id
}

output "instance_id" {
    value = aws_instance.web_server.id
}

output "instance_state" {
    value = aws_instance.web_server.instance_state
}

output "instance_public_ip" {
  value = aws_instance.web_server.public_ip
}