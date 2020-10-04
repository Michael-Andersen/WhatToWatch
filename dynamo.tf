resource "aws_dynamodb_table" "basic-dynamodb-table" {
  name           = "WhatToWatchDB"
  billing_mode   = "PROVISIONED"
  read_capacity  = 20
  write_capacity = 20
  hash_key       = "Field"

  attribute {
    name = "Field"
    type = "S"
  }

  attribute {
    name = "StringValue"
    type = "S"
  }

  attribute {
    name = "NumericalValue"
    type = "N"
  }

  ttl {
    attribute_name = ""
    enabled        = false
  }
  
  global_secondary_index {
    name               = "StringValueIndex"
    hash_key           = "StringValue"
    range_key          = "NumericalValue"
    write_capacity     = 10
    read_capacity      = 10
    projection_type    = "INCLUDE"
    non_key_attributes = ["Field"]
  }

}