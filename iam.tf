resource "aws_iam_role" "lambda_exec_role" {
  name = "lambda_exec_role"
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      }
    }
  ]
}
EOF
}

data "aws_iam_policy_document" "lambda_policy_doc" {
  statement {
    sid = "AllowCreatingLogGroups"
    effect = "Allow"

    resources = [
      "arn:aws:logs:*:*:*"
    ]

    actions = [
      "logs:CreateLogGroup"
    ]
  }

  statement {
    sid = "AllowWritingLogs"
    effect = "Allow"

    resources = [
      "arn:aws:logs:*:*:log-group:/aws/lambda/*:*"
    ]

    actions = [
      "logs:CreateLogStream",
      "logs:PutLogEvents",
    ]
  }
  
  statement {
    sid = "AllowReadingAndWritingBucket"
    effect = "Allow"

    resources = [
      "${aws_s3_bucket.bucket_json.arn}",
        "${aws_s3_bucket.bucket_json.arn}/*"
    ]

    actions = [
    "s3:*"
    ]
  }

  statement {
    sid = "AllowReadingSQS"
    effect = "Allow"

    resources = [
     "${aws_sqs_queue.lambda_queue.arn}",
    ]

    actions = [
    "sqs:*"
    ]
  }
  statement {
    sid = "AllowUpdateDB"
    effect = "Allow"

    resources = [
     "${aws_dynamodb_table.basic-dynamodb-table.arn}",
    ]

    actions = [
    "dynamodb:*"
    ]
  }
}

resource "aws_iam_policy" "lambda_iam_policy" {
  name = "lambda_iam_policy"
  policy = data.aws_iam_policy_document.lambda_policy_doc.json
}

resource "aws_iam_role_policy_attachment" "lambda_policy_attachment" {
  policy_arn = aws_iam_policy.lambda_iam_policy.arn
  role = aws_iam_role.lambda_exec_role.name
}