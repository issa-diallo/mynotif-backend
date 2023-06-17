data "aws_iam_policy_document" "apprunner_ecr_policy" {
  statement {
    actions = [
      "ecr:BatchCheckLayerAvailability",
      "ecr:BatchGetImage",
      "ecr:DescribeImages",
      "ecr:GetAuthorizationToken",
      "ecr:GetDownloadUrlForLayer",
    ]
    resources = ["*"]
  }
}

resource "aws_iam_policy" "apprunner_ecr_policy" {
  name        = "${var.app_name}-ecr-policy-${var.environment}"
  path        = "/"
  description = "Allow AppRunner to access ECR"
  policy      = data.aws_iam_policy_document.apprunner_ecr_policy.json
}

resource "aws_iam_role" "apprunner_ecr_role" {
  name = "${var.app_name}-ecr-role-${var.environment}"
  assume_role_policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement" : [
      {
        "Action" : "sts:AssumeRole",
        "Principal" : {
          "Service" : [
            "build.apprunner.amazonaws.com",
          ]
        },
        "Effect" : "Allow",
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "aws_iam_role_policy_attachment" {
  role       = aws_iam_role.apprunner_ecr_role.name
  policy_arn = aws_iam_policy.apprunner_ecr_policy.arn
}
