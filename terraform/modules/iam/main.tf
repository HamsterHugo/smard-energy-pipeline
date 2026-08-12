resource "aws_iam_role" "lambda_role" {
  name = var.role_name
  tags = var.tags

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action    = "sts:AssumeRole"
        Effect    = "Allow"
        Principal = { Service : "lambda.amazonaws.com" }
      }
    ]
  })
}

resource "aws_iam_role_policy" "lambda_policy" {
  name = "${var.role_name}-policy"
  role = aws_iam_role.lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:DeleteObject",
          "s3:ListBucket"
        ]
        Resource = [
          var.bucket_arn,
          "${var.bucket_arn}/*"
        ]
      },
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "arn:aws:logs:*:*:*"
      },
      {
        Effect   = "Allow"
        Action   = "sts:GetCallerIdentity"
        Resource = "*"
      }
    ]
  })
}

#resource "aws_iam_role" "lambda_role" {
#  name = var.lambda_role_name
#
#  assume_role_policy = jsonencode({
#    Version : "2012-10-17"
#    Statement : [
#      {
#        Action = "sts:AssumeRole"
#        Effect = "Allow"
#        Principal = {
#          Service = "lambda.amazonaws.com"
#        }
#      }
#    ]
#  })
#}
#
#resource "aws_iam_policy" "s3_policy" {
#  name        = "${var.lambda_role_name}-s3-policy"
#  description = "Policy for the S3 bucket ${var.s3_bucket_name}"
#
#  policy = jsonencode({
#    Version = "2012-10-17"
#    Statement = [
#      {
#        Effect = "Allow"
#        Action = [
#          "s3:GetObject",
#          "s3:PutObject",
#          "s3:DeleteObject",
#          "s3:ListBucket"
#        ]
#        Resource = [
#          "arn:aws:s3:::${var.s3_bucket_name}",
#          "arn:aws:s3:::${var.s3_bucket_name}/*"
#        ]
#      }
#    ]
#  })
#}

#resource "aws_iam_policy" "logs_policy" {
#  name        = "${var.lambda_role_name}-logs-policy"
#  description = "Policy for CloudWatch Logs."
#
#  policy = jsonencode({
#    Version = "2012-10-17"
#    Statement = [
#      {
#        Effect = "Allow"
#        Action = [
#          "logs:CreateLogGroup",
#          "logs:CreateLogStream",
#          "logs:PutLogEvents"
#        ]
#        Resource = "arn:aws:logs:*:*:*"
#      }
#    ]
#  })
#}

#resource "aws_iam_role_policy_attachment" "s3_attachment" {
#  role       = aws_iam_role.lambda_role.name
#  policy_arn = aws_iam_policy.s3_policy.arn
#}

#resource "aws_iam_role_policy_attachment" "logs_attachment" {
#  role       = aws_iam_role.lambda_role.name
#  policy_arn = aws_iam_policy.logs_policy.arn
#}