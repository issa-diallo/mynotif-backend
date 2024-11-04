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

# Zoho domain verification
resource "aws_route53_record" "zoho_verification" {
  zone_id = data.aws_route53_zone.this.zone_id
  name    = var.domain_name
  type    = "TXT"
  ttl     = 300
  records = [
    "zoho-verification=zb76736764.zmverify.zoho.eu",
    # Sender Policy Framework (SPF)
    # https://mailadmin.zoho.eu/cpanel/home.do#domains/ordopro.fr/emailConfig/spf
    "v=spf1 include:zohomail.eu ~all",
  ]
}

# Zoho Mail Exchanger (MX) Records
# https://mailadmin.zoho.eu/cpanel/home.do#domains/ordopro.fr/emailConfig/mx
resource "aws_route53_record" "zoho_mx" {
  zone_id = data.aws_route53_zone.this.zone_id
  name    = var.domain_name
  type    = "MX"
  ttl     = 300
  records = [
    "10 mx.zoho.eu",
    "20 mx2.zoho.eu",
    "50 mx3.zoho.eu",
  ]
}

# Zoho DomainKeys Identified Mail (DKIM)
# https://mailadmin.zoho.eu/cpanel/home.do#domains/ordopro.fr/emailConfig/dkim/dkim-listing
resource "aws_route53_record" "zoho_dkim" {
  zone_id = data.aws_route53_zone.this.zone_id
  name    = "zmail._domainkey"
  type    = "TXT"
  ttl     = 300
  records = ["v=DKIM1; k=rsa; p=MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDJo3TedcEMBPG+7Xv0e4IlC458NGI4EygyAAjVJCNhkgOvkLdcuDzdHU+zg5NGrIFwg8hZUbW4JMuqqufCcXFEcBmALMDBRIb3QRXeo2FUz7ormQFMu6WqdfThdQcF1N7O5+RQhkPPfELabNvcCeMq/eKdyNLL2iNtUvM99fGj3wIDAQAB"]
}
