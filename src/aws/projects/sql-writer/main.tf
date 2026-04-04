terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region                      = "us-east-1"
  access_key                  = "test"
  secret_key                  = "test"
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_requesting_account_id  = true
  endpoints {
    secretsmanager = var.aws_endpoint
    lambda         = var.aws_endpoint
    iam            = var.aws_endpoint
  }
}

variable "postgres_user" {}
variable "postgres_password" {}
variable "postgres_host" {}
variable "postgres_port" {}
variable "postgres_db" {}
variable "aws_endpoint" {}

# Secret for DB Credentials in JSON format
resource "aws_secretsmanager_secret" "db_credentials" {
  name = "postgres-credentials"
}

resource "aws_secretsmanager_secret_version" "db_credentials_val" {
  secret_id     = aws_secretsmanager_secret.db_credentials.id
  secret_string = jsonencode({
    user     = var.postgres_user
    password = var.postgres_password
    host     = "host.docker.internal" # Accessing host from Lambda container
    port     = var.postgres_port
    dbname   = var.postgres_db
  })
}

# IAM Role for Lambda
resource "aws_iam_role" "lambda_role" {
  name = "lambda-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = { Service = "lambda.amazonaws.com" }
    }]
  })
}

# Lambda Function
resource "aws_lambda_function" "add_user" {
  filename      = "lambda.zip"
  function_name = "AddUserFunction"
  role          = aws_iam_role.lambda_role.arn
  handler       = "lambda_handler.lambda_handler"
  runtime       = "python3.11"
  timeout       = 30

  source_code_hash = fileexists("lambda.zip") ? filebase64sha256("lambda.zip") : null

  environment {
    variables = {
      AWS_ENDPOINT_URL = var.aws_endpoint
    }
  }
}
