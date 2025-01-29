variable "aws_region" {
  type        = string
  description = "AWS Region"
  default     = "eu-west-3"
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

## Domain setup
variable "domain_name" {
  type        = string
  description = "Application domain"
  default     = "ordopro.fr"
}

variable "github_pages_cname_records" {
  type        = list(string)
  description = "GitHub Pages frontend landing domain mapping."
  default     = ["mynotif.github.io"]
}

variable "github_pages_a_records" {
  description = "GitHub Pages A records for IPv4."
  type        = list(string)
  default = [
    "185.199.108.153",
    "185.199.109.153",
    "185.199.110.153",
    "185.199.111.153"
  ]
}

variable "github_pages_aaaa_records" {
  description = "GitHub Pages AAAA records for IPv6."
  type        = list(string)
  default = [
    "2606:50c0:8000::153",
    "2606:50c0:8001::153",
    "2606:50c0:8002::153",
    "2606:50c0:8003::153"
  ]
}

variable "vercel_cname_records" {
  type        = list(string)
  description = "Vercel frontend app domain mapping."
  default     = ["cname.vercel-dns.com."]
}

variable "record_ttl" {
  type        = number
  description = "The TTL of the record"
  default     = 300
}

## App Runner environment variables definition
variable "env_allowed_hosts" {
  type        = list(string)
  description = "https://docs.djangoproject.com/en/4.2/ref/settings/#allowed-hosts"
  default = [
    "127.0.0.1",
    "localhost",
    ".eu-west-3.awsapprunner.com",
    "api.ordopro.fr",
  ]
}

variable "env_csrf_trusted_origins" {
  type        = list(string)
  description = "https://docs.djangoproject.com/en/4.2/ref/settings/#csrf-trusted-origins"
  default = [
    "http://127.0.0.1",
    "http://localhost",
    "https://*.eu-west-3.awsapprunner.com",
    "https://api.ordopro.fr",
  ]
}

## App Runner database
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
    "https://ordopro.fr",
    "https://www.ordopro.fr",
    "https://app.ordopro.fr",
  ]
}

variable "env_cors_allowed_origin_regexes" {
  type        = list(string)
  description = "https://github.com/adamchainz/django-cors-headers"
  default = [
    "^https://mynotif-git-[\\w-]+-issa-diallo\\.vercel\\.app$",
    "^https://mynotif-frontend-git-[\\w-]+-miras\\.vercel\\.app$",
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

variable "env_templated_site_name" {
  type    = string
  default = "MyNotif"
}

# Frontend URL
variable "frontend_url" {
  type        = string
  description = "Frontend URL for Stripe redirects"
  default     = "https://app.ordopro.fr"
}

## Lambda configuration
variable "lambda_python_runtime" {
  description = "AWS Lambda Python runtime version"
  type        = string
  default     = "python3.12"
}

locals {
  image_name             = "${var.app_name}-${var.environment}"
  backend_subdomain      = "api.${var.domain_name}"
  frontend_domain_prefix = "app"
  ## dynamic environment variables
  env_templated_mail_domain = var.domain_name
}
