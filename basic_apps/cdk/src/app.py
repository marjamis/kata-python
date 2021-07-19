#!/usr/bin/env python3.6
import os

from aws_cdk import core

from stacks import (
    main as main,
    minimalStacks as minStacks,
)

app = core.App()

minStacks.WaitCondition(app, 'WaitCondition')
minStacks.WaitConditionWithData(app, 'WaitConditionWithData')
minStacks.WaitConditionWithInstance(app, 'WaitConditionWithInstance')

try:
    cdk_account = os.getenv('CDK_ACCOUNT')
    cdk_region = os.getenv('CDK_REGION')
except Exception as e:
    print(f"The required ENVs CDK_ACCOUNT and CDK_REGION likely haven't been set. Error: {e}")


if cdk_account and cdk_region:
    main.MainInstance(
        app,
        'MainInstance',
        env=core.Environment(
            account=cdk_account,
            region=cdk_region,
        ),
    )

app.synth()
