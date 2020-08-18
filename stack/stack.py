from aws_cdk import aws_lambda, aws_ssm, aws_stepfunctions, core


class PretzelStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        process_orders_step_function = aws_stepfunctions.StateMachine(
            self,
            "ProcessOrders",
            definition=aws_stepfunctions.Chain.start(
                aws_stepfunctions.Pass(self, "Pass")
            ),
        )

        aws_ssm.StringParameter(
            self,
            "ProcessOrdersStepFunctionArn",
            string_value=process_orders_step_function.state_machine_arn,
            parameter_name=f"/integration_tests/{id}/process_orders_step_function_arn",
        )

        process_orders = aws_lambda.Function(
            self,
            "ProcessOrdersLambda",
            code=aws_lambda.Code.from_asset("./lambdas/process_orders"),
            handler="function.handler.handler",
            timeout=core.Duration.seconds(5),
            runtime=aws_lambda.Runtime.PYTHON_3_8,
            environment={
                "PROCESS_ORDERS_STEP_FUNCTION_ARN": (
                    process_orders_step_function.state_machine_arn
                )
            },
        )

        aws_ssm.StringParameter(
            self,
            "ProcessOrdersLambdaArn",
            string_value=process_orders.function_arn,
            parameter_name=f"/integration_tests/{id}/process_orders_lambda_arn",
        )

        process_orders_step_function.grant_start_execution(process_orders)
