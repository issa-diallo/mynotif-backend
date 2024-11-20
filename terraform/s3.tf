resource "aws_s3_bucket" "prescription" {
  bucket = "mynotif-prescription"
  tags = {
    Name = "Prescription files"
  }
}
