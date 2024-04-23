data "aws_ssm_parameter" "secret_key" {
  name = "${var.app_name}-secret-key-${var.environment}"
}

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

# Email
data "aws_ssm_parameter" "email_host" {
  name = "${var.app_name}-email-host-${var.environment}"
}

data "aws_ssm_parameter" "email_host_user" {
  name = "${var.app_name}-email-host-user-${var.environment}"
}

data "aws_ssm_parameter" "email_host_password" {
  name = "${var.app_name}-email-host-password-${var.environment}"
}

# S3
data "aws_ssm_parameter" "aws_access_key_id" {
  name = "${var.app_name}-aws-access-key-id-${var.environment}"
}

data "aws_ssm_parameter" "aws_secret_access_key" {
  name = "${var.app_name}-aws-secret-access-key-${var.environment}"
}

# OneSignal
data "aws_ssm_parameter" "onesignal_api_id" {
  name = "${var.app_name}-onesignal-api-id-${var.environment}"
}

data "aws_ssm_parameter" "onesignal_api_key" {
  name = "${var.app_name}-onesignal-api-key-${var.environment}"
}

data "aws_ssm_parameter" "notify_username" {
  name = "${var.app_name}-notify-username-${var.environment}"
}

data "aws_ssm_parameter" "notify_password" {
  name = "${var.app_name}-notify-password-${var.environment}"
}
