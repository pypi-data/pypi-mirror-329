from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import jinja2
import logging
import markdownify
import os
from pathlib import Path
import smtplib
import ssl

from kortical.helpers import KorticalKnownException, load_from_path
from kortical.logging import logging_config

logging_config.init_logger()
logger = logging.getLogger(__name__)

kortical_smtp_server = None
kortical_smtp_port = None


def _render_email_template(template_path, **kwargs):
    template_text = load_from_path(template_path)
    template = jinja2.Template(template_text)
    return template.render(**kwargs)


def _handle_template_and_parameter_inputs(plain_text_template, html_template, template_parameters):
    if plain_text_template is None and html_template is None:
        raise KorticalKnownException(
            "Must specify at least one of ['plain_text_template', 'html_template'] + template_parameters.")
    if template_parameters is not None:
        if not isinstance(template_parameters, dict):
            raise KorticalKnownException("Must specify template_parameters as a dictionary.")
    else:
        template_parameters = {}

    plain_text = _render_email_template(plain_text_template, **template_parameters) if plain_text_template is not None else None
    html_text = _render_email_template(html_template, **template_parameters) if html_template is not None else None

    return plain_text, html_text


def _handle_plain_text_and_html_text_inputs(plain_text, html_text):
    if plain_text is None and html_text is None:
        raise KorticalKnownException(
            "Must specify at least one of ['plain_text', 'html_text'].")

    if plain_text is None and html_text is not None:
        plain_text = markdownify.markdownify(html_text)

    return plain_text, html_text


def init(smtp_server, smtp_port):
    global kortical_smtp_server
    global kortical_smtp_port

    kortical_smtp_server = smtp_server
    kortical_smtp_port = smtp_port


def build_message(
        from_name,
        from_email,
        to_emails,
        subject,
        plain_text=None,
        html_text=None,
        attachments=None,
        cc_emails=None,
        bcc_emails=None,
        reply_to_name=None,
        reply_to_email=None):

    plain_text, html_text = _handle_plain_text_and_html_text_inputs(plain_text, html_text)

    if isinstance(to_emails, str):
        to_emails = [to_emails]
    if attachments is not None:
        if isinstance(attachments, str):
            attachments = [attachments]
    else:
        attachments = []
    if cc_emails is not None:
        if isinstance(cc_emails, str):
            cc_emails = [cc_emails]
    else:
        cc_emails = []

    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = f"{from_name} <{from_email}>"
    message["To"] = ', '.join(to_emails)

    if len(cc_emails) > 0:
        message["CC"] = ', '.join(cc_emails)

    if reply_to_email:
        message["Reply-To"] = f"{reply_to_name} <{reply_to_email}>" if reply_to_name else reply_to_email

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(plain_text, "plain")
    part2 = MIMEText(html_text, "html")

    # List of files to attach
    for filepath in attachments:
        filename = Path(filepath).name
        filepath = os.path.abspath(filepath)
        with open(filepath, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename={filename}")
        message.attach(part)

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)
    return message


def send_message(
        from_email,
        from_password,
        to_emails,
        message):

    global kortical_smtp_server
    global kortical_smtp_port

    if kortical_smtp_server is None or kortical_smtp_port is None:
        raise KorticalKnownException("You must first run kortical.reporting.email.init() with a server and port configuration.")

    if isinstance(to_emails, str):
        to_emails = [to_emails]

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(kortical_smtp_server, kortical_smtp_port, context=context) as server:
        server.login(from_email, from_password)
        server.sendmail(from_email, to_emails, message.as_string())


def send_email(
        from_name,
        from_email,
        from_password,
        to_emails,
        subject,
        plain_text=None,
        html_text=None,
        attachments=None,
        cc_emails=None,
        bcc_emails=None,
        reply_to_name=None,
        reply_to_email=None):

    message = build_message(from_name, from_email, to_emails, subject, plain_text, html_text, attachments, cc_emails, bcc_emails, reply_to_name, reply_to_email)

    if isinstance(to_emails, str):
        to_emails = [to_emails]

    if cc_emails is not None:
        if isinstance(cc_emails, str):
            cc_emails = [cc_emails]
    else:
        cc_emails = []

    if bcc_emails is not None:
        if isinstance(bcc_emails, str):
            bcc_emails = [bcc_emails]
    else:
        bcc_emails = []

    logger.info(f"kortical: sending email message to {to_emails}")
    if len(cc_emails) > 0:
        logger.info(f"kortical: CC to {cc_emails}")
        to_emails += cc_emails
    if len(bcc_emails) > 0:
        logger.info(f"kortical: BCC to {bcc_emails}")
        to_emails += bcc_emails

    send_message(from_email, from_password, to_emails, message)


def send_email_from_template(
        from_name,
        from_email,
        from_password,
        to_emails,
        subject,
        plain_text_template=None,
        html_template=None,
        template_parameters=None,
        attachments=None,
        cc_emails=None,
        bcc_emails=None,
        reply_to_name=None,
        reply_to_email=None):

    plain_text, html_text = _handle_template_and_parameter_inputs(plain_text_template, html_template, template_parameters)

    send_email(from_name, from_email, from_password, to_emails, subject, plain_text, html_text, attachments, cc_emails, bcc_emails, reply_to_name, reply_to_email)
