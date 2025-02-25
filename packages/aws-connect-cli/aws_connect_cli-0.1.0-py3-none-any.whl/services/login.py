import typer
import boto3
import getpass
import configparser
from pathlib import Path
from botocore.exceptions import NoCredentialsError, ClientError
from rich.console import Console
from InquirerPy import inquirer

app = typer.Typer()
console = Console()

AWS_CREDENTIALS_FILE = Path.home() / ".aws" / "credentials"
AWS_CONFIG_FILE = Path.home() / ".aws" / "config"
CREATE_NEW_ACCOUNT = "Create New Account"

def list_profiles():
    """Reads and returns all available AWS profiles from the credentials file."""
    config = configparser.ConfigParser()
    if AWS_CREDENTIALS_FILE.exists():
        config.read(AWS_CREDENTIALS_FILE)
        return config.sections()
    return []

def save_credentials(profile_name, aws_access_key, aws_secret_key):
    """Saves AWS credentials under a specific profile."""
    config = configparser.ConfigParser()
    if AWS_CREDENTIALS_FILE.exists():
        config.read(AWS_CREDENTIALS_FILE)
    config[profile_name] = {
        "aws_access_key_id": aws_access_key,
        "aws_secret_access_key": aws_secret_key
    }
    AWS_CREDENTIALS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with AWS_CREDENTIALS_FILE.open("w") as configfile:
        config.write(configfile)
    console.print(f"[green]AWS credentials saved successfully under profile: {profile_name}[/green]")

def save_config(profile_name, aws_region):
    """Saves AWS region under a specific profile."""
    config = configparser.ConfigParser()
    if AWS_CONFIG_FILE.exists():
        config.read(AWS_CONFIG_FILE)
    # AWS CLI config typically uses "profile <name>" for non-default profiles
    section = "default" if profile_name == "default" else f"profile {profile_name}"
    config[section] = {
        "region": aws_region,
        "output": "json"
    }
    AWS_CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with AWS_CONFIG_FILE.open("w") as configfile:
        config.write(configfile)
    console.print(f"[green]AWS configuration saved for profile: {profile_name}[/green]")

def create_new_account():
    """Prompts the user to enter AWS credentials for a new account and saves them."""
    profile_name = inquirer.text(
        message="Enter a profile name for this account:",
    ).execute()
    aws_access_key = inquirer.text(
        message="AWS Access Key ID:"
    ).execute()
    # Using getpass for secure input
    aws_secret_key = getpass.getpass("AWS Secret Access Key: ")
    aws_region = inquirer.text(
        message="AWS Region:",
        default="us-east-1"
    ).execute()

    save_credentials(profile_name, aws_access_key, aws_secret_key)
    save_config(profile_name, aws_region)
    console.print(f"[green]New AWS account added under profile: {profile_name}[/green]")
    return profile_name

@app.command("login")
def aws_login():
    """
    Allows users to choose an existing AWS profile or add a new account.
    """
    profiles = list_profiles()
    choices = []
    if profiles:
        # Create a list of choices for interactive selection.
        for profile in profiles:
            choices.append(profile)
    # Always add the option to create a new account.
    choices.append(CREATE_NEW_ACCOUNT)

    selected_profile = inquirer.select(
        message="Select an AWS profile:",
        choices=choices,
        default=profiles[0] if profiles else CREATE_NEW_ACCOUNT
    ).execute()

    if selected_profile == CREATE_NEW_ACCOUNT:
        selected_profile = create_new_account()

    # Use the selected profile
    try:
        session = boto3.Session(profile_name=selected_profile)
        sts = session.client("sts")
        identity = sts.get_caller_identity()
        account_id = identity.get("Account")
        console.print(f"[bold green]Successfully logged in with profile '{selected_profile}'. Account ID: {account_id}[/bold green]")
    except NoCredentialsError:
        console.print("[bold red]Invalid credentials or missing permissions![/bold red]")
    except ClientError as e:
        console.print(f"[bold red]Failed to log in: {e}[/bold red]")
