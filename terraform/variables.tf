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
  default     = "arn:aws:iam::332944743618:role/mynotif-deployment-automation-role"
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

variable "env_cors_allowed_origins" {
  type        = list(string)
  description = "https://github.com/adamchainz/django-cors-headers"
  default = [
    "http://localhost:3000",
    "http://localhost:8000",
    "https://mynotif.herokuapp.com",
    "https://mynotif.vercel.app",
  ]
}

variable "env_production" {
  type        = number
  description = "Set to 1 for production, 0 otherwise"
  default     = 1
}

locals {
  image_name = "${var.app_name}-${var.environment}"
}
