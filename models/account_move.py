from odoo import models, fields, api
from datetime import date


class AccountMove(models.Model):
    _inherit = 'account.move'

    reminder_sent_7 = fields.Boolean(
        string='7-Day Reminder Sent',
        default=False,
        copy=False,
    )
    reminder_sent_15 = fields.Boolean(
        string='15-Day Reminder Sent',
        default=False,
        copy=False,
    )
    reminder_sent_30 = fields.Boolean(
        string='30-Day Reminder Sent',
        default=False,
        copy=False,
    )
    days_overdue = fields.Integer(
        string='Days Overdue',
        compute='_compute_days_overdue',
        store=False,
    )
    reminder_level = fields.Selection([
        ('none', 'Not Overdue'),
        ('level_1', 'Level 1 — 7 Days'),
        ('level_2', 'Level 2 — 15 Days'),
        ('level_3', 'Level 3 — 30 Days'),
    ], string='Reminder Level',
       compute='_compute_reminder_level',
       store=False,
    )

    @api.depends('invoice_date_due', 'payment_state')
    def _compute_days_overdue(self):
        today = date.today()
        for move in self:
            if (
                move.move_type == 'out_invoice'
                and move.payment_state not in ('paid', 'in_payment')
                and move.invoice_date_due
                and move.state == 'posted'
            ):
                delta = (today - move.invoice_date_due).days
                move.days_overdue = max(delta, 0)
            else:
                move.days_overdue = 0

    @api.depends('days_overdue')
    def _compute_reminder_level(self):
        for move in self:
            if move.days_overdue >= 30:
                move.reminder_level = 'level_3'
            elif move.days_overdue >= 15:
                move.reminder_level = 'level_2'
            elif move.days_overdue >= 7:
                move.reminder_level = 'level_1'
            else:
                move.reminder_level = 'none'

    @api.model
    def send_payment_reminders(self):
        """
        Scheduled action — runs daily.
        Sends reminder emails at 7, 15, and 30 days overdue.
        """
        today = date.today()
        overdue_invoices = self.search([
            ('move_type', '=', 'out_invoice'),
            ('state', '=', 'posted'),
            ('payment_state', 'not in', ['paid', 'in_payment']),
            ('invoice_date_due', '<', fields.Date.today()),
        ])

        for invoice in overdue_invoices:
            days = (today - invoice.invoice_date_due).days

            if days >= 30 and not invoice.reminder_sent_30:
                template = self.env.ref(
                    'invoice_payment_reminder.email_template_reminder_30',
                    raise_if_not_found=False
                )
                if template:
                    template.send_mail(invoice.id, force_send=True)
                invoice.reminder_sent_30 = True
                invoice.message_post(
                    body='30-day overdue payment reminder sent to customer.',
                    subtype_xmlid='mail.mt_note',
                )

            elif days >= 15 and not invoice.reminder_sent_15:
                template = self.env.ref(
                    'invoice_payment_reminder.email_template_reminder_15',
                    raise_if_not_found=False
                )
                if template:
                    template.send_mail(invoice.id, force_send=True)
                invoice.reminder_sent_15 = True
                invoice.message_post(
                    body='15-day overdue payment reminder sent to customer.',
                    subtype_xmlid='mail.mt_note',
                )

            elif days >= 7 and not invoice.reminder_sent_7:
                template = self.env.ref(
                    'invoice_payment_reminder.email_template_reminder_7',
                    raise_if_not_found=False
                )
                if template:
                    template.send_mail(invoice.id, force_send=True)
                invoice.reminder_sent_7 = True
                invoice.message_post(
                    body='7-day overdue payment reminder sent to customer.',
                    subtype_xmlid='mail.mt_note',
                )
