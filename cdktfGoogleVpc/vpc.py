#!/usr/bin/env python
from constructs import Construct
from cdktf import App, TerraformStack, TerraformOutput

# Import the Providers

#from cdktf_cdktf_provider_google.provider import GoogleProvider

# Import the Network 
from  cdktf_cdktf_provider_google.compute_network  import ComputeNetwork
from  cdktf_cdktf_provider_google.compute_subnetwork  import ComputeSubnetwork

class Vpc(Construct):
    def __init__(self, scope: Construct, id: str, project_id: str, vpc_name: str, region: str, vpc_routing_mode: str, subnets_config: list[dict]):
        super().__init__(scope, id)

        # Validate the inputsputs here
        if not project_id:
            raise ValueError("project_id must be provided for GcpVpcModule.")
        if not region:
            raise ValueError("region must be provided for GcpVpcModule.")
        if not vpc_name:
            raise ValueError("vpc_name must be provided for GcpVpcModule.")
        if not vpc_routing_mode:
            raise ValueError("vpc_routing_mode must be provided for Vpc module.")
        if not subnets_config:
            raise ValueError("subnets_config must be provided and not empty for GcpVpcModule.")

        self.vpc_network = ComputeNetwork(self, "google-vpc", project=project_id, name=vpc_name, auto_create_subnetworks=False, routing_mode=vpc_routing_mode)
        self.vpc_network.override_logical_id(vpc_name)
        self.subnets = []

        for i, subnets_conf in enumerate (subnets_config):
            if not all(k in subnets_conf for k in ["name", "ip_cidr_range"]):
                 raise ValueError(f"Subnet configuration at index {i} is missing 'name' or 'ip_cidr_range'.")
            
            subnet = ComputeSubnetwork(
                self, 
                f"subnetwork_{subnets_conf['name'].replace('-','_')}_{i}",
                name = subnets_conf["name"],
                ip_cidr_range=subnets_conf["ip_cidr_range"],
                network = self.vpc_network.id,
                project = project_id,
                region = region
                )
            subnet.override_logical_id(subnets_conf["name"])
            self.subnets.append(subnet)

        # --- Define Dynamic Outputs ---
        # Outputs should be based on the dynamic resources
        TerraformOutput(self, "vpc_network_name", value=self.vpc_network.name)
        TerraformOutput(self, "vpc_network_self_link", value=self.vpc_network.self_link)
        TerraformOutput(self, "vpc_network_id", value=self.vpc_network.id)
        TerraformOutput(self, "vpc_network_project", value=self.vpc_network.project)
        TerraformOutput(self, "vpc_network_region", value=region) # Directly from input

        # Output details for each created subnet
        for i, subnet in enumerate(self.subnets):
            subnet_name = subnets_config[i]["name"].replace("-", "_")

            TerraformOutput(self, f"subnet_{subnet_name}_name", value=subnet.name)
            TerraformOutput(self, f"subnet_{subnet_name}_ip_cidr_range", value=subnet.ip_cidr_range)
            TerraformOutput(self, f"subnet_{subnet_name}_self_link", value=subnet.self_link)
            TerraformOutput(self, f"subnet_{subnet_name}_id", value=subnet.id)
            TerraformOutput(self, f"subnet_{subnet_name}_region", value=subnet.region)
