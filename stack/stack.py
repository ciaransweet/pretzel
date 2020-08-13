from aws_cdk import aws_lambda as lambda_functions
from aws_cdk import core


class MosexStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        lambda_functions.Function(
            self,
            "HelloWorld",
            code=lambda_functions.Code.from_asset("./lambdas/hello_world"),
            handler="function.handler.handler",
            timeout=core.Duration.seconds(5),
            runtime=lambda_functions.Runtime.PYTHON_3_8,
        )
