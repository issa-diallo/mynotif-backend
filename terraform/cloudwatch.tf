resource "aws_cloudwatch_event_rule" "daily_lambda_trigger" {
  name = "${var.app_name}-daily"
  # daily at 8AM UTC
  schedule_expression = "cron(0 8 * * ? *)"
}

resource "aws_cloudwatch_event_target" "trigger_lambda" {
  rule = aws_cloudwatch_event_rule.daily_lambda_trigger.name
  arn  = module.lambda_function.lambda_function_arn
}
