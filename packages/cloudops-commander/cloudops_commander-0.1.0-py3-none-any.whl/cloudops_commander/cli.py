import argparse
import sys
from .deploy import deploy
from .monitor import watch
from .iac import generate_terraform_config, generate_cloudformation_config

def main():
    parser = argparse.ArgumentParser(description="CloudOps Commander CLI")
    subparsers = parser.add_subparsers(dest="command")

    deploy_parser = subparsers.add_parser("deploy", help="Deploy the application to the cloud")
    deploy_parser.add_argument("--target", type=str, default="aws", help="Cloud target (aws, azure, gcp)")
    deploy_parser.add_argument("--region", type=str, default="us-east-1", help="Cloud region")

    monitor_parser = subparsers.add_parser("monitor", help="Monitor a microservice")
    monitor_parser.add_argument("--service", type=str, required=True, help="Service name to monitor")

    iac_parser = subparsers.add_parser("iac", help="Generate Infrastructure as Code configurations")
    iac_parser.add_argument("--provider", type=str, choices=["terraform", "cloudformation"], required=True, help="IaC provider")

    args = parser.parse_args()

    if args.command == "deploy":
        print(f"Initiating deployment on {args.target} in region {args.region}...")
        @deploy(target=args.target, region=args.region)
        def dummy_app():
            print("App deployed successfully!")
        dummy_app()
    elif args.command == "monitor":
        print(f"Monitoring service: {args.service}")
        watch(service=args.service, alert_callback=lambda msg: print(f"[ALERT] {msg}"))
    elif args.command == "iac":
        if args.provider == "terraform":
            config = generate_terraform_config()
            print("Terraform Configuration:\n", config)
        elif args.provider == "cloudformation":
            config = generate_cloudformation_config()
            print("CloudFormation Configuration:\n", config)
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
