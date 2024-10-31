module "lambda_function" {
  source         = "terraform-aws-modules/lambda/aws"
  version        = "7.14.0"
  function_name  = "${var.app_name}-onesignal-notifications"
  handler        = "notify.handler"
  runtime        = var.lambda_python_runtime
  create_package = true
  source_path    = "../src/lambdas"
  timeout        = 10
  environment_variables = {
    BACKEND_URL     = "https://${aws_apprunner_service.backend.service_url}"
    NOTIFY_USERNAME = data.aws_ssm_parameter.notify_username.value
    NOTIFY_PASSWORD = data.aws_ssm_parameter.notify_password.value
  }
}

resource "aws_lambda_permission" "allow_cloudwatch" {
  action        = "lambda:InvokeFunction"
  function_name = module.lambda_function.lambda_function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.daily_lambda_trigger.arn
}
