data "aws_route53_zone" "this" {
  name = var.domain_name
}

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
