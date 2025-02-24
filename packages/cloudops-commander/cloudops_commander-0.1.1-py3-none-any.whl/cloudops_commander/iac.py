def generate_terraform_config():
    config = """
provider "aws" {
  region = "us-east-1"
}

resource "aws_instance" "example" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t2.micro"
  tags = {
    Name = "CloudOpsInstance"
  }
}
"""
    return config.strip()

def generate_cloudformation_config():
    config = """
AWSTemplateFormatVersion: '2010-09-09'
Description: CloudOps Commander Sample CloudFormation Template
Resources:
  ExampleInstance:
    Type: AWS::EC2::Instance
    Properties:
      ImageId: ami-0c55b159cbfafe1f0
      InstanceType: t2.micro
      Tags:
        - Key: Name
          Value: CloudOpsInstance
"""
    return config.strip()
