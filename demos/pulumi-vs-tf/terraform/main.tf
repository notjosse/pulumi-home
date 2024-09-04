/*
    An AWS Terraform Module
*/

locals {
  name = "josse"
}

module "module_dev" {
  source = "./modules/ec2_instance"
  count = var.env == "dev" ? length(var.users) : 0

  suffix = "user${count.index}"
}

module "module_prod" {
  source = "./modules/ec2_instance"
  for_each = var.env == "prod" ? var.users : []

  suffix = each.key
}