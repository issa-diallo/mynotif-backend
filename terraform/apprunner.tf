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
  instance_configuration {
    cpu    = "0.25 vCPU"
    memory = "0.5 GB"
  }
  source_configuration {
    auto_deployments_enabled = false
    authentication_configuration {
      access_role_arn = aws_iam_role.apprunner_ecr_role.arn
    }
    image_repository {
      image_configuration {
        port = "8000"
        runtime_environment_variables = {
          SECRET_KEY                  = data.aws_ssm_parameter.secret_key.value
          TIME_ZONE                   = var.env_time_zone
          ALLOWED_HOSTS               = jsonencode(var.env_allowed_hosts)
          CSRF_TRUSTED_ORIGINS        = jsonencode(var.env_csrf_trusted_origins)
          CORS_ALLOWED_ORIGINS        = jsonencode(var.env_cors_allowed_origins)
          CORS_ALLOWED_ORIGIN_REGEXES = jsonencode(var.env_cors_allowed_origin_regexes)
          PRODUCTION                  = var.env_production
          SENTRY_DSN                  = data.aws_ssm_parameter.sentry_dsn.value
          # Database
          DATABASE_ENGINE   = var.env_database_engine
          DATABASE_NAME     = data.aws_ssm_parameter.database_name.value
          DATABASE_USER     = data.aws_ssm_parameter.database_user.value
          DATABASE_PASSWORD = data.aws_ssm_parameter.database_password.value
          DATABASE_HOST     = data.aws_ssm_parameter.database_host.value
          DATABASE_PORT     = var.env_database_port
          # Email
          EMAIL_USE_SSL       = var.env_email_use_ssl
          EMAIL_HOST          = data.aws_ssm_parameter.email_host.value
          EMAIL_PORT          = var.env_email_port
          EMAIL_HOST_USER     = data.aws_ssm_parameter.email_host_user.value
          EMAIL_HOST_PASSWORD = data.aws_ssm_parameter.email_host_password.value
          # S3
          AWS_ACCESS_KEY_ID     = data.aws_ssm_parameter.aws_access_key_id.value
          AWS_SECRET_ACCESS_KEY = data.aws_ssm_parameter.aws_secret_access_key.value
          # Djoser
          PASSWORD_RESET_CONFIRM_URL = var.env_password_reset_confirm_url
          TEMPLATED_MAIL_DOMAIN      = local.env_templated_mail_domain
          TEMPLATED_SITE_NAME        = var.env_templated_site_name
          # OneSignal
          ONESIGNAL_APP_ID  = data.aws_ssm_parameter.onesignal_api_id.value
          ONESIGNAL_API_KEY = data.aws_ssm_parameter.onesignal_api_key.value
        }
      }
      image_repository_type = "ECR"
      image_identifier      = "${aws_ecr_repository.this.repository_url}:latest"
    }
  }
}

resource "aws_apprunner_custom_domain_association" "backend" {
  provider    = aws.app_runner
  domain_name = local.backend_subdomain
  service_arn = aws_apprunner_service.backend.arn
}
