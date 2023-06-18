data "aws_ssm_parameter" "sentry_dsn" {
  name = "${var.app_name}-sentry-dsn-${var.environment}"
}

# Database
data "aws_ssm_parameter" "database_name" {
  name = "${var.app_name}-database-name-${var.environment}"
}

data "aws_ssm_parameter" "database_user" {
  name = "${var.app_name}-database-user-${var.environment}"
}

data "aws_ssm_parameter" "database_password" {
  name = "${var.app_name}-database-password-${var.environment}"
}

data "aws_ssm_parameter" "database_host" {
  name = "${var.app_name}-database-host-${var.environment}"
}
