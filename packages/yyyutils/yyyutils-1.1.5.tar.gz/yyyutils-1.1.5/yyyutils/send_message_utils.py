import imaplib
import email
import itchat
from twilio.rest import Client
import qq
from email.header import decode_header
from email import policy
from yyyutils.data_structure_utils import StringUtils
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from typing import Optional, List, Union


class SendMessageUtils:
    """
    用于通过QQ邮箱或其他邮箱发送邮件的嵌套工具类，目前只支持QQ邮箱。
    """

    def __init__(self):
        pass

    class ByQQEmail:
        """
        用于通过QQ邮箱发送邮件的静态工具类。
        """

        @staticmethod
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

        @staticmethod
        async def send_email_async(recipient, subject, message):
            sender_email = '1992541488@qq.com'
            password = 'eubldafgdbuhdgea'  # Use a secure method for handling passwords
            smtp_server = 'smtp.qq.com'
            smtp_port = 587

            msg = MIMEText(message)
            msg['Subject'] = subject
            msg['From'] = sender_email
            msg['To'] = recipient

            try:
                with smtplib.SMTP(smtp_server, smtp_port) as server:
                    server.starttls()
                    server.login(sender_email, password)
                    server.sendmail(sender_email, recipient, msg.as_string())
            except Exception as e:
                print('Error sending email:', e)

        @staticmethod
        def __get_from_and_to(email_message):
            from_email = email_message['From']
            to_email = email_message['To']
            return from_email, to_email

        @staticmethod
        def __check_sender(sender, from_email):
            return StringUtils.b_is_substring_of_a(from_email.lower(), sender.lower())

        @staticmethod
        def __check_recipient(recipient, to_email):
            return StringUtils.b_is_substring_of_a(recipient.lower(), to_email.lower())

        @staticmethod
        def get_emails(username, password, imap_url='imap.qq.com', imap_port=993, search_criteria='ALL', sender=None,
                       check_num=None):
            search_conditions = {
                'ALL': 'ALL',
                'UNSEEN': 'UNSEEN',
                'SEEN': 'SEEN',
            }

            mail = imaplib.IMAP4_SSL(imap_url, imap_port)
            mail.login(username, password)
            mail.select('inbox')

            search_command = search_conditions.get(search_criteria, 'ALL')
            result, data = mail.search(None, search_command)
            if result != 'OK':
                print('No new emails to fetch')
                return
            email_ids = data[0].split()
            print(email_ids)
            if not email_ids:
                print('No emails found with the given criteria.')
                return
            if check_num:
                num = 1
            while email_ids:
                latest_email_id = email_ids.pop()
                _, msg_raw = mail.fetch(latest_email_id, '(RFC822)')
                raw_email = msg_raw[0][1].decode('utf-8')
                email_message = email.message_from_string(raw_email)
                if check_num:
                    if num > check_num:
                        break
                    num += 1
                if not sender:
                    break
                from_email, to_email = SendMessageUtils.ByQQEmail.__get_from_and_to(email_message)
                print(f"From: {from_email}, To: {to_email}")
                if SendMessageUtils.ByQQEmail.__check_sender(sender, from_email):
                    print(f"From: {from_email},FOUND")
                    break

            if check_num and num > check_num:
                print(f"Check {check_num} emails done.")
                return

            if len(email_ids) == 0:
                print('No more emails to fetch.')
                return

            for part in email_message.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))

                if content_type == 'text/plain' and 'attachment' not in content_disposition:
                    body = part.get_payload(decode=True).decode('utf-8')
                    print('Email Body:', body)
                    return body
                elif content_type == 'text/html' and 'attachment' not in content_disposition:
                    body = part.get_payload(decode=True).decode('utf-8')
                    print('HTML Email Body:', body)
                    return body

            mail.close()
            mail.logout()

        @staticmethod
        def get_all_senders(username: str, password: str, imap_url: str = 'imap.qq.com', imap_port: int = 993):
            """
            获取所有发件人信息的生成器
            :param username: 邮箱用户名
            :param password: 邮箱密码或授权码
            :param imap_url: IMAP服务器地址
            :param imap_port: IMAP服务器端口
            :yield: 元组 (序号, 发件人, 主题)
            """
            try:
                with imaplib.IMAP4_SSL(imap_url, imap_port) as mail:
                    mail.login(username, password)
                    mail.select('inbox')
                    _, message_numbers = mail.search(None, 'ALL')

                    for i, num in enumerate(message_numbers[0].split(), 1):
                        try:
                            _, msg_data = mail.fetch(num, '(RFC822)')
                            email_message = email.message_from_bytes(msg_data[0][1], policy=policy.default)

                            sender = email_message['From']
                            subject = email_message['Subject']

                            sender_str = SendMessageUtils.ByQQEmail.decode_header_safe(sender)
                            subject_str = SendMessageUtils.ByQQEmail.decode_header_safe(subject)

                            yield i, sender_str, subject_str

                        except Exception as e:
                            yield i, "Error processing email", None

            except imaplib.IMAP4.error as e:
                raise imaplib.IMAP4.error(f"IMAP error occurred: {e}")
            except Exception as e:
                raise Exception(f"An unexpected error occurred: {e}")

        @staticmethod
        def decode_header_safe(header) -> str:
            """
            安全地解码邮件头
            :param header: 邮件头字符串
            :return: 解码后的字符串
            """
            if header is None:
                return "N/A"
            try:
                decoded = decode_header(header)
                return ''.join(
                    part.decode(encoding or 'utf-8') if isinstance(part, bytes) else str(part)
                    for part, encoding in decoded
                )
            except Exception as e:
                print(f"Error decoding header: {e}")
                return str(header)

    class ByWechat:
        @staticmethod
        def send_message(wechat_username, message):
            itchat.auto_login()
            itchat.send_msg(message, toUserName=wechat_username)
            print(f"Message sent to WeChat: {wechat_username}")

        @staticmethod
        def get_messages():
            itchat.auto_login()
            messages = itchat.get_msg()
            for msg in messages:
                print(msg)
            return messages

    class ByQQ:
        @staticmethod
        def send_message(qq_number, message):
            # 假设你已经有了QQ的API密钥和相关配置
            client = qq.Client(api_key='your_api_key', api_secret='your_api_secret')
            client.send_message(qq_number, message)
            print(f"Message sent to QQ: {qq_number}")

        @staticmethod
        def get_messages():
            # 假设你已经有了QQ的API密钥和相关配置
            client = qq.Client(api_key='your_api_key', api_secret='your_api_secret')
            messages = client.get_messages()
            for msg in messages:
                print(msg)
            return messages

    class ByPhoneMessage:
        @staticmethod
        def send_message(phone_number, message):
            account_sid = 'your_account_sid'
            auth_token = 'your_auth_token'
            client = Client(account_sid, auth_token)

            message = client.messages.create(
                body=message,
                from_='your_twilio_phone_number',
                to=phone_number
            )
            print(f"Message sent to phone: {phone_number}")

        @staticmethod
        def get_messages():
            # Twilio不支持直接获取短信内容，需要通过回调URL获取
            # 这里假设你已经有了Twilio的API密钥和相关配置
            account_sid = 'your_account_sid'
            auth_token = 'your_auth_token'
            client = Client(account_sid, auth_token)

            messages = client.messages.list()
            for msg in messages:
                print(msg.body)
            return messages


if __name__ == '__main__':

    from mytools.auto_utils.moniter.moniter_keyboard_utils import MoniterKeyboardUtils


    def toggle_clicking_func():
        SendMessageUtils.ByQQEmail.send_email('2017894158@qq.com', 'test', '你好显眼包翠花奶浓')


    m = MoniterKeyboardUtils('F12', toggle_clicking_func=toggle_clicking_func)
    m.start()

    while True:
        pass
    # SendMessageUtils.ByQQEmail.send_email('2662464050@qq.com', 'test', 'test message')
