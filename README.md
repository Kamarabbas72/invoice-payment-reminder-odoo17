# Invoice Payment Reminder — Odoo 17

A custom Odoo 17 addon that automatically sends payment reminder emails to customers when invoices become overdue. Three escalating reminder levels at 7, 15, and 30 days, powered by a daily scheduled action with full chatter logging and audit trail.

![Odoo Version](https://img.shields.io/badge/Odoo-17.0-blue)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![License](https://img.shields.io/badge/License-LGPL--3-green)
![Category](https://img.shields.io/badge/Category-Accounting-orange)

---

## Features

### Three-Level Automated Reminders
Overdue invoices automatically trigger escalating email reminders based on how many days past due:

| Days Overdue | Reminder Level | Email Tone |
|-------------|---------------|------------|
| 7+ days | Level 1 | Friendly reminder |
| 15+ days | Level 2 | Second notice, firmer |
| 30+ days | Level 3 | Final notice, urgent |

Each level sends only once — the module tracks which reminders have already been sent using boolean flags on the invoice, preventing duplicate emails.

### Daily Scheduled Action
An `ir.cron` scheduled action runs every day and automatically processes all overdue posted invoices, checking which reminder level is due and sending the appropriate email.

### Live Overdue Indicators
Two computed fields appear directly on the invoice form and list view:
- **Days Overdue** — real-time count of days past the due date
- **Reminder Level** — badge indicator showing current escalation level (colour-coded: warning for Level 1, danger for Level 2 and 3)

### Chatter Logging
Every reminder email sent is logged in the invoice chatter with the reminder level and timestamp — full audit trail of all customer communications.

### Three Email Templates
Separate `mail.template` records for each reminder level with appropriate subject lines and message content. All templates are customisable directly from the Odoo interface.

---

## Module Structure

```
invoice_payment_reminder/
├── __init__.py
├── __manifest__.py               # depends on account, mail
├── models/
│   ├── __init__.py
│   └── account_move.py           # Extends account.move with reminder fields and logic
├── data/
│   ├── mail_template.xml         # 3 email templates (7-day, 15-day, 30-day)
│   └── cron.xml                  # Daily scheduled action
├── views/
│   └── account_move_views.xml    # Inherits invoice form and list views
└── security/
    └── ir.model.access.csv       # Access rights
```

---

## Technical Highlights

- `_inherit` on `account.move` — non-destructive extension of Odoo's core accounting model
- `@api.depends('invoice_date_due', 'payment_state')` computed field for real-time overdue calculation
- `ir.cron` scheduled action calling a custom `@api.model` method daily
- Three separate `mail.template` records with appropriate escalation messaging
- Boolean tracking fields (`reminder_sent_7`, `reminder_sent_15`, `reminder_sent_30`) prevent duplicate sends
- `message_post()` integration for full chatter audit trail
- View inheritance using `xpath` on Odoo 17 invoice form and list views
- `widget="badge"` with `decoration-warning` and `decoration-danger` for visual indicators

---

## How It Works

1. Daily cron job searches all posted, unpaid invoices with a past due date
2. For each invoice, calculates days overdue using `(today - invoice_date_due).days`
3. Checks which reminder level is due and whether it has already been sent
4. Sends the appropriate email template via `template.send_mail()`
5. Sets the boolean flag to prevent duplicate sends
6. Logs the action in the invoice chatter

---

## Installation

1. Clone this repository into your Odoo custom addons directory:
   ```bash
   git clone https://github.com/Kamarabbas72/invoice-payment-reminder-odoo17.git
   ```

2. Add the path to your `odoo.conf`:
   ```ini
   addons_path = /path/to/odoo/addons,/path/to/your/custom/addons
   ```

3. Restart Odoo and install:
   ```bash
   python odoo-bin -c odoo.conf -u invoice_payment_reminder -d your_database
   ```

4. Go to **Apps** → search `Invoice Payment Reminder` → **Install**

---

## Requirements

- Odoo 17.0
- Python 3.10+
- Depends on: `account`, `mail`

---

## Roadmap

- [ ] Configurable reminder days via Settings UI (instead of hardcoded 7/15/30)
- [ ] Reminder report — summary of all overdue invoices and reminder status
- [ ] Pause reminders per customer or per invoice
- [ ] SMS reminder integration using Odoo SMS gateway
- [ ] Dashboard widget showing overdue invoice statistics

---

## Author

**Kamarabbas Bukhari** — Odoo ERP Developer

- GitHub: [github.com/Kamarabbas72](https://github.com/Kamarabbas72)
- LinkedIn: [linkedin.com/in/kamarabbas-bukhari-2522981b1](https://linkedin.com/in/kamarabbas-bukhari-2522981b1)
- Email: fardeenbukhari313@gmail.com
