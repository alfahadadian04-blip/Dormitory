# DORM — Dormitory Management System

A clean, minimalist dormitory management system built with **Flask** and **Supabase (PostgreSQL)**. Brown / black / white theme, responsive layout, and fully working CRUD, payments, reports and Excel export.

## Features

- Admin authentication (Flask-Login)
- Dashboard with live stats: total tenants, active tenants, monthly income, unpaid/overdue counts
- Tenant CRUD (nickname, full name, room, contact, move-in, rent, due day, balance, status)
- Payment recording with automatic balance & status updates
- Payment history with per-tenant filter
- Reports page + Excel exports (`.xlsx`) for tenants and payments
- Live overdue badge that auto-refreshes every 30 seconds
- Responsive UI (desktop / tablet / mobile) with sidebar, spinners, empty states, flash messages

## Project structure

```
DORM/
├─ app.py
├─ config.py
├─ models.py
├─ routes.py
├─ auth.py
├─ requirements.txt
├─ .env.example
├─ templates/
│  ├─ base.html
│  ├─ login.html
│  ├─ dashboard.html
│  ├─ tenants.html
│  ├─ tenant_form.html
│  ├─ tenant_detail.html
│  ├─ payments.html
│  ├─ payment_form.html
│  ├─ reports.html
│  └─ error.html
└─ static/
   └─ css/
      └─ style.css
```

## Requirements

- Python 3.10+
- A Supabase project (or any PostgreSQL database)

## Setup

1. **Clone / open** this folder.
2. **Create a virtual environment** and install dependencies:

   ```bash
   python -m venv .venv
   # Windows PowerShell
   .venv\Scripts\Activate.ps1
   # macOS / Linux
   source .venv/bin/activate

   pip install -r requirements.txt
   ```

3. **Configure environment variables**. Copy `.env.example` to `.env` and edit:

   ```env
   DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@db.YOUR_PROJECT.supabase.co:5432/postgres
   SECRET_KEY=some-long-random-string
   ```

   You can grab the Supabase connection string from your project dashboard under **Project Settings → Database → Connection string (URI)**. If it starts with `postgres://`, the app automatically converts it to `postgresql://` for SQLAlchemy compatibility.

4. **Run the app**:

   ```bash
   python app.py
   ```

   Open [http://localhost:5000](http://localhost:5000).

5. **Log in** with the default credentials (auto-seeded on first run):

   - Username: `adian`
   - Password: `adian123`

   > Change the password by creating a new admin user or updating directly in the database. You can also override defaults via `DEFAULT_ADMIN_USERNAME` / `DEFAULT_ADMIN_PASSWORD` env vars before first run.

## How it works

- **Tables** (`tenants`, `payments`, `admins`) are auto-created on first launch using `db.create_all()`.
- **Recording a payment** subtracts the amount from `tenants.pending_balance` automatically. Deleting a payment restores the balance.
- A tenant is considered **overdue** when: `status = active`, `pending_balance > 0`, and today's day of month is past the tenant's `due_day`.
- The sidebar and top bar show a **live overdue badge** that polls `/api/notifications` every 30s.
- **Excel exports** (`openpyxl`) are available at:
  - `/export/tenants.xlsx`
  - `/export/payments.xlsx`

## Security notes

- All sensitive values come from environment variables — nothing is hard-coded.
- Passwords are stored hashed via `werkzeug.security`.
- All app routes are protected with `@login_required` except `/login`.
- Supabase pool is configured with `pool_pre_ping` + `pool_recycle=300` to keep long-running connections healthy.

## Troubleshooting

- **`sqlalchemy.exc.OperationalError` / cannot connect to Supabase** — double-check the `DATABASE_URL`, IPv4/IPv6 settings in Supabase, and that your password is URL-encoded if it contains special characters.
- **`dialect` errors** — make sure the URL starts with `postgresql://`, not `postgres://` (the app auto-fixes this, but verify).
- **Default admin not created** — it's only seeded when the `admins` table is empty; delete the row or update the password manually if needed.

## License

MIT — use it freely for your dormitory.
