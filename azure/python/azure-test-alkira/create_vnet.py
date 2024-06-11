import pulumi
import pulumi_azure_native as azure_native

class createVnet:
    def __init__(self) -> None:
        pass

    def create_vnet(self, rg_name, num_vnets):
        p_vnet_map = {}
        for i in range(0, num_vnets):
            p_vnet_map[f"josse-vnet-{i}"] = azure_native.network.VirtualNetwork(f"josse-vnet-{i}",
                                                                  address_space=azure_native.network.AddressSpaceArgs(address_prefixes=[f"10.0.0.0/21"],),
                                                                #   location=vnet_data[vnet]["location"],
                                                                  resource_group_name=rg_name[f"josse-rg-{i}"].name,
                                                                  virtual_network_name=f"josse-vnet-{i}"
                                                                #   tags = tags
                                                                  )
            pulumi.export(f'vnet-{i}', p_vnet_map[f"josse-vnet-{i}"].name)

        return p_vnet_map