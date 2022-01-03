from aws_cdk import (
  core,
  aws_cloudformation as cfn,
  aws_ec2 as ec2,
)

from .constructs import cfn as con


class WaitCondition(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        cfn.CfnWaitCondition(self, "testWaitCondition")


class WaitConditionWithData(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(
            scope, id,
            **kwargs,
            description="A test on sending data to a WaitCondition. Once created to use: Send data output: cfn-signal -d <data> <wait_handle>"
        )

        c = con.WaitConditionWithDataConstruct(self, "Blah", count=1, timeout="300")

        core.CfnOutput(
            self,
            "Outputs",
            value=c.getWaitCondition().get_att("Data").to_string(),
            description="Data for Cloudformation Handle using cfn-signal with data that is outputted into the Outputs"
        )


class WaitConditionWithInstance(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(
            scope, id,
            **kwargs,
            description="A test on sending data to a WaitCondition. Once created to use: Send data output: cfn-signal -d <data> <wait_handle>"
        )

        c = con.WaitConditionWithDataConstruct(self, "Blah", count=2, timeout="300")

        instance = ec2.CfnInstance(
            self,
            "MainInstance",
            image_id="ami-f173cc91",
            key_name="testing",
            instance_type="t2.micro",
            subnet_id=core.CfnParameter(self, "SubnetId", type="AWS::EC2::Subnet::Id").to_string(),
            user_data=core.Fn.base64(
                core.Fn.sub(
                    '''#!/bin/bash
                    /opt/aws/bin/cfn-init -s ${{AWS::StackName}} -r MyEC2Instance  --region ${{AWS::Region}}
                    /opt/aws/bin/cfn-signal -d "tempdata" {handle}'''.format(handle=c.getWaitHandle().logical_id)
                )
            )
        )

        core.CfnOutput(
            self,
            "Outputs",
            value=c.getWaitCondition().get_att("Data").to_string(),
            description="Data for Cloudformation Handle using cfn-signal with data that is outputted into the Outputs"
        )

        c.getWaitCondition().add_depends_on(instance)
