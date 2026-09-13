
```text
STEP 1 → FastAPI + MySQL connection                 
STEP 2 → User model + Alembic                       
STEP 3 → RefreshToken model + migration
STEP 4 → Password hashing + registration
STEP 5 → Email/password login
STEP 6 → Access JWT
STEP 7 → Refresh-token generation + secure storage
STEP 8 → /auth/refresh + token rotation
STEP 9 → Logout + revocation
STEP 10 → Protected endpoints
STEP 11 → Google OAuth
STEP 12 → Connect Google users to MySQL
STEP 13 → React authentication
STEP 14 → React token refresh/interceptor
STEP 15 → Production CORS/cookies/HTTPS
STEP 16 → Full authentication testing
STEP 17 → Production deployment

```

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
                       │ MySQL  │
                       └────────┘

```

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

## Step 11 — Google Login FLow

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

###  we will handle the important cases:

- Existing Google user
- New Google user
- Existing email/password user
- Account linking
- google_id
- Profile picture
- Access/refresh cookies
- Refresh rotation
- Logout
- Security considerations

### Is User Prevouly Logged with Email & Password Intsead of Google SignIn
```text
User registered using email/password
            ↓
Tries Google login with same email
            ↓
Google ID does not exist in DB
            ↓
Email already exists in DB
            ↓
Send OTP to that email
            ↓
Verify OTP
            ↓
Link Google account safely
            ↓
Login
```