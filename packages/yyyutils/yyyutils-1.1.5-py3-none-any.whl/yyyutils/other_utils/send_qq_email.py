import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os


def send_email(sender, smtp_password, recipient, subject, message,
               attachment_paths: Optional[Union[List[str], str]] = None, smtp_port=587):
    sender_email = str(sender)  # 发送方邮箱地址
    password = str(smtp_password)  # SMTP授权码
    smtp_server = 'smtp.qq.com'  # QQ邮箱SMTP服务器
    smtp_port = int(smtp_port)  # QQ邮箱SMTP服务端口号

    # 创建邮件对象
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = recipient

    # 添加邮件正文
    msg.attach(MIMEText(message, 'plain'))

    # 添加附件
    if attachment_paths:
        if isinstance(attachment_paths, str):
            attachment_paths = [attachment_paths]

        for attachment_path in attachment_paths:
            with open(attachment_path, 'rb') as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename= {attachment_path}')
                msg.attach(part)

    try:
        print(f"Connecting to {smtp_server} on port {smtp_port}")
        server = smtplib.SMTP(smtp_server, smtp_port)
        print("Starting TLS...")
        server.starttls()
        print("Logging in...")
        server.login(sender_email, password)
        print("Sending email...")
        server.sendmail(sender_email, recipient, msg.as_string())
        print("Email sent successfully!")
    except smtplib.SMTPException as e:
        print(f"Failed to send email: {e}")
    finally:
        print("Closing connection...")
        server.quit()
