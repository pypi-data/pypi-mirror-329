from cloudops_commander.iac import generate_terraform_config, generate_cloudformation_config

def test_generate_terraform_config():
    config = generate_terraform_config()
    assert "provider \"aws\"" in config
    assert "aws_instance" in config

def test_generate_cloudformation_config():
    config = generate_cloudformation_config()
    assert "AWSTemplateFormatVersion" in config
    assert "AWS::EC2::Instance" in config
