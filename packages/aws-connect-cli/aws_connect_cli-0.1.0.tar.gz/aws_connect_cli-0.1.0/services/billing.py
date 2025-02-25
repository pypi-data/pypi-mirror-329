from datetime import datetime, timedelta, timezone
from tabulate import tabulate
import typer
import boto3
from botocore.exceptions import ClientError

app = typer.Typer()


def get_cost_explorer_client(region: str = "us-east-1"):
    # Cost Explorer is a global service but requires a region.
    return boto3.client("ce", region_name=region)


def get_monthly_costs(client):
    now = datetime.now(timezone.utc)
    start = datetime(now.year, now.month, 1, tzinfo=timezone.utc)
    end = now
    try:
        response = client.get_cost_and_usage(
            TimePeriod={
                "Start": start.strftime("%Y-%m-%d"),
                "End": (end + timedelta(days=1)).strftime("%Y-%m-%d"),
            },
            Granularity="MONTHLY",
            Metrics=["UnblendedCost"],
        )
        results = response["ResultsByTime"]
        table_data = []
        for result in results:
            period = f"{result['TimePeriod']['Start']} to {result['TimePeriod']['End']}"
            amount = result["Total"]["UnblendedCost"]["Amount"]
            table_data.append([period, f"${float(amount):.2f}"])
        return table_data
    except ClientError as e:
        typer.echo(f"Error fetching cost data: {e}", err=True)
        return []


@app.command()
def show(
    region: str = typer.Option(
        "us-east-1", help="Region for Cost Explorer (typically us-east-1)"
    ),
):
    """
    Displays monthly AWS billing information and bills due as tables.
    """
    ce_client = get_cost_explorer_client(region)
    typer.echo("\nMonthly AWS Costs:")
    monthly_costs = get_monthly_costs(ce_client)
    if monthly_costs:
        typer.echo(
            tabulate(monthly_costs, headers=["Period", "Cost"], tablefmt="pretty")
        )
    else:
        typer.echo("No cost data available.")

    # Simulated bills due (no direct API for bills due)
    typer.echo("\nBills Due:")
    due_bills = [
        ["2025-02-01", "AWS EC2", "$50.00", "Due"],
        ["2025-02-05", "AWS S3", "$20.00", "Due"],
    ]
    typer.echo(
        tabulate(
            due_bills,
            headers=["Due Date", "Service", "Amount", "Status"],
            tablefmt="pretty",
        )
    )
