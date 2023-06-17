terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~>4.18"
    }
  }

  required_version = ">=0.14.9"
}

provider "aws" {
  region = var.aws_region
  # Role to assume for AWS operations
  assume_role {
    role_arn = var.role_arn
  }
}

provider "aws" {
  alias  = "app_runner"
  region = var.app_runner_region
  # Role to assume for AWS operations
  assume_role {
    role_arn = var.role_arn
  }
}

# You cannot create a new backend by simply defining this and then
# immediately proceeding to "terraform apply". The S3 backend must
# be bootstrapped according to the simple yet essential procedure in
# https://github.com/cloudposse/terraform-aws-tfstate-backend#usage
module "terraform_state_backend" {
  source = "cloudposse/tfstate-backend/aws"
  # Cloud Posse recommends pinning every module to a specific version
  version    = "0.38.1"
  namespace  = var.app_name
  name       = "terraform"
  attributes = ["state"]

  terraform_backend_config_file_path = "."
  terraform_backend_config_file_name = "backend.tf"
  force_destroy                      = false
}
