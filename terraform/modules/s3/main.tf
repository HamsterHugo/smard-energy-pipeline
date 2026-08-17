resource "aws_s3_bucket" "bucket" {
  bucket        = var.bucket_name
  force_destroy = true
  tags          = var.tags
}

resource "aws_s3_bucket_website_configuration" "website" {
  bucket = var.bucket_name

  index_document {
    suffix = "index.html"
  }

  error_document {
    key = "index.html"
  }
}

resource "aws_s3_bucket_public_access_block" "public_access" {
  bucket = aws_s3_bucket.bucket.id

  block_public_acls       = var.public ? false : true
  block_public_policy     = var.public ? false : true
  ignore_public_acls      = var.public ? false : true
  restrict_public_buckets = var.public ? false : true
}

resource "aws_s3_bucket_policy" "public_read" {
  bucket     = aws_s3_bucket.bucket.id
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
          "${aws_s3_bucket.bucket.arn}/index.html",
          "${aws_s3_bucket.bucket.arn}/style.css",
          "${aws_s3_bucket.bucket.arn}/script.js",
          "${aws_s3_bucket.bucket.arn}/favicon.ico"
        ]
      }
    ]
  })
}

resource "aws_s3_object" "layer_zip" {
  bucket = aws_s3_bucket.bucket.id
  key    = "lambda-layer/layer.zip"
  source = var.layer_zip
  etag   = filemd5(var.layer_zip)
}
