class ExpenseImportSourceEnum:
    """
    Enum for Expense Import Source
    """
    WEBHOOK = 'WEBHOOK'
    DASHBOARD_SYNC = 'DASHBOARD_SYNC'
    DIRECT_EXPORT = 'DIRECT_EXPORT'
    BACKGROUND_SCHEDULE = 'BACKGROUND_SCHEDULE'


class ExpenseStateEnum:
    """
    Enum for Expense State
    """
    PAYMENT_PROCESSING = 'PAYMENT_PROCESSING'
    PAID = 'PAID'
    APPROVED = 'APPROVED'
