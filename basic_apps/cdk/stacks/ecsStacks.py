from aws_cdk import (
  core,
  aws_ec2 as ec2,
  aws_ecs as ecs,
)

from .constructs import ecs as con

class ECSwAppMesh(core.Stack):
  def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
    super().__init__(scope, id, **kwargs)

    vpc = ec2.Vpc(self, "MyVpc", max_azs=3)
    cluster = ecs.Cluster(self, "MyCluster", vpc=vpc)
    con.ECSTestFargateServicewSDAppMesh(self, "TestService", cluster=cluster, vpc=vpc)


# class ECSwAppMesh(core.Stack):
#   def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
#     super().__init__(scope, id, **kwargs)
#
#     vpc = ec2.Vpc(self, "MyVpc", max_azs=3)
#     cluster = ecs.Cluster(self, "MyCluster", vpc=vpc)
#     con.ECSTestFargateServicewSDAppMesh(self, "TestService", cluster=cluster, vpc=vpc)
#     con.ECSTestFargateServicewSDAppMesh(self, "TestService2", cluster=cluster, vpc=vpc)
#     con.ECSTestFargateServicewSDAppMesh(self, "TestService3", cluster=cluster, vpc=vpc)
