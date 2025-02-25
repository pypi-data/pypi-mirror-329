import os
import platform
import shutil
import subprocess
import uuid
from typing import Optional

import boto3
import botocore
import click
import semver

from tensorkube.constants import CliColors
from tensorkube.constants import get_cluster_name, DEFAULT_NAMESPACE, LOCKED_AWS_CLI_VERSION
from tensorkube.services.error import CLIVersionError
from tensorkube.services.s3_service import list_s3_buckets


def get_session_region():
    return boto3.session.Session().region_name


def get_eks_client():
    return boto3.client("eks")


def get_cloudformation_client():
    return boto3.client("cloudformation")


def get_ec2_client():
    return boto3.client("ec2")


def get_iam_client():
    return boto3.client("iam")


def get_aws_account_id():
    sts = boto3.client('sts')
    identity = sts.get_caller_identity()
    return identity['Account']


def get_aws_user_arn() -> str:
    sts = boto3.client('sts')
    identity = sts.get_caller_identity()
    return identity['Arn']


def get_principal_arn_from_identity_center_arn(arn: str) -> str:
    arn_parts = arn.split(':')
    account_no = arn_parts[4]
    role_name = arn_parts[5].split('/')[1]
    principal_arn = f"arn:aws:iam::{account_no}:role/aws-reserved/sso.amazonaws.com/{role_name}"
    return principal_arn


def get_aws_user_principal_arn() -> str:
    sts = boto3.client('sts')
    identity = sts.get_caller_identity()
    if 'assumed-role' in identity['Arn']:
        return get_principal_arn_from_identity_center_arn(identity['Arn'])
    return identity['Arn']


def get_karpenter_namespace():
    return "kube-system"


def get_karpenter_version():
    return "0.37.0"


def get_aws_default_region():
    return "us-east-1"


def get_kubernetes_context_name():
    return f"{get_cluster_name()}.{get_aws_default_region()}.eksctl.io"


def get_credentials():
    return boto3.Session().get_credentials().get_frozen_credentials()


def are_credentials_valid(credentials):
    sts = boto3.client('sts', aws_access_key_id=credentials.access_key, aws_secret_access_key=credentials.secret_key,
                       aws_session_token=credentials.token)
    try:
        sts.get_caller_identity()
        return True
    except botocore.exceptions.ClientError as e:
        return False


# TODO!: make function generic to get any config value
def get_bucket_name(env_name: Optional[str] = None, type: str = "build"):
    buckets = list_s3_buckets()
    if env_name and env_name != DEFAULT_NAMESPACE:
        prefix = f'{get_cluster_name()}-{env_name}-{type}-bucket-'
    else:
        prefix = f'{get_cluster_name()}-{type}-bucket-'
    # checks if such a bucket already exists
    for bucket in buckets:
        if bucket['Name'].startswith(prefix):
            return bucket['Name']
    else:
        bucket_name = f"{prefix}{str(uuid.uuid4())[:18]}"
        if len(bucket_name) > 63:
            raise ValueError("Environment name is too long. Please use a shorter name.")
        return bucket_name


def check_and_install_aws_cli():
    """Check if aws cli is installed and if not install it."""
    try:
        result = subprocess.run(["aws", "--version"], capture_output=True, text=True, check=True)

        # The version is in the format: "aws-cli/2.13.4 Python/3.9.6 Linux/x86_64"
        version_output = result.stdout.strip()
        # Extract the AWS CLI version using string manipulation
        aws_version = semver.VersionInfo.parse(version_output.split(" ")[0].split("/")[1])
        locked_cli_version = semver.VersionInfo.parse(LOCKED_AWS_CLI_VERSION)
        if (aws_version.major, aws_version.minor) < (locked_cli_version.major, locked_cli_version.minor):
            text = f"AWS CLI version is {aws_version}. Please upgrade AWS CLI to version above {LOCKED_AWS_CLI_VERSION}."
            click.echo(click.style(text, bold=True, fg=CliColors.ERROR.value))
            raise CLIVersionError(text)
    except Exception as e:
        if isinstance(e, CLIVersionError):
            raise e
        click.echo(
            click.style("aws-cli not found. Proceeding with installation. Might require sudo password.", bold=True,
                        fg=CliColors.WARNING.value))
        try:
            system = platform.system().lower()
            architecture = platform.machine()
            print(f"Detected operating system: {system.capitalize()}")
            print(f"Detected architecture: {architecture}")
            url = ""
            file_name = ""
            # Define the download URL and file name based on the OS
            if system == "linux":
                url = f"https://awscli.amazonaws.com/awscli-exe-linux-{architecture}-{LOCKED_AWS_CLI_VERSION}.zip"
                file_name = f"awscliv2-{LOCKED_AWS_CLI_VERSION}.zip"
            elif system == "darwin":
                url = f"https://awscli.amazonaws.com/AWSCLIV2-{LOCKED_AWS_CLI_VERSION}.pkg"
                file_name = f"AWSCLIV2-{LOCKED_AWS_CLI_VERSION}.pkg"
            else:
                print("Unsupported operating system. Please install AWS CLI manually.")
                raise Exception("Unsupported operating system.")
            # Download the installer
            print(f"Downloading AWS CLI installer from {url}...")
            subprocess.run(["curl", "-fsSL", url, "-o", file_name], check=True)
            print("AWS CLI installer downloaded successfully.")
            if system == "linux":
                # Unzip the installer
                print("Unzipping the AWS CLI installer...")
                subprocess.run(["unzip", "-o", file_name], check=True)
                print("AWS CLI installer unzipped successfully.")

                # Install the AWS CLI
                print("Installing AWS CLI...")
                subprocess.run(["sudo", "./aws/install"], check=True)
                print("AWS CLI installed successfully.")

            elif system == "darwin":
                # Use the macOS installer
                print("Installing AWS CLI using macOS package...")
                subprocess.run(["sudo", "installer", "-pkg", file_name, "-target", "/"], check=True)
                print("AWS CLI installed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error occurred during installation: {e}")
        finally:
            if os.path.exists(file_name):
                os.remove(file_name)
            if os.path.exists("aws"):
                shutil.rmtree("aws")
            print("Clean-up completed.")
