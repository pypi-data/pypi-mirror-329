from ..function.get_settings import get_settings
from .basic import app
import typer


def send_email(to: str, subject: str, body: str):
    settings = get_settings()
    """Send a test email."""
    import emails
    try:
        message = emails.Message(
            subject=subject,
            html=body,
            mail_from=settings.SENDER_EMAIL  # Ensure this is defined in settings
        )
        
        response = message.send(
            to=to,
            smtp={
                "host": settings.SMTP_SERVER,
                "port": settings.SMTP_PORT,
                "user": settings.SMTP_USERNAME,
                "password": settings.SMTP_PASSWORD,
                "tls": True
            }
        )

        typer.echo(typer.style(f"Email sent successfully to {to}!", fg=typer.colors.GREEN))

    except Exception as e:
        typer.echo(typer.style(f"Error: {e}", fg=typer.colors.RED))

@app.command("testmail")
def test_mail(to: str, subject: str = "Test Email", body: str = "<h3>Hello, this is a test email!</h3>"):
    """Send a test email."""
    send_email(to=to, subject=subject, body=body)

if __name__ == "__main__":
    app()
