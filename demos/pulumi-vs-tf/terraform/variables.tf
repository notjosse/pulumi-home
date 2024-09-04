/*
    Required Variables
*/

variable "users" {
  description = "List of users that require vpcs."
  type = set(string)
}

/*
    Optional Variables
*/

variable "aws-region" {
  description = "The AWS region where resources will be created."
  type = string
  default = "us-east-1"
}

variable "env" {
  description = "Environment that resources will be created in."
  type = string
  default = "dev"
}