"""An Azure RM Python Pulumi program"""

import pulumi
import pulumi_azure_native as azure_native
from create_rg import createRG
from create_vnet import createVnet
from create_subnets import createSubnets
# from create_route_table import createRouteTable
# from create_route_table_route import createRouteTableRoute
# #from create_subnet_route_table_association import createSubnetRouteTableAssociation
# from create_network_security_group import createNetworkSecurityGroup
# from create_network_security_group_rule import createNetworkSecurityGroupRule
# from create_vnet_gateway import createVnetGateway
# from create_vm_instance import createVmInstance

from deployments import deployment_settings_resource

if __name__ == "__main__":
    config = pulumi.Config()

    if config.require_object("deploy_resources"):
        
        # Number of resources
        num_resources = 50

        #create rg
        rg = createRG()
        rg_out = rg.create_rg(num_resources)

        #create vnet
        create_vnet = createVnet()
        create_vnet_out = create_vnet.create_vnet(rg_out, num_resources)

        # #create route table - one route table per vnet
        # create_route_table = createRouteTable()
        # create_route_table_out = create_route_table.create_route_table(tags, rg_out, vnet_data)

        # #create route table rules
        # create_route_table_route = createRouteTableRoute()
        # create_route_table_route_out = create_route_table_route.create_route_table_route(rg_out, vnet_data, create_route_table_out, whitelist, "Internet")

        # #create subnets
        create_subnets = createSubnets()
        subnet_prefixes = ["10.0.4.0/23", "10.0.6.0/23"]
        create_subnets_out = create_subnets.create_subnets(rg_out, create_vnet_out, subnet_prefixes)

        # #create network security group
        # create_network_security_group = createNetworkSecurityGroup()
        # create_network_security_group_out = create_network_security_group.create_network_secuirty_group(rg_out, vnet_data)

        # #create an outbout allow all rule
        # #you can only call the outbound and inbound security group rules once, construct a full list if you need to call the function again
        # create_network_security_group_rule = createNetworkSecurityGroupRule()
        # create_network_security_group_rule_out = create_network_security_group_rule.create_network_security_group_rule(rg_out, create_network_security_group_out, vnet_data, ["0.0.0.0/0"], "Outbound")
        # full_white_list = whitelist + rfc_1918
        # create_network_security_group_inbound_office_rule_out = create_network_security_group_rule.create_network_security_group_rule(rg_out, create_network_security_group_out, vnet_data, full_white_list, "Inbound")

        # #create vnet gateway if required
        # create_vnet_gateway = createVnetGateway()
        # create_vnet_gateway_out = create_vnet_gateway.create_vnet_gateway(rg_out,create_vnet_out, vnet_data, tags)

        # #create vm
        # create_vm_instance = createVmInstance()
        # create_vm_instance_out = create_vm_instance.create_vm_instance(vnet_data, rg_out, create_subnets_out, create_network_security_group_out, tags)
    else:
        print("Nothing to deploy or deleting existing resources")