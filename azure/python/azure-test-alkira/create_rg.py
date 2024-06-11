import pulumi
import pulumi_azure_native as azure_native

class createRG:
    def __init__(self) -> None:
        pass

    def create_rg(self, num_rg):
        rg_map = {}
        for i in range(0, num_rg):
            rg_map[f"josse-rg-{i}"] = azure_native.resources.ResourceGroup(f"josse-rg-{i}")
            pulumi.export(f'rg-{i}', rg_map[f"josse-rg-{i}"].name)

        return rg_map