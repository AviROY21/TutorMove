# TutorMove

This repository contains a minimal prototype for a tutor marketplace platform inspired by TeacherOn. It demonstrates basic user registration, email OTP verification, and login functionality using only Python's standard library.

## Running the server

```bash
python3 -m backend.main
```

The server exposes the following endpoints:

- `POST /register` – parameters: `username`, `email`, `phone`, `password`, `role`
- `POST /verify-email` – parameters: `user_id`, `code`
- `POST /login` – parameters: `username`, `password`

All data is stored in `backend/tutormove.db` (SQLite).

This is only a starting point. The detailed project scope includes additional features such as gig management, credit system, job postings, messaging, escrow payments, and more. Those components would need to be implemented on top of this minimal foundation.
