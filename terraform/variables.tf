variable "aws_region" {
  type        = string
  description = "AWS Region"
  default     = "eu-west-3"
}

variable "app_runner_region" {
  type        = string
  description = "App Runner Region"
  # App Runner isn't currently available in `eu-west-3`
  default = "eu-central-1"
}

variable "app_name" {
  type        = string
  description = "Application Name"
  default     = "mynotif-backend"
}

variable "role_arn" {
  type        = string
  description = "Deployment role ARN"
  default     = "arn:aws:iam::332944743618:role/mynotif-infra-deployment-automation-role"
}

variable "environment" {
  type        = string
  description = "Environment (acceptance, staging, production)"
  default     = "production"
}

# Environment variables definition
variable "env_allowed_hosts" {
  type        = list(string)
  description = "https://docs.djangoproject.com/en/4.2/ref/settings/#allowed-hosts"
  default = [
    "127.0.0.1",
    "localhost",
    ".eu-central-1.awsapprunner.com",
  ]
}

variable "env_csrf_trusted_origins" {
  type        = list(string)
  description = "https://docs.djangoproject.com/en/4.2/ref/settings/#csrf-trusted-origins"
  default = [
    "http://127.0.0.1",
    "http://localhost",
    "https://*.eu-central-1.awsapprunner.com",
  ]
}

# Database
variable "env_database_engine" {
  type        = string
  description = "https://docs.djangoproject.com/en/3.2/ref/settings/#engine"
  default     = "django.db.backends.postgresql"
}

variable "env_database_port" {
  type        = number
  description = "https://docs.djangoproject.com/en/3.2/ref/settings/#port"
  default     = 5432
}

variable "env_email_use_ssl" {
  type        = string
  description = "https://docs.djangoproject.com/en/4.2/ref/settings/#email-use-ssl"
  default     = "true"
}

variable "env_email_port" {
  type        = number
  description = "https://docs.djangoproject.com/en/4.2/ref/settings/#email-use-ssl"
  default     = 465
}

variable "env_time_zone" {
  type        = string
  description = "https://docs.djangoproject.com/en/3.2/ref/settings/#std-setting-TIME_ZONE"
  default     = "Europe/Paris"
}

variable "env_cors_allowed_origins" {
  type        = list(string)
  description = "https://github.com/adamchainz/django-cors-headers"
  default = [
    "http://localhost:3000",
    "http://localhost:8000",
    "https://mynotif.herokuapp.com",
    "https://mynotif.vercel.app",
    "https://mynotif.netlify.app",
  ]
}

variable "env_cors_allowed_origin_regexes" {
  type        = list(string)
  description = "https://github.com/adamchainz/django-cors-headers"
  default = [
    "^https://mynotif-git-[\\w-]+-issa-diallo\\.vercel\\.app$",
    "^https://deploy-preview-\\d+--mynotif\\.netlify\\.app$",
  ]
}

variable "env_production" {
  type        = string
  description = "Set to 1 or true for production, 0 or false otherwise"
  default     = "true"
}

variable "env_password_reset_confirm_url" {
  type    = string
  default = "reset/password/{uid}/{token}"
}

variable "env_templated_mail_domain" {
  type    = string
  default = "mynotif.netlify.app"
}

variable "env_templated_site_name" {
  type    = string
  default = "MyNotif"
}

locals {
  image_name = "${var.app_name}-${var.environment}"
}
