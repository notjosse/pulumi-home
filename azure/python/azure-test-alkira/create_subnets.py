import pulumi
import pulumi_azure_native as azure_native

class createSubnets:
    def __init__(self) -> None:
        pass

    def create_subnets(self, rg, vnet_data, subnet_prefixes):
        p_subnet = {}
        for i in range(0, len(vnet_data.keys())):
            for j, prefix in enumerate(subnet_prefixes):
                p_name = f"josse-vnet-{i}" + "_" + f"subnet-{j}"
                p_subnet[p_name] = azure_native.network.Subnet(p_name,
                                                    address_prefix=prefix,
                                                    resource_group_name=rg[f"josse-rg-{i}"].name,
                                                    subnet_name=p_name,
                                                    virtual_network_name=vnet_data[f"josse-vnet-{i}"].name,
                                                    # route_table = azure_native.network.RouteTableArgs(id=p_route_table[vnet].id)
                                                    opts=pulumi.ResourceOptions(depends_on=[vnet_data[f"josse-vnet-{i}"]]))
                pulumi.export(p_name, p_subnet[p_name].name)

        return p_subnet