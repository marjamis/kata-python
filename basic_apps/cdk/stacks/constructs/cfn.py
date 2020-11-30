from aws_cdk import (
  aws_cloudformation as cfn,
  aws_ec2 as ec2,
  core
)

class WaitConditionWithDataConstruct(core.Construct):
  def getWaitHandle(self):
    return self._h

  def getWaitCondition(self):
    return self._w

  def __init__(self, scope: core.Construct, id: str, count: int, timeout: str, **kwargs):
    super().__init__(scope, id, **kwargs)

    eip = ec2.CfnEIP(self, "NAT_EIP", domain="vpc")
    self._h = cfn.CfnWaitConditionHandle(self, "testWaitConditionWithDataHandle")
    self._w = cfn.CfnWaitCondition(self, "testWaitConditionWithData", count=count, handle=self._h.ref, timeout=timeout)
    self._w.add_depends_on(eip)
