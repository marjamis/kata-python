from aws_cdk import (
  core,
  aws_ec2 as ec2,
  aws_ecs as ecs,
  aws_servicediscovery as sd,
  aws_appmesh as am,
  aws_iam as iam,
)

class ECSTestFargateServicewSDAppMesh(core.Construct):
  def __init__(self, scope: core.Construct, id: str, cluster: ecs.Cluster, vpc: ec2.Vpc, **kwargs):
    super().__init__(scope, id, **kwargs)

    namespace = sd.PrivateDnsNamespace(self, "TestServiceNS", name="testing.local", vpc=vpc)

    mesh = am.Mesh(self, "SerivceMesh", mesh_name="cdkTestMesh")
    vn = mesh.add_virtual_node("virtual_node",
      dns_host_name="t1.testing.local",
      listener=am.VirtualNodeListener(
        port_mapping=am.PortMapping(
          port=80,
          protocol=am.Protocol.TCP,
        ),
      ),
    )
    mesh.add_virtual_service("virtual_service", virtual_node=vn, virtual_service_name="testing.local")

    ECSTestFargateService(self, "TestService", cluster=cluster, virtualNode=vn, subnets=vpc.public_subnets, sdns=namespace)

# TODO make the most of the below and consistent but optional, add in AAS. ALB(simple to add others)
class ECSTestFargateService(core.Construct):
  def __init__(self, scope: core.Construct, id: str, cluster: ecs.Cluster, virtualNode: am.VirtualNode, subnets: ec2.ISubnet, sdns: sd.INamespace, **kwargs):
    super().__init__(scope, id, **kwargs)

    proxy_container_name="envoy"

    td = ecs.TaskDefinition(self, "TaskDefinition",
      compatibility=ecs.Compatibility.EC2_AND_FARGATE,
      cpu=".25 vCPU",
      memory_mib="512",
      execution_role=iam.Role.from_role_arn(self, "TaskExecutionRole", "arn:aws:iam::109951093165:role/ecsTaskExecutionRole"),
      task_role=iam.Role.from_role_arn(self, "TaskRole", "arn:aws:iam::109951093165:role/ecs_TaskRole"),
      network_mode=ecs.NetworkMode.AWS_VPC,
      proxy_configuration=ecs.AppMeshProxyConfiguration(
        container_name=proxy_container_name,
        properties=ecs.AppMeshProxyConfigurationProps(
          proxy_ingress_port=15000,
          app_ports=[80],
          egress_ignored_i_ps=["169.254.170.2", "169.254.169.254"],
          ignored_gid=None,
          egress_ignored_ports=[],
          ignored_uid=1337,
          proxy_egress_port=15001,
        ),
      ),
    )

    envoy = td.add_container(proxy_container_name,
      image=ecs.RepositoryImage(
        image_name="840364872350.dkr.ecr.us-west-2.amazonaws.com/aws-appmesh-envoy:v1.12.1.0-prod",
      ),
      memory_limit_mib=256,
      environment={
        "APPMESH_VIRTUAL_NODE_NAME": "mesh/{mesh}/virtualNode/{virtualNode}".format(mesh=virtualNode.mesh.mesh_name, virtualNode=virtualNode.virtual_node_name)
      },
      user= "1337",
      health_check=ecs.HealthCheck(
        command=["CMD-SHELL", "curl -s http://localhost:9901/server_info | grep state | grep -q LIVE"],
        interval=core.Duration.seconds(5),
        retries=3,
        start_period=core.Duration.seconds(10),
        timeout=core.Duration.seconds(2),
      ),
    )

    appc = td.add_container("accessContainer",
      image=ecs.RepositoryImage(image_name="109951093165.dkr.ecr.us-west-2.amazonaws.com/test:debugger"),
      memory_limit_mib=256,
    )
    appc.add_container_dependencies(ecs.ContainerDependency(container=envoy, condition=ecs.ContainerDependencyCondition.HEALTHY))
    appc.add_port_mappings(
        ecs.PortMapping(
          container_port=80,
          host_port=80,
          protocol=ecs.Protocol.TCP,
      ),
      (
        ecs.PortMapping(
          container_port=8022,
          host_port=8022,
          protocol=ecs.Protocol.TCP,
        )
      ),
    )
    # TODO add SGs and rules with 80 and 8022 for access
    ecs.FargateService(self, "Service",
      task_definition=td,
      assign_public_ip=True,
      vpc_subnets=ec2.SubnetSelection(
        subnets=subnets,
      ),
      cluster=cluster,
      cloud_map_options=ecs.CloudMapOptions(
        cloud_map_namespace=sdns,
        dns_record_type=sd.DnsRecordType.A,
        dns_ttl=core.Duration.seconds(30),
        failure_threshold=1,
        name="t1"
      ),
      desired_count=1,
    )
