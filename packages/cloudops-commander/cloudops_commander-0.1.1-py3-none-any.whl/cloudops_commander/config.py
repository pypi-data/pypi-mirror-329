DEFAULT_REGION = "us-east-1"
DEFAULT_CLOUD_PROVIDER = "aws"

def get_config():
    return {
        "region": DEFAULT_REGION,
        "provider": DEFAULT_CLOUD_PROVIDER,
    }
