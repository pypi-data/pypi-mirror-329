from python_sdk_remote.our_object import OurObject


class Contact(OurObject):
    def __init__(self, **kwargs):
        contact_fields = {
            "first_name",
            "last_name",
            "birthday",
            "job_title",
            "organization",
            "organization_profile_id",
            "owner_profile_id",
            "account_name",
            "person_id",
            "name_prefix",
            "additional_name",
            "full_name",
            "name_suffix",
            "nickname",
            "display_as",
            "title",
            "department",
            "notes",
            "email1",
            "email2",
            "email3",
            "phone1",
            "phone2",
            "phone3",
            "address1_street",
            "address1_city",
            "address1_state",
            "address1_postal_code",
            "address1_country",
            "address2_street",
            "address2_city",
            "address2_state",
            "address2_postal_code",
            "address2_country",
            "day",
            "month",
            "year",
            "cira",
            "anniversary",
            "website1",
            "website2",
            "website3",
            "photo_url",
            "photo_file_name",
            "source",
        }

        # TODO EmailAddressesLocal.process_email_address( email_address )
        #
        # TODO Can we make it generic in python-sdk repo?
        for field, value in kwargs.items():
            if field in contact_fields:
                setattr(self, field, value)

    def get_name(self):
        return self.first_name + " " + self.last_name

    def __str__(self):
        return "Contact: " + str(self.__dict__)

    def __repr__(self):
        return "Contact: " + str(self.__dict__)

    def to_dict(self):
        return self.__dict__
