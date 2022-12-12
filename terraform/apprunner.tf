resource "aws_apprunner_auto_scaling_configuration_version" "backend" {
  provider                        = aws.app_runner
  auto_scaling_configuration_name = "${var.app_name}-${var.environment}"
  min_size                        = 1
  max_size                        = 1
}

resource "aws_apprunner_service" "backend" {
  auto_scaling_configuration_arn = aws_apprunner_auto_scaling_configuration_version.backend.arn
  service_name                   = "${var.app_name}-runner-${var.environment}"
  provider                       = aws.app_runner
  source_configuration {
    auto_deployments_enabled = false
    authentication_configuration {
      access_role_arn = aws_iam_role.apprunner_ecr_role.arn
    }
    image_repository {
      image_configuration {
        port = "8000"
        runtime_environment_variables = {
          ALLOWED_HOSTS        = jsonencode(var.env_allowed_hosts)
          CORS_ALLOWED_ORIGINS = jsonencode(var.env_cors_allowed_origins)
          PRODUCTION           = var.env_production
          SENTRY_DSN           = data.aws_ssm_parameter.sentry_dsn.value
        }
      }
      image_repository_type = "ECR"
      image_identifier      = "${aws_ecr_repository.this.repository_url}:latest"
    }
  }
}
