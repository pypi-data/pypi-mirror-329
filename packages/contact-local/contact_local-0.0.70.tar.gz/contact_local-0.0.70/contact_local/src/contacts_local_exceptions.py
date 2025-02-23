class ContactsLocalException(Exception):
    """Base class for ContactsLocal exceptions."""

    def __init__(self, message="ContactsLocal error occurred."):
        self.message = message
        super().__init__(self.message)


class ContactInsertionException(ContactsLocalException):
    """Exception raised for errors related to inserting contacts."""

    def __init__(self, message="Error occurred while inserting contact."):
        super().__init__(message)


class ContactUpdateException(ContactsLocalException):
    """Exception raised for errors related to updating contacts."""

    def __init__(self, message="Error occurred while updating contact."):
        super().__init__(message)


class ContactDeletionException(ContactsLocalException):
    """Exception raised for errors related to deleting contacts."""

    def __init__(self, message="Error occurred while deleting contact."):
        super().__init__(message)


class ContactBatchInsertionException(ContactsLocalException):
    """Exception raised for errors related to batch insertion of contacts."""

    def __init__(self, message="Error occurred while batch inserting contacts."):
        super().__init__(message)


class ContactRetrievalException(ContactsLocalException):
    """Exception raised for errors related to retrieving contacts."""

    def __init__(self, message="Error occurred while retrieving contact."):
        super().__init__(message)


class ContactObjectInsertionException(ContactsLocalException):
    """Exception raised for errors related to inserting contact objects."""

    def __init__(self, message="Error occurred while inserting contact object."):
        super().__init__(message)
