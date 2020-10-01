provider "aws" {
  profile = "default"
  region = "us-west-1"
}

terraform {
	backend "s3" {
		bucket = "what-to-watch-tf-state"
		key    = "global/s3/terraform.tfstate"
		region = "us-west-1"
	}
}