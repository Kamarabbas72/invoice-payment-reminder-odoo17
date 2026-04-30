{
    'name': 'Invoice Payment Reminder',
    'version': '17.0.1.0.0',
    'summary': 'Automatically sends payment reminders for overdue invoices at 7, 15, and 30 days',
    'author': 'Kamarabbas Bukhari',
    'category': 'Accounting',
    'depends': ['account', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/mail_template.xml',
        'data/cron.xml',
        'views/account_move_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
