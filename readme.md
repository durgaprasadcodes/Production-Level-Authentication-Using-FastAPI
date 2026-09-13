# 🫆 Production-Grade Authentication System

A production-oriented authentication system built incrementally using:

- FastAPI
- React
- MySQL
- SQLAlchemy
- Alembic
- JWT
- HttpOnly Cookies
- Google OAuth 2.0
- Secure refresh-token rotation
- Email OTP verification

This project is being developed step by step to understand how a complete authentication architecture works from the database layer to production deployment.

---

## 🚀 Project Architecture

```text
                    ┌───────────────┐
                    │     React     │
                    └───────┬───────┘
                            │
              ┌─────────────┴─────────────┐
              │                           │
        Email/Password              Google OAuth
              │                           │
              └─────────────┬─────────────┘
                            ▼
                    ┌───────────────┐
                    │    FastAPI    │
                    └───────┬───────┘
                            │
                   Access + Refresh
                            │
                            ▼
                       ┌────────┐
                       │  MySQL │
                       └────────┘
```

---

## 📚 Development Roadmap

```
STEP 1  → FastAPI + MySQL connection
STEP 2  → User model + Alembic
STEP 3  → RefreshToken model + migration
STEP 4  → Password hashing + registration
STEP 5  → Email/password login
STEP 6  → Access JWT
STEP 7  → Refresh-token generation + secure storage
STEP 8  → /auth/refresh + token rotation
STEP 9  → Logout + revocation
STEP 10 → Protected endpoints
STEP 11 → Google OAuth
STEP 12 → Connect Google users to MySQL
STEP 13 → React authentication
STEP 14 → React token refresh/interceptor
STEP 15 → Production CORS/cookies/HTTPS
STEP 16 → Full authentication testing
STEP 17 → Production deployment
```

---

## 🗄️ Database Structure

### Users Table

```text
users

┌─────────────────────┐
│ id                  │
│ email               │
│ password_hash       │
│ google_id           │
│ name                │
│ picture             │
│ is_active           │
│ created_at          │
│ updated_at          │
└──────────┬──────────┘
           │
           │ 1 : many
           ▼
```

### Refresh Tokens Table

```text
refresh_tokens

┌─────────────────────────┐
│ id                      │
│ user_id                 │
│ token_hash              │
│ expires_at              │
│ created_at              │
│ revoked_at              │
│ replaced_by             │
└─────────────────────────┘
```

### Relationship

One user can have multiple refresh tokens.

```text
One User
   │
   ├── Refresh Token 1
   ├── Refresh Token 2
   └── Refresh Token 3
```

This supports multiple devices and sessions.

---

## 🔐 Authentication Strategy

The application uses:

```
Access Token  → Short-lived JWT
Refresh Token → Long-lived random token
```

Both tokens are stored in:

```
HttpOnly Cookies
```

The browser automatically sends the cookies with requests.
The frontend does not directly access the tokens using JavaScript.

### Access Token

The access token is a JWT containing information such as:

```json
{
  "sub": "user_id",
  "email": "user@example.com",
  "type": "access",
  "exp": "expiration_timestamp"
}
```

Used for accessing protected endpoints.

Example:

```
GET /user/me
```

### Refresh Token

Refresh tokens are:

- Cryptographically random
- Stored as hashes in MySQL
- Never stored in raw form
- Rotated after every refresh
- Revoked during logout

```text
Raw Refresh Token
       ↓
SHA-256 Hash
       ↓
Store Hash in MySQL
```

The raw refresh token is only sent to the browser through an HttpOnly cookie.

---

## 🔄 Refresh Token Rotation

```text
Client sends refresh token
          ↓
Backend hashes received token
          ↓
Find token hash in database
          ↓
Check expiration
          ↓
Check revoked_at
          ↓
Revoke old token
          ↓
Generate new refresh token
          ↓
Store new token hash
          ↓
Set new cookies
```

This prevents long-term reuse of the same refresh token.

---

## 🚪 Logout Flow

```text
User clicks Logout
        ↓
Backend reads refresh_token cookie
        ↓
Hashes refresh token
        ↓
Finds database record
        ↓
Marks token as revoked
        ↓
Deletes access_token cookie
        ↓
Deletes refresh_token cookie
```

Logout does not merely delete browser cookies. It also revokes the refresh token on the server.

---

## 🛡️ Protected Endpoints

Protected endpoints require a valid access token.

Example:

```
GET /user/me
```

Flow:

```text
Request
   ↓
Read access_token from HttpOnly cookie
   ↓
Decode JWT
   ↓
Validate signature
   ↓
Validate expiration
   ↓
Validate token type
   ↓
Get user ID
   ↓
Fetch user
   ↓
Return protected data
```

---

## 🌐 Google OAuth Login

### Basic Google Login Flow

```text
Google Login
     ↓
Google OAuth
     ↓
Get Google identity
     ↓
Find/Create User in MySQL
     ↓
Generate YOUR access token
     ↓
Generate YOUR refresh token
     ↓
HttpOnly cookies
     ↓
/user/me
```

Google is used only to verify the user's identity.

The application still generates and manages its own:

- Access token
- Refresh token
- Sessions
- Cookies
- Database records

Google tokens are not used as the application's own access tokens.

---

## 🔎 Google OAuth Account Decision Flow

```text
Continue with Google
        |
        v
Google OAuth callback
        |
        v
Is Google email verified?
        |
        ├── No → Reject
        |
        └── Yes
              |
              v
       Does google_id exist?
              |
              ├── Yes → Login
              |
              └── No
                    |
                    v
             Does email exist?
                    |
                    ├── No
                    |    → Create Google user
                    |    → Login
                    |
                    └── Yes
                         → Send OTP
                         → Pending linking state
                         → Verify OTP
                         → Link Google ID
                         → Login
```

---

## 👤 Google User Cases

The system handles the following cases:

### Case 1 — Existing Google User

```text
Google ID exists in database
        ↓
Find user using google_id
        ↓
Generate access token
        ↓
Generate refresh token
        ↓
Set cookies
        ↓
Login successful
```

### Case 2 — New Google User

```text
Google ID does not exist
        ↓
Email does not exist
        ↓
Create new user
        ↓
Store:
    - name
    - email
    - google_id
    - picture
    - password = NULL
        ↓
Generate tokens
        ↓
Login successful
```

### Case 3 — Existing Email/Password User

```text
User registered using email/password
        ↓
Tries Google login with same email
        ↓
Google ID does not exist in DB
        ↓
Email already exists in DB
        ↓
Do not automatically link accounts
        ↓
Send OTP to existing email
```

This prevents unauthorized account linking.

---

## 🔗 Google Account Linking with OTP

```text
User registered using email/password
            ↓
Tries Google login with same email
            ↓
Google ID does not exist in DB
            ↓
Email already exists in DB
            ↓
Generate OTP
            ↓
Send OTP to that email
            ↓
Create pending linking state
            ↓
Redirect user to React /verify-otp page
            ↓
User enters OTP
            ↓
React sends OTP to FastAPI
            ↓
FastAPI verifies OTP
            ↓
OTP correct?
       ├── No → Reject
       └── Yes
             ↓
      Link Google ID
             ↓
      Generate access token
             ↓
      Generate refresh token
             ↓
      Set HttpOnly cookies
             ↓
      Login successful
```

---

## ✉️ Email OTP System

For the current testing implementation, OTPs use temporary in-memory storage.

This is intentionally being used only for development/testing.

```text
Generate OTP
     ↓
Store OTP temporarily
     ↓
Set 60-second expiry
     ↓
Send OTP through email
     ↓
User enters OTP
     ↓
Verify OTP
     ↓
Delete OTP after successful verification
```

Example temporary storage:

```python
otp_store[email] = {
    "otp": otp,
    "google_id": google_id,
    "expires_at": time.time() + 60
}
```

OTP generation uses Python's `secrets` module:

```python
import secrets

otp = str(secrets.randbelow(1000000)).zfill(6)
```

### Current Testing Limitation

In-memory OTP storage:

- Is lost when the server restarts
- Is not suitable for multiple backend instances
- Is not production-ready
- Is being used only to complete and test Google OAuth

For production systems, Redis with TTL will be used later.

---

## 📧 Email Sending

Email is sent using SMTP through `aiosmtplib`.

The email service supports:

- Plain-text emails
- HTML emails
- OTP emails
- Password reset emails
- Verification emails

Example HTML email structure:

```python
message.set_content(plain_body)
message.add_alternative(html_body, subtype="html")
```

SMTP credentials are stored in `.env`.

```env
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_google_app_password
MAIL_FROM=your_email@gmail.com
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
```

---

## 🧭 Frontend OTP Flow

The frontend contains a route such as:

```
/verify-otp
```

Flow:

```text
Google callback
      ↓
OTP sent
      ↓
Redirect:
http://localhost:5173/verify-otp
      ↓
User enters OTP
      ↓
POST /auth/google/verify-otp
      ↓
Backend validates OTP
      ↓
Google ID linked
      ↓
Authentication cookies created
      ↓
Redirect to dashboard
```

Opening `/verify-otp` manually should not grant access.

The backend must verify that an active OTP verification session exists.

```text
No pending OTP session
        ↓
Reject verification request
```

---

## 🔒 Security Considerations

Important security principles used in this project:

- Passwords are hashed using `pwdlib`
- Raw refresh tokens are never stored in MySQL
- Refresh tokens are hashed using SHA-256
- Refresh tokens are rotated
- Revoked refresh tokens cannot be reused
- Access tokens are short-lived
- Tokens are stored in HttpOnly cookies
- Google email verification is checked
- Existing accounts are not automatically linked
- OTP is required for account linking
- OTP has a limited lifetime
- OTP is deleted after successful verification
- Sensitive credentials are stored in `.env`
- Google OAuth credentials are never exposed to React
- Production cookies will use HTTPS and Secure flags
- CORS will be restricted to trusted frontend origins

---

## 🧪 Testing Checklist

### Email/Password Authentication

- [X] Register new user
- [x] Reject duplicate email
- [x] Reject incorrect password
- [x] Login successfully
- [x] Access protected endpoint
- [x] Reject missing access token
- [x] Refresh access token
- [x] Rotate refresh token
- [x] Reject reused refresh token
- [x] Logout successfully
- [x] Reject revoked refresh token


### Google OAuth

- [x] Login with new Google account
- [x] Create Google user in MySQL
- [x] Login with existing Google user
- [x] Reject unverified Google email
- [x] Detect existing email/password account
- [x] Send OTP
- [x] Redirect to frontend OTP page
- [x] Reject incorrect OTP
- [x] Reject expired OTP
- [x] Verify correct OTP
- [x] Link Google ID
- [x] Login after successful linking
- [x] Confirm access/refresh cookies
- [x] Confirm /user/me

---

## 🏗️ Future Production Improvements

The current testing implementation will later be upgraded with:

- Redis OTP storage with TTL
- OTP rate limiting
- OTP attempt limits
- OTP resend cooldown
- CSRF protection
- Secure cookie configuration
- HTTPS
- Strict production CORS
- Better email provider
- Structured logging
- Error monitoring
- Automated tests
- Docker deployment
- CI/CD
- Production database configuration
- Deployment on Render/Vercel

---

## 🎯 Project Goal

The goal is not just to make login work.

The goal is to understand and implement a complete authentication architecture involving:

```text
Database Design
      ↓
Password Security
      ↓
JWT Authentication
      ↓
Refresh Token Security
      ↓
Session Revocation
      ↓
Google OAuth
      ↓
Account Linking
      ↓
OTP Verification
      ↓
React Integration
      ↓
Production Security
      ↓
Deployment
```

This project is being built incrementally, with each authentication concept implemented, tested, and understood before moving to the next stage.
