from email_validator import validate_email, EmailNotValidError

def validate_email_format(email: str) -> str:
    try:
        v = validate_email(email)
        return v.email  
    except EmailNotValidError:
        return None
    

