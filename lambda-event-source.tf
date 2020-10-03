resource "aws_lambda_event_source_mapping" "event_source_mapping" {
  event_source_arn = aws_sqs_queue.lambda_queue.arn
  enabled          = true
  function_name    = aws_lambda_function.aws_lambda_test.arn
  batch_size       = 1
}