from pydantic import (
    BaseModel, 
    EmailStr
)

class EmailConfig(BaseModel):
    email_host: str
    email_port: int
    is_tls: bool
    email_host_user: str
    email_host_password: str

class EmailHeader(BaseModel):
    recipient_email: list[EmailStr]
    sender_email: EmailStr

class EmailContent(BaseModel):
    subject: str
    is_html: bool
    body: str

class EmailToSend(BaseModel):
    email_header: EmailHeader
    email_content: EmailContent

