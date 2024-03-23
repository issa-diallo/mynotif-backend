terraform {
  required_version = ">= 0.12.2"

  backend "s3" {
    region         = "eu-west-3"
    bucket         = "mynotif-backend-terraform-state"
    key            = "terraform.tfstate"
    dynamodb_table = "mynotif-backend-terraform-state-lock"
    profile        = ""
    encrypt        = "true"
  }
}
