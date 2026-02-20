"""
Email sender for application submissions.
Uses Python's built-in smtplib via Gmail SMTP — completely free.

Required environment variables (set on Render):
    GMAIL_USER          your Gmail address (e.g. yourname@gmail.com)
    GMAIL_APP_PASSWORD  16-char App Password from Google Account → Security → App Passwords
    ADMIN_EMAIL         where you want to receive applications (can be same as GMAIL_USER)
"""

import os
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime


GMAIL_USER         = os.environ.get('GMAIL_USER', '')
GMAIL_APP_PASSWORD = os.environ.get('GMAIL_APP_PASSWORD', '')
ADMIN_EMAIL        = os.environ.get('ADMIN_EMAIL', GMAIL_USER)


def send_application_email(application: dict) -> tuple[bool, str]:
    """
    Send a new application notification to the admin.
    Returns (success: bool, error_message: str).
    """
    if not GMAIL_USER or not GMAIL_APP_PASSWORD:
        return False, "Email not configured (GMAIL_USER / GMAIL_APP_PASSWORD missing)"

    subjects_list = application.get('subjects', [])
    if isinstance(subjects_list, str):
        subjects_list = subjects_list.split(',')

    submitted_at  = datetime.now().strftime('%d %B %Y at %H:%M')
    subject_line  = f"📩 New Application — {application['full_name']} | Rewrite Academy"

    # ── plain text body ─────────────────────────────────────────────────────
    plain = f"""NEW STUDENT APPLICATION
{'='*52}

Submitted: {submitted_at}

STUDENT DETAILS
  Name         : {application['full_name']}
  Phone        : {application['phone']}
  Email        : {application.get('email') or 'Not provided'}

PARENT / GUARDIAN
  Name         : {application.get('parent_name') or 'Not provided'}
  Phone        : {application.get('parent_phone') or 'Not provided'}

ACADEMIC
  Subjects     : {', '.join(subjects_list)}
  Previous School : {application.get('previous_school') or 'Not provided'}
  Year Failed  : {application.get('year_failed') or 'Not provided'}

MESSAGE FROM APPLICANT
  {application.get('message') or 'No message'}

{'='*52}
Reply to this email or call {application['phone']} to follow up.
— Rewrite Academy Automation
"""

    # ── HTML body ────────────────────────────────────────────────────────────
    subj_pills = ''.join(
        f'<span style="display:inline-block;margin:2px 4px 2px 0;padding:3px 10px;'
        f'border-radius:99px;background:rgba(34,211,238,.15);color:#22d3ee;'
        f'font-size:.8rem;font-weight:700;">{s.strip()}</span>'
        for s in subjects_list if s.strip()
    )

    html = f"""<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"></head>
<body style="margin:0;padding:0;background:#06080f;font-family:Inter,system-ui,sans-serif;">
<table width="100%" cellpadding="0" cellspacing="0" style="background:#06080f;padding:32px 0;">
  <tr><td align="center">
    <table width="600" cellpadding="0" cellspacing="0"
           style="background:#0c0f1e;border:1px solid rgba(34,211,238,.15);border-radius:16px;overflow:hidden;">

      <!-- header -->
      <tr>
        <td style="background:linear-gradient(135deg,rgba(34,211,238,.12),rgba(8,145,178,.06));
                   padding:28px 32px;border-bottom:1px solid rgba(34,211,238,.15);">
          <div style="font-family:Georgia,serif;font-size:1.4rem;font-weight:900;color:#f1f5f9;">
            Rewrite<span style="color:#22d3ee;">Academy</span>
          </div>
          <div style="color:#22d3ee;font-size:.75rem;text-transform:uppercase;letter-spacing:.1em;margin-top:6px;">
            📩 New Student Application
          </div>
        </td>
      </tr>

      <!-- body -->
      <tr><td style="padding:28px 32px;">

        <p style="color:#94a3b8;font-size:.82rem;margin:0 0 24px;">
          Submitted <strong style="color:#f1f5f9;">{submitted_at}</strong>
        </p>

        <!-- student -->
        <div style="background:#111527;border:1px solid rgba(34,211,238,.08);border-radius:10px;padding:20px;margin-bottom:16px;">
          <div style="font-size:.7rem;text-transform:uppercase;letter-spacing:.1em;color:#22d3ee;margin-bottom:10px;">Student</div>
          <table><tr>
            <td style="padding:4px 16px 4px 0;color:#94a3b8;font-size:.82rem;white-space:nowrap;">Full Name</td>
            <td style="color:#f1f5f9;font-size:.88rem;font-weight:700;">{application['full_name']}</td>
          </tr><tr>
            <td style="padding:4px 16px 4px 0;color:#94a3b8;font-size:.82rem;">Phone</td>
            <td style="color:#f1f5f9;font-size:.88rem;">{application['phone']}</td>
          </tr><tr>
            <td style="padding:4px 16px 4px 0;color:#94a3b8;font-size:.82rem;">Email</td>
            <td style="color:#f1f5f9;font-size:.88rem;">{application.get('email') or '—'}</td>
          </tr></table>
        </div>

        <!-- parent -->
        <div style="background:#111527;border:1px solid rgba(34,211,238,.08);border-radius:10px;padding:20px;margin-bottom:16px;">
          <div style="font-size:.7rem;text-transform:uppercase;letter-spacing:.1em;color:#94a3b8;margin-bottom:10px;">Parent / Guardian</div>
          <table><tr>
            <td style="padding:4px 16px 4px 0;color:#94a3b8;font-size:.82rem;white-space:nowrap;">Name</td>
            <td style="color:#f1f5f9;font-size:.88rem;">{application.get('parent_name') or '—'}</td>
          </tr><tr>
            <td style="padding:4px 16px 4px 0;color:#94a3b8;font-size:.82rem;">Phone</td>
            <td style="color:#f1f5f9;font-size:.88rem;">{application.get('parent_phone') or '—'}</td>
          </tr></table>
        </div>

        <!-- subjects -->
        <div style="background:#111527;border:1px solid rgba(34,211,238,.08);border-radius:10px;padding:20px;margin-bottom:16px;">
          <div style="font-size:.7rem;text-transform:uppercase;letter-spacing:.1em;color:#94a3b8;margin-bottom:10px;">Subjects</div>
          <div>{subj_pills}</div>
          <div style="margin-top:12px;">
            <span style="color:#94a3b8;font-size:.82rem;">Previous School: </span>
            <span style="color:#f1f5f9;font-size:.82rem;">{application.get('previous_school') or '—'}</span>
            &nbsp;&nbsp;
            <span style="color:#94a3b8;font-size:.82rem;">Year Failed: </span>
            <span style="color:#f1f5f9;font-size:.82rem;font-weight:700;">{application.get('year_failed') or '—'}</span>
          </div>
        </div>

        <!-- message -->
        {f'<div style="background:#111527;border:1px solid rgba(34,211,238,.08);border-radius:10px;padding:20px;margin-bottom:16px;"><div style="font-size:.7rem;text-transform:uppercase;letter-spacing:.1em;color:#94a3b8;margin-bottom:10px;">Message</div><p style="color:#f1f5f9;font-size:.85rem;line-height:1.6;margin:0;">{application["message"]}</p></div>' if application.get('message') else ''}

        <!-- CTA -->
        <div style="text-align:center;padding:20px 0 0;">
          <a href="tel:{application['phone']}"
             style="display:inline-block;padding:12px 32px;border-radius:99px;
                    background:#22d3ee;color:#06080f;font-size:.88rem;font-weight:800;
                    text-decoration:none;">
            📞 Call {application['phone']}
          </a>
        </div>

      </td></tr>

      <!-- footer -->
      <tr>
        <td style="padding:16px 32px;border-top:1px solid rgba(34,211,238,.08);
                   color:#475569;font-size:.72rem;text-align:center;">
          Sent automatically by Rewrite Academy · rewrite-academy.onrender.com
        </td>
      </tr>
    </table>
  </td></tr>
</table>
</body>
</html>"""

    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject_line
    msg['From']    = GMAIL_USER
    msg['To']      = ADMIN_EMAIL
    msg['Reply-To'] = application.get('email') or ADMIN_EMAIL

    msg.attach(MIMEText(plain, 'plain'))
    msg.attach(MIMEText(html,  'html'))

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
            server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
            server.sendmail(GMAIL_USER, ADMIN_EMAIL, msg.as_string())
        return True, ''
    except smtplib.SMTPAuthenticationError:
        return False, 'Gmail authentication failed. Check GMAIL_USER and GMAIL_APP_PASSWORD.'
    except Exception as e:
        return False, str(e)
