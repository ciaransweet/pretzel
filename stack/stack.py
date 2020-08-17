from aws_cdk import (
    aws_lambda,
    aws_ssm,
    aws_stepfunctions,
    aws_stepfunctions_tasks,
    core,
)


class PretzelStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        hello_world = aws_lambda.Function(
            self,
            "HelloWorld",
            code=aws_lambda.Code.from_asset("./lambdas/hello_world"),
            handler="function.handler.handler",
            timeout=core.Duration.seconds(5),
            runtime=aws_lambda.Runtime.PYTHON_3_8,
        )

        aws_ssm.StringParameter(
            self,
            "HelloWorldLambdaArn",
            string_value=hello_world.function_arn,
            parameter_name=f"/integration_tests/{id}/hello_world_lambda_arn",
        )

        hello_world_task = aws_stepfunctions_tasks.LambdaInvoke(
            self,
            "InvokeHelloWorld",
            lambda_function=hello_world,
            result_path="$.hello_message",
        )

        step_function = aws_stepfunctions.StateMachine(
            self,
            "Hello World Step Function",
            definition=aws_stepfunctions.Chain.start(hello_world_task),
        )

        aws_ssm.StringParameter(
            self,
            "HelloWorldStepFunctionArn",
            string_value=step_function.state_machine_arn,
            parameter_name=f"/integration_tests/{id}/hello_world_step_function_arn",
        )
