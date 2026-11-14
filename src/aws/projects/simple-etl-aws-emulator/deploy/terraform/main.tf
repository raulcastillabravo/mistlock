terraform {
  required_providers {
    # >= 6.20: first version that accepts the python3.14 Lambda runtime.
    # < 6.23: from 6.23 aws_s3_bucket manages tags with S3 Control APIs
    # (hashicorp/terraform-provider-aws#45251), whose host name carries the
    # account ID (000000000000.127.0.0.1) and never reaches AWS Emulator.
    aws = { source = "hashicorp/aws", version = ">= 6.20, < 6.23" }
  }
}

# Endpoint, credentials, CA certificate and Region come from the AWS_*
# variables in .env, so the same code deploys to the emulator or to AWS.
provider "aws" {
  s3_use_path_style = true
}

variable "bucket_name" { type = string }
variable "table_name" { type = string }
variable "function_name" { type = string }
variable "role_name" { type = string }
variable "lambda_zip" { type = string }

resource "aws_s3_bucket" "file_uploads" {
  bucket        = var.bucket_name
  force_destroy = true
}

resource "aws_dynamodb_table" "file_logs" {
  name         = var.table_name
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "file_id"
  attribute {
    name = "file_id"
    type = "S"
  }
}

resource "aws_iam_role" "lambda_role" {
  name = var.role_name
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action    = "sts:AssumeRole"
      Effect    = "Allow"
      Principal = { Service = "lambda.amazonaws.com" }
    }]
  })
}

resource "aws_iam_role_policy" "lambda_policy" {
  name = var.role_name
  role = aws_iam_role.lambda_role.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = ["s3:GetObject", "s3:ListBucket"]
        Resource = [aws_s3_bucket.file_uploads.arn, "${aws_s3_bucket.file_uploads.arn}/*"]
      },
      {
        Effect   = "Allow"
        Action   = ["dynamodb:PutItem", "dynamodb:GetItem"]
        Resource = aws_dynamodb_table.file_logs.arn
      },
      {
        Effect   = "Allow"
        Action   = ["logs:CreateLogGroup", "logs:CreateLogStream", "logs:PutLogEvents"]
        Resource = "arn:aws:logs:*:*:*"
      }
    ]
  })
}

resource "aws_lambda_function" "s3_processor" {
  filename         = var.lambda_zip
  source_code_hash = filebase64sha256(var.lambda_zip)
  function_name    = var.function_name
  role             = aws_iam_role.lambda_role.arn
  handler          = "handler.lambda_handler"
  runtime          = "python3.14"
  timeout          = 30
  environment {
    variables = { DYNAMODB_TABLE_NAME = aws_dynamodb_table.file_logs.name }
  }
  depends_on = [aws_iam_role_policy.lambda_policy]
}

resource "aws_lambda_permission" "allow_s3" {
  statement_id  = "s3-trigger"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.s3_processor.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = aws_s3_bucket.file_uploads.arn
}

resource "aws_s3_bucket_notification" "bucket_notification" {
  bucket = aws_s3_bucket.file_uploads.id
  lambda_function {
    lambda_function_arn = aws_lambda_function.s3_processor.arn
    events              = ["s3:ObjectCreated:*"]
  }
  depends_on = [aws_lambda_permission.allow_s3]
}
