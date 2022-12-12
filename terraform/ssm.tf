data "aws_ssm_parameter" "sentry_dsn" {
  name = "${var.app_name}-sentry-dsn-${var.environment}"
}
