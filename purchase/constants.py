class Status:
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELED = "canceled"
    as_choices = ((PENDING, PENDING), (COMPLETED, COMPLETED), (CANCELED, CANCELED))
