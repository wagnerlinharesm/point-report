provider "aws" {
  region = var.region
}

# -- queue

resource "aws_sqs_queue" "point_report_sqs_queue" {
  name                      = var.point_report_sqs_queue_name
  delay_seconds             = 0
  max_message_size          = 262144
  message_retention_seconds = 259200
  visibility_timeout_seconds = 30

  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.point_report_dlq_sqs_queue.arn
    maxReceiveCount     = 3
  })
}

resource "aws_sqs_queue" "point_report_dlq_sqs_queue" {
  name                      = "${var.point_report_sqs_queue_name}-dlq"
  delay_seconds             = 0
  max_message_size          = 262144
  message_retention_seconds = 1209600
  visibility_timeout_seconds = 30
}

# -- lambda

data "aws_secretsmanager_secret" "point_db_secretsmanager_secret" {
  name = var.point_db_secretsmanager_secret_name
}

data "aws_secretsmanager_secret_version" "point_db_secretsmanager_secret_version" {
  secret_id = data.aws_secretsmanager_secret.point_db_secretsmanager_secret.id
}

locals {
  point_db_credentials = jsondecode(data.aws_secretsmanager_secret_version.point_db_secretsmanager_secret_version.secret_string)
}

resource "aws_iam_role" "point_report_iam_role" {
  name               = "point_report_iam_role"
  assume_role_policy = file("iam/policy/assume_role_policy.json")
}

resource "aws_iam_role_policy_attachment" "point_report_sqs_iam_role_policy_attachment" {
  role       = aws_iam_role.point_report_iam_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaSQSQueueExecutionRole"
}

resource "aws_iam_role_policy_attachment" "point_report_ses_iam_role_policy_attachment" {
  role       = aws_iam_role.point_report_iam_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSESFullAccess"
}

resource "aws_lambda_function" "point_report_lambda_function" {
  function_name = "point_report"
  handler       = "app/lambda_function.handler"
  runtime       = "python3.11"
  role          = aws_iam_role.point_report_iam_role.arn

  filename = "lambda_function.zip"

  source_code_hash = filebase64sha256("lambda_function.zip")

  depends_on = [
    aws_iam_role.point_report_iam_role
  ]

  environment {
    variables = {
        POINT_DB_HOST       = var.point_db_host,
        POINT_DB_DATABASE   = var.point_db_database,
        POINT_DB_USERNAME   = local.point_db_credentials["username"]
        POINT_DB_PASSWORD   = local.point_db_credentials["password"]
    }
  }
}

# -- trigger

resource "aws_lambda_permission" "allow_sqs_to_invoke_lambda" {
  action        = "lambda:InvokeFunction"
  principal     = "sqs.amazonaws.com"

  source_arn = aws_sqs_queue.point_report_sqs_queue.arn
  function_name    = aws_lambda_function.point_report_lambda_function.function_name
}

resource "aws_lambda_event_source_mapping" "point_report_lambda_event_source_mapping" {
  event_source_arn = aws_sqs_queue.point_report_sqs_queue.arn
  function_name    = aws_lambda_function.point_report_lambda_function.function_name
  batch_size       = 1
}