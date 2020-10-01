variable "bucket_for_json" {
  description = "Bucket name for json"
  default = "aws-what-to-watch-json"
}

variable "function_name" {
  description = "function name for lambda"
  default = "what_to_watch_lambda"
}

variable "runtime" {
  default = "python3.8"
}

variable "output_path" {
  description = "Path to function's deployment package into local filesystem. eg: /path/lambda_function.zip"
  default = "function.zip"
}