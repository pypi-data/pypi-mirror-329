import typer
import boto3
from botocore.exceptions import NoCredentialsError

app = typer.Typer()

@app.command("list")
def list_buckets():
    """
    Lists all S3 buckets.
    """
    try:
        session = boto3.Session()
        s3 = session.client("s3")
        response = s3.list_buckets()
        for bucket in response.get("Buckets", []):
            typer.echo(f"Bucket: {bucket['Name']}")
    except NoCredentialsError:
        typer.echo("AWS credentials not found. Please log in using 'aws-connect auth login'.", err=True)
