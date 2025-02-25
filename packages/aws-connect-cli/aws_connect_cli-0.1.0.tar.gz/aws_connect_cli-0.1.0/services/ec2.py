import typer
import boto3
from botocore.exceptions import NoCredentialsError, ClientError
from InquirerPy import inquirer
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

app = typer.Typer()
console = Console()

AWS_REGION_HELP = "AWS region (optional)"

def get_ec2_client(region: str = None):
    session = boto3.Session()
    return session.client("ec2", region_name=region)

def fetch_instances():
    """Fetches all EC2 instances and returns a list of them."""
    client = get_ec2_client()
    instances = []
    try:
        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:
            progress.add_task(description="Fetching EC2 instances...", total=None)
            response = client.describe_instances()
        for reservation in response.get("Reservations", []):
            for instance in reservation.get("Instances", []):
                instances.append(instance)
        return instances
    except (NoCredentialsError, ClientError) as e:
        console.print(f"[red]Error fetching instances: {e}[/red]")
        return []

@app.command("ls")
def list_instances():
    """
    Lists all EC2 instances interactively using arrow keys and displays full details of the selected instance.
    """
    instances = fetch_instances()
    if not instances:
        console.print("[red]No EC2 instances found or unable to fetch instances.[/red]")
        raise typer.Exit()

    # Prepare a rich table to display summary information.
    table = Table(title="Available EC2 Instances", style="cyan", header_style="bold magenta")
    table.add_column("Instance ID", style="green")
    table.add_column("State", style="yellow")
    table.add_column("Type", style="blue")

    choices = []
    for instance in instances:
        instance_id = instance.get("InstanceId", "N/A")
        state = instance.get("State", {}).get("Name", "N/A")
        instance_type = instance.get("InstanceType", "N/A")
        table.add_row(instance_id, state, instance_type)
        choices.append(f"{instance_id} | {state} | {instance_type}")

    console.print(table)

    # Interactive selection using InquirerPy.
    selected_instance_str = inquirer.select(
        message="Select an instance to view details:",
        choices=choices,
        default=choices[0]
    ).execute()

    # Extract instance ID from selection.
    selected_instance_id = selected_instance_str.split(" | ")[0]
    selected_instance = next((i for i in instances if i["InstanceId"] == selected_instance_id), None)

    if not selected_instance:
        console.print("[red]Error: Instance not found.[/red]")
        raise typer.Exit()

    # Display full details in a formatted Rich table.
    detail_table = Table(title=f"Details for Instance {selected_instance_id}", style="bright_blue", header_style="bold magenta")
    detail_table.add_column("Attribute", style="magenta", no_wrap=True)
    detail_table.add_column("Value", style="white")

    for key, value in selected_instance.items():
        detail_table.add_row(str(key), str(value))

    console.print(detail_table)

def perform_action(instance_id: str, action: str, region: str = None):
    client = get_ec2_client(region)
    try:
        if action == "start":
            client.start_instances(InstanceIds=[instance_id])
        elif action == "stop":
            client.stop_instances(InstanceIds=[instance_id])
        elif action == "reboot":
            client.reboot_instances(InstanceIds=[instance_id])
        elif action == "hibernate":
            # Ensure the instance supports hibernation.
            client.stop_instances(InstanceIds=[instance_id], Hibernate=True)
        elif action == "terminate":
            client.terminate_instances(InstanceIds=[instance_id])
        else:
            console.print(f"[red]Invalid action: {action}[/red]")
            raise typer.Exit()
        console.print(f"[green]{action.capitalize()} command sent successfully to instance {instance_id}.[/green]")
    except (ClientError, NoCredentialsError) as e:
        console.print(f"[red]Error performing {action} on instance {instance_id}: {e}[/red]")

@app.command("start")
def start_instance(
    instance_id: str = typer.Argument(..., help="The ID of the EC2 instance to start"),
    region: str = typer.Option(None, help="")
):
    """Start an EC2 instance."""
    perform_action(instance_id, "start", region)

@app.command("stop")
def stop_instance(
    instance_id: str = typer.Argument(..., help="The ID of the EC2 instance to stop"),
    region: str = typer.Option(None, help=AWS_REGION_HELP)
):
    """Stop an EC2 instance."""
    perform_action(instance_id, "stop", region)

@app.command("reboot")
def reboot_instance(
    instance_id: str = typer.Argument(..., help="The ID of the EC2 instance to reboot"),
    region: str = typer.Option(None, help=AWS_REGION_HELP)
):
    """Reboot an EC2 instance."""
    perform_action(instance_id, "reboot", region)

@app.command("hibernate")
def hibernate_instance(
    instance_id: str = typer.Argument(..., help="The ID of the EC2 instance to hibernate"),
    region: str = typer.Option(None, help=AWS_REGION_HELP)
):
    """Hibernate an EC2 instance."""
    perform_action(instance_id, "hibernate", region)

@app.command("terminate")
def terminate_instance(
    instance_id: str = typer.Argument(..., help="The ID of the EC2 instance to terminate"),
    region: str = typer.Option(None, help=AWS_REGION_HELP)
):
    """Terminate an EC2 instance."""
    confirm = typer.confirm(f"Are you sure you want to terminate instance {instance_id}? This cannot be undone.")
    if not confirm:
        console.print("[yellow]Termination cancelled.[/yellow]")
        raise typer.Exit()
    perform_action(instance_id, "terminate", region)
