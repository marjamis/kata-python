from diagrams import Cluster, Diagram, Edge, Node
from diagrams.aws.compute import EC2, ECS
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB
from diagrams.custom import Custom
from diagrams.onprem.network import Internet


def create_ecs_cluster(start, end):
    cluster = ECS("Primary Cluster")
    workers = [EC2(f"worker#{i}") for i in range(start, end)]
    cluster >> Edge(
        color="pink",
        style="dashed",
        label="Container Instance") >> workers

    return cluster


with Diagram("Cluster Integration", show=False, direction="TB", outformat="png", filename="/output/grouped_workers"):

    with Cluster("Other AWS Resources"):
        primary_load_balancer = ELB("Load Balancer")
        events_database = RDS("Events Databse")

    with Cluster("Primary ECS Cluster"):
        primary_cluster = create_ecs_cluster(start=0, end=7)

    with Cluster("Backup Clusters"):
        with Cluster("First Backup ECS Cluster"):
            backup_cluster1 = create_ecs_cluster(start=10, end=12)

        with Cluster("Second Backup ECS Cluster"):
            backup_cluster2 = create_ecs_cluster(start=20, end=21)

    primary_cluster >> events_database
    backup_cluster1 >> events_database
    backup_cluster2 >> events_database
    primary_load_balancer >> primary_cluster
    primary_load_balancer >> Edge(style="dashed", label="Cut over in an emergency") >> [backup_cluster1, backup_cluster2]

    Internet() >> primary_load_balancer
