# Pulumi vs Terraform

This demo will highlight some of the differences between Pulumi IaC and Terraform when defining infrastructure.

Main points:
- General Purpose Languages vs HCL
- State Management
- Component Resources vs Modules
- Stacks vs Module Calls
- Stack References vs Module Outputs
- Automation API
- Secrets Management

## General Purpose Languages vs HCL

**Pulumi** allows users to define infrastructure in their desired, supported, open source, general purpose language. This significantly lowers the barrier to entry for dev teams that want to define infrastructure as IaC. This also allows users to take advantage of the ecosystem of tools and frameworks available to the language they choose.

In contrast, **Terraform** uses a Domain Specific Language called Hashicorp Configuration Language (HCL) which is specific to just Terraform. Its closed source, and requires dev teams to pick up a new syntax and language separate from what they used to write their applicaiton.

Point goes to Pulumi for offering felixbility.

***Score: Pulumi: 1; Terraform: 0***

## State Management

By default, **Pulumi** invites you to log into your Pulumi Cloud account so that the state files can be securely stored and managed. If users choose to store the state file locally, they have the option to do so.

**Terraform** stores state files locally by default. This can become messy pretty quickly if you're managing multiple state files. This also doesn't scale if you have multiple users working on the same IaC module, so you will have to setup a remote backend eventually.

Point is evenly split as both tools allow users to manage state locally and remotely.

***Score: Pulumi: 2; Terraform: 1***

## Component Resources vs Modules

Pulumi Component Resources and Terraform Modules essentially accomplish the same thing; to encapsulate a set of resources that are tightly coupled with some predefined configurations.

Pulumi's implemenations is that of a class than extends the pulumi.ComponentResource class.

Terraform follows the standard module format of requiring a main.tf, a variables.tf, and an outputs.tf file.

Point is evenly split as both accomplish the same goal.

***Score: Pulumi: 3; Terraform: 2***

## Stacks vs Module Calls

Pulumi implements the concept of a 'Stack', which is an independent instance of a Pulumi Program. You can create any number of stacks from the same Pulumi program, and every stack has their own separate state.

In contrast, using Terraform, you would do a module call by using the "source" meta argument. However, if you're doing multiple module calls from the same root module, the module calls will be part of the same state file.

To have separate state files, you must initialize completely separate Terraform module repos. Or, developers would need to use a GitOps branching strategy and separate deployments Pipelines for each respective branch.

Overall Terraform requires more overhead to achieve whats Stacks achieve natively.

Point goes to Pulumi because Stacks allow you to have clean separation of environments (dev, staging, prod) in an intuitive way.

***Score: Pulumi: 4; Terraform: 2***

## Stack References vs Module Outputs

In Pulumi, due to Stacks being independent from one another, their outputs are not available to other Stacks by default.

To reference an output from another Stack, you would use a Stack reference to access the output of another stack at runtime. To create a stack reference you would use the following syntax: 

`stack_ref = pulumi.StackReference(f"{org}/{project}/{stack}")`

Then refernce a specific output by doing the following: `stack_output = stack_ref.get_output("x")`

In Terraform, module outputs are available to module callers by default.

Giving this point to Terraform as its a simpler process to manage outputs.

***Score: Pulumi: 4; Terraform: 3***

## Automation API

Pulumi's Autmation API allows users to create Pulumi Programs without utilizing the Pulumi CLI.

Developers can also embedd their infrastructure into their application with the inline program functionality. Heres an example of an inline Pulumi program: https://github.com/pulumi/automation-api-examples/blob/main/python/inline_program/main.py

Terraform has a similar feature `terraform-exec` that allows you to run Terraform CLI commands inside of a Go program; but only available to the Go language and no inline functionality.

Point goes to Pulumi for the extended funtionality over Terraform.

***Score: Pulumi: 5; Terraform: 3***

## Secrets Management

Pulumi offers functionality to manage secrets right out of the box.

You can set a secret value by running the following command `pulumi config set --secret mySecret secret-value` where "mySecret" is the key, and "secret-value" will be the encrypted value.

To retrieve the secret in your Pulumi program you would add the following code `config.require_secret("mySecret")`

Pulumi secrets are stored in the state file in the Pulumi Cloud or your backend of choice, and are encrypted at rest and in transit.

Terraform does not offer any functionality to manage secrets natively, it can mark values as `sensitive` but they are stored as plain text in the state. It requires additional tools like "Vault" to securely handle secrets.

Point goes to Pulumi for offering native functionality to handle secrets.

***Final Score: Pulumi: 6; Terraform: 3***