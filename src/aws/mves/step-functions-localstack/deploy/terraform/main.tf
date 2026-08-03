variable "aws_region" {}
variable "endpoint_url" {}
variable "role_name" {}
variable "table_name" {}
variable "log_user_function" {}
variable "validate_email_function" {}
variable "state_machine_name" {}
variable "lambda_runtime" {}

provider "aws" {
  region                      = var.aws_region
  access_key                  = "test"
  secret_key                  = "test"
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_requesting_account_id  = true

  endpoints {
    dynamodb       = var.endpoint_url
    iam            = var.endpoint_url
    lambda         = var.endpoint_url
    stepfunctions  = var.endpoint_url
  }
}

resource "aws_iam_role" "workflow" {
  name = var.role_name

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = ["lambda.amazonaws.com", "states.amazonaws.com"]
      }
    }]
  })
}

resource "aws_dynamodb_table" "user_logs" {
  name         = var.table_name
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "username"

  attribute {
    name = "username"
    type = "S"
  }
}

resource "aws_lambda_function" "log_user" {
  function_name = var.log_user_function
  filename      = "${path.module}/../../dist/log_user.zip"
  role          = aws_iam_role.workflow.arn
  handler       = "log_user.handler"
  runtime       = var.lambda_runtime
  timeout       = 30

  environment {
    variables = {
      DYNAMODB_TABLE = var.table_name
    }
  }
}

resource "aws_lambda_function" "validate_email" {
  function_name = var.validate_email_function
  filename      = "${path.module}/../../dist/validate_email.zip"
  role          = aws_iam_role.workflow.arn
  handler       = "validate_email.handler"
  runtime       = var.lambda_runtime
  timeout       = 30
}

resource "aws_sfn_state_machine" "onboarding" {
  name     = var.state_machine_name
  role_arn = aws_iam_role.workflow.arn

  definition = templatefile("${path.module}/../../step_function.asl.json", {
    LogUserLambdaArn       = aws_lambda_function.log_user.arn
    ValidateEmailLambdaArn = aws_lambda_function.validate_email.arn
  })
}
