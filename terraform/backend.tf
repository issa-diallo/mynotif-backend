terraform {
  required_version = ">= 1.0.0"

  backend "s3" {
    region  = "eu-west-3"
    bucket  = "mynotif-backend-terraform-state"
    key     = "terraform.tfstate"
    profile = ""
    encrypt = "true"

    dynamodb_table = "mynotif-backend-terraform-state-lock"
  }
}
