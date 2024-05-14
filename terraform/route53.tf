data "aws_route53_zone" "this" {
  name = var.domain_name
}

## Backend domain setup
resource "aws_route53_record" "cert_validation_records" {
  count   = 3
  zone_id = data.aws_route53_zone.this.id
  name    = tolist(aws_apprunner_custom_domain_association.backend.certificate_validation_records)[count.index].name
  type    = tolist(aws_apprunner_custom_domain_association.backend.certificate_validation_records)[count.index].type
  records = [tolist(aws_apprunner_custom_domain_association.backend.certificate_validation_records)[count.index].value]
  ttl     = var.record_ttl
}

resource "aws_route53_record" "backend_domain" {
  zone_id = data.aws_route53_zone.this.id
  name    = aws_apprunner_custom_domain_association.backend.domain_name
  type    = "CNAME"
  records = [aws_apprunner_service.backend.service_url]
  ttl     = var.record_ttl
}

## Frontend domain setup
resource "aws_route53_record" "vercel_root" {
  zone_id = data.aws_route53_zone.this.zone_id
  name    = local.frontend_domain
  type    = "A"
  ttl     = var.record_ttl
  records = var.vercel_root_records
}

resource "aws_route53_record" "vercel_www" {
  zone_id = data.aws_route53_zone.this.zone_id
  name    = "www"
  type    = "CNAME"
  records = var.vercel_www_records
  ttl     = var.record_ttl
}
