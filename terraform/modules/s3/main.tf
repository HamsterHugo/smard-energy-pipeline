resource "aws_s3_bucket" "s3_bucket" {
  bucket        = var.bucket_name
  force_destroy = true
  tags          = var.tags
}

resource "aws_s3_bucket_website_configuration" "website" {
  bucket = aws_s3_bucket.s3_bucket.id
  count  = var.public ? 1 : 0

  index_document {
    suffix = "index.html"
  }

  error_document {
    key = "index.html"
  }
}

resource "aws_s3_bucket_public_access_block" "public_access" {
  bucket = aws_s3_bucket.s3_bucket.id

  block_public_acls       = var.public ? false : true
  block_public_policy     = var.public ? false : true
  ignore_public_acls      = var.public ? false : true
  restrict_public_buckets = var.public ? false : true
}

resource "aws_s3_bucket_policy" "public_read" {
  count      = var.public ? 1 : 0
  bucket     = aws_s3_bucket.s3_bucket.id
  depends_on = [aws_s3_bucket_public_access_block.public_access]

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid       = "PublicReadFrontend"
        Effect    = "Allow"
        Principal = "*"
        Action    = "s3:GetObject"
        Resource = [
          "${aws_s3_bucket.s3_bucket.arn}/index.html",
          "${aws_s3_bucket.s3_bucket.arn}/style.css",
          "${aws_s3_bucket.s3_bucket.arn}/script.js",
          "${aws_s3_bucket.s3_bucket.arn}/favicon.ico"
        ]
      }
    ]
  })
}