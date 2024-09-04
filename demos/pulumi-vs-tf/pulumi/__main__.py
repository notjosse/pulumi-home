"""An AWS Python Pulumi program"""

import pulumi
import ec2_instance

config = pulumi.Config()
main_config = pulumi.Config("main")
users = main_config.get_object('users')

name = 'josse'
instances = {}

for num in range(0,len(users)):
    # Create predefined ec2 instances and required resources
    my_instance = ec2_instance.EC2Instance(name=f"ec2-instance-{users[num]}", suffix=f"{users[num]}", num=num)
    instances[f"{users[num]}"] = my_instance

# Export Outputs
for inst in instances:
    pulumi.export(inst, instances[inst])

pulumi.export("mySecret", config.require_secret("mySecret"))