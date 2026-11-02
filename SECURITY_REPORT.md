\# CSRF Security Lab



\## 1. Project Overview

This project demonstrates Cross-Site Request Forgery (CSRF) using a local Flask application.



The application allows a logged-in user to change their account email address.



\## 2. Initial Vulnerability

The original application accepted email-change POST requests without requiring a CSRF token.



A test using Flask's test client confirmed that an authenticated request without a CSRF token was accepted and returned HTTP 302.



\## 3. Security Risk

An attacker could potentially trick an authenticated user into submitting an unwanted request.



Actual browser exploitability also depends on cookie settings and browser protections, including SameSite.



\## 4. Remediation

The application was updated to:

\- Generate unpredictable CSRF tokens using Python's secrets module.

\- Store the token in the user's session.

\- Include the token in the email-change form.

\- Validate the submitted token using secrets.compare\_digest().

\- Reject missing or invalid tokens with HTTP 403.



\## 5. Security Testing



| Test | Expected result | Actual result |

|---|---|---|

| Valid token | HTTP 302 | PASS |

| Missing token | HTTP 403 | PASS |

| Invalid token | HTTP 403 | PASS |

| Unauthenticated request | HTTP 401 | PASS |



\*\*Final result: 4/4 tests passed.\*\*



\## 6. Tools Used

\- Python

\- Flask

\- HTML forms

\- Flask test client

\- Command Prompt

\- Chrome Developer Tools



\## 7. Ethical Scope

All testing was conducted against a locally hosted training application using fictional accounts and data.

