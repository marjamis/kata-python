#!/usr/bin/env python3.6

from aws_cdk import core

from stacks import (
  minimalStacks as minStacks,
  ecsStacks as ecsStacks,
)

app = core.App()

minStacks.WaitCondition(app, "WaitCondition")
minStacks.WaitConditionWithData(app, "WaitConditionWithData")
minStacks.WaitConditionWithInstance(app, "WaitConditionWithInstance")

ecsStacks.ECSwAppMesh(app, "ECSwithAppMesh")

app.synth()
