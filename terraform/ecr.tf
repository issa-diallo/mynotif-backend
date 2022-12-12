resource "aws_ecr_repository" "this" {
  name         = local.image_name
  force_delete = true
  tags = {
    Name        = var.app_name
    Environment = var.environment
  }
}
