data "archive_file" "create_dist_pkg" {
  source_dir = "function"
  output_path = var.output_path
  type = "zip"
}

resource "aws_lambda_function" "aws_lambda_test" {
  function_name = var.function_name
  description = "Process video and does face recognition..."
  handler = "lambda_function.lambda_handler"
  runtime = var.runtime
  role = aws_iam_role.lambda_exec_role.arn
  memory_size = 128
  timeout = 600
  source_code_hash = data.archive_file.create_dist_pkg.output_base64sha256
  filename = data.archive_file.create_dist_pkg.output_path
}
