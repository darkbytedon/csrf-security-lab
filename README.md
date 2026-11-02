\# CSRF Security Lab



A beginner-friendly cybersecurity project demonstrating Cross-Site Request Forgery (CSRF), its impact, remediation, and automated security testing.



\## Project Objective

Build a deliberately vulnerable Flask application, demonstrate that an email-change request can be accepted without a CSRF token, then implement token-based protection.



\## Technologies

\- Python

\- Flask

\- HTML

\- Git and GitHub



\## Vulnerability Demonstration

The original `/change-email` endpoint accepted authenticated POST requests without validating a CSRF token.



The initial test confirmed that a request without a token was accepted.



\## Security Fix

The application now:

1\. Generates a random CSRF token.

2\. Stores it in the user's session.

3\. Includes it in the email-change form.

4\. Validates the submitted token before changing the email.

5\. Rejects missing or invalid tokens.



\## Automated Tests

Run:



```bash

python test\_csrf.py

```



Expected result: \*\*4/4 security tests passed.\*\*



\## Project Files

\- `app.py` — Flask training application

\- `test\_csrf.py` — Automated security tests

\- `SECURITY\_REPORT.md` — Vulnerability analysis and remediation



\## Ethical Scope

This project uses a local application and fictional account data. It is intended for cybersecurity education.

