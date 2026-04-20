import logging
from pydantic import SecretStr
from fastapi import HTTPException
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, NameEmail, MessageType
from app.core.config import settings

FRONTEND_URL = "http://localhost:3000"  # Dev; prod: "https://parmenide.me"

logger = logging.getLogger(__name__)

conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USER,
    MAIL_PASSWORD=SecretStr(settings.MAIL_PASS),
    MAIL_FROM=settings.MAIL_USER,
    MAIL_FROM_NAME="Nide Portfolio",
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_HOST,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=False
)


async def send_reset_email(email: str, name: str, token: str):
    if settings.MAIL_TEST_MODE:
        logger.info(f"TEST MODE - Password reset token for {email}: {token}")
        logger.info(
            f"TEST MODE - Reset URL: {FRONTEND_URL}/reset-password?token={token}")
        return

    html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Password Reset - Nide Portfolio</title>
    <style>
        body {{ font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; }}
        .button {{ background: #007bff; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; display: inline-block; }}
        .token {{ background: #f8f9fa; padding: 10px; font-family: monospace; word-break: break-all; }}
    </style>
</head>
<body>
    <h2>Hi {name},</h2>
    <p>You have requested a password reset for your Nide Portfolio account.</p>
    <p><strong>This link expires in {settings.PASSWORD_RESET_TOKEN_EXPIRE_HOURS} hour.</strong></p>
    <p style="text-align: center;">
        <a href="{FRONTEND_URL}/reset-password?token={token}" class="button">Reset Password</a>
    </p>
    <p style="font-size: 10px; color: #666; background: #f8f9fa; padding: 8px; font-family: monospace; word-break: break-all; border-radius: 4px; margin-top: 20px;">
        Token (fallback): {token}
    </p>
    <p>If you did not request this, ignore this email.</p>
    <p>Best,<br>Nide Portfolio Team</p>
</body>
</html>
    """

    message = MessageSchema(
        subject="Password Reset Request - Nide Portfolio",
        recipients=[NameEmail(email=email, name=name)],
        body=html_content,
        subtype=MessageType.html
    )
    fm = FastMail(conf)
    try:
        await fm.send_message(message)
        logger.info(f"Reset email sent to {email}")
    except Exception as e:
        logger.error(f"Email send failed for {email}: {e}")
        raise HTTPException(
            status_code=500, detail="Failed to send reset email. Try again.")
