import functools
import os
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from .config import DEFAULT_REGION, DEFAULT_CLOUD_PROVIDER

def check_aws_credentials():
    """
    Checks if AWS credentials are configured.
    Returns True if credentials are found, False otherwise.
    """
    try:
        session = boto3.Session()
        credentials = session.get_credentials()
        return credentials is not None and credentials.access_key is not None
    except (NoCredentialsError, PartialCredentialsError):
        return False

def deploy(target=DEFAULT_CLOUD_PROVIDER, region=DEFAULT_REGION):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if target.lower() == "aws":
                if not check_aws_credentials():
                    print("⚠️ AWS Credentials not found! Please configure them before deploying.")
                    print("To configure, run: `aws configure` or set environment variables.")
                    return
                
                print(f"Deploying to AWS in region {region} using boto3...")
                ec2 = boto3.client("ec2", region_name=region)
                try:
                    response = ec2.run_instances(
                        ImageId="ami-0c55b159cbfafe1f0",
                        InstanceType="t2.micro",
                        MinCount=1,
                        MaxCount=1
                    )
                    instance_id = response["Instances"][0]["InstanceId"]
                    print(f"✅ AWS deployment successful! Instance ID: {instance_id}")
                except Exception as e:
                    print("❌ AWS deployment failed:", e)
            else:
                print(f"🚀 Starting deployment to {target} in {region} (simulated)...")
                result = func(*args, **kwargs)
                print(f"✅ Deployment to {target} in {region} completed!")
                return result
        return wrapper
    return decorator
