from multidict import MultiDict
from typing import List, Dict
from logger_local.MetaLogger import MetaLogger

from database_mysql_local.connector import Connector
from person_local.persons_local import PersonsLocal
from people_local.people import PeopleLocal

from .contact import Contact
from .contact_constants import (
    SCHEMA_NAME,
    CONTACT_TABLE_NAME,
    CONTACT_VIEW_TABLE_NAME,
    CONTACT_ID_COLUMN_NAME,
    GOOGLE_CONTACT_PEOPLE_API_DATA_SOURCE_TYPE_ID,
    logger,
)
from .contacts_local_exceptions import (
    ContactBatchInsertionException,
    ContactDeletionException,
    ContactInsertionException,
    ContactObjectInsertionException,
    ContactUpdateException,
)


class ContactsLocal(PeopleLocal, metaclass=MetaLogger):

    def __init__(self, contact_dict: dict = None, is_test_data: bool = False) -> None:
        details_for_people_local = (
            self.__get_details_for_people_local_from_contact_dict(
                contact_dict=contact_dict
            )
        )
        (
            first_name_original,
            last_names_original,
            organizations_names_original,
            email_addresses,
        ) = details_for_people_local

        PeopleLocal.__init__(
            self,
            default_schema_name=SCHEMA_NAME,
            default_table_name=CONTACT_TABLE_NAME,
            default_view_table_name=CONTACT_VIEW_TABLE_NAME,
            default_column_name=CONTACT_ID_COLUMN_NAME,
            first_name_original=first_name_original,
            last_names_original=last_names_original,
            organizations_names_original=organizations_names_original,
            email_addresses=email_addresses,
            is_test_data=is_test_data,
        )

    def insert_contact_dict(
        self, contact_dict: dict, ignore_duplicate: bool = False
    ) -> int:
        logger.start(
            object={
                "contact_to_insert": contact_dict,
                "ignore_duplicate": ignore_duplicate,
            }
        )
        if not contact_dict:
            logger.error("contact_to_insert cannot be empty")
            logger.end()
            raise ContactInsertionException("contact_to_insert cannot be empty")

        processed_contact_info_details_dict = self.__process_contact_info_details(
            contact_dict
        )
        contact_id = None
        try:
            contact_dict = {
                "owner_profile_id": contact_dict.get("owner_profile_id", None),
                "data_source_instance_id": contact_dict.get(
                    "data_source_instance_id", None
                ),
                "account_name": contact_dict.get("account_name", None),
                "person_id": contact_dict.get("person_id", None),
                "name_prefix": contact_dict.get("name_prefix", None),
                "first_name": (
                    self.normalized_first_name
                    if self.normalized_first_name
                    else contact_dict.get("first_name")
                ),
                "original_first_name": (
                    self.first_name_original
                    if self.first_name_original
                    else contact_dict.get("first_name")
                ),
                "additional_name": contact_dict.get("additional_name", None),
                "last_name": (
                    self.normalized_last_names[0]
                    if self.normalized_last_names
                    else contact_dict.get("last_name")
                ),
                "original_last_name": (
                    self.last_names_original[0] if self.last_names_original else None
                ),
                "full_name": contact_dict.get("full_name", None),
                "name_suffix": contact_dict.get("name_suffix", None),
                "nickname": contact_dict.get("nickname", None),
                "display_as": contact_dict.get("display_as", None),
                "title": contact_dict.get("title", None),
                "organization": contact_dict.get("organization", None),
                "organization_profile_id": contact_dict.get(
                    "organization_profile_id", None
                ),
                "job_title": contact_dict.get("job_title", None),
                "department": contact_dict.get("department", None),
                "notes": contact_dict.get("notes", None),
                "email1": processed_contact_info_details_dict.get("email_addresses"),
                "email2": contact_dict.get("email2", None),
                "email3": contact_dict.get("email3", None),
                "phone1": contact_dict.get("phone1", None),
                "phone2": contact_dict.get("phone2", None),
                "phone3": contact_dict.get("phone3", None),
                "address1_street": contact_dict.get("address1_street", None),
                "address1_city": contact_dict.get("address1_city", None),
                "address1_state": contact_dict.get("address1_state", None),
                "address1_postal_code": contact_dict.get("address1_postal_code", None),
                "address1_country": contact_dict.get("address1_country", None),
                "address2_street": contact_dict.get("address2_street", None),
                "address2_city": contact_dict.get("address2_city", None),
                "address2_state": contact_dict.get("address2_state", None),
                "address2_postal_code": contact_dict.get("address2_postal_code", None),
                "address2_country": contact_dict.get("address2_country", None),
                "birthday": contact_dict.get("birthday", None),
                "day": contact_dict.get("day", None),
                "month": contact_dict.get("month", None),
                "year": contact_dict.get("year", None),
                "cira": contact_dict.get("cira", None),
                "anniversary": contact_dict.get("anniversary", None),
                "website1": (
                    processed_contact_info_details_dict.get("urls")[0]
                    if processed_contact_info_details_dict.get("urls")
                    else None
                ),
                "website2": contact_dict.get("website2", None),
                "website3": contact_dict.get("website3", None),
                "photo_url": contact_dict.get("photo_url", None),
                "photo_file_name": contact_dict.get("photo_file_name", None),
                "source": contact_dict.get("source", None),
            }
            if contact_dict.get("display_as", None) is None:
                contact_dict["display_as"] = contact_dict.get(
                    "original_first_name", None
                )
                if contact_dict.get("original_last_name", None) is not None:
                    contact_dict["display_as"] += " " + contact_dict.get(
                        "original_last_name", ""
                    )
            if contact_dict.get("full_name") is None:
                contact_dict["full_name"] = contact_dict.get("first_name")
                if contact_dict.get("last_name") is not None:
                    contact_dict["full_name"] += " " + contact_dict.get("last_name")
            contact_id = self.insert(
                data_dict=contact_dict, ignore_duplicate=ignore_duplicate
            )
            logger.end("contact added", object={"contact_id": contact_id})
        except Exception as exception:
            logger.error(
                f"Contact.insert Exception: {exception}",
                object={"exception": exception},
            )
            logger.end()
            raise ContactInsertionException(
                "Exception occurred while inserting contact." + str(exception)
            )

        return contact_id

    # Warning! be careful when using data_dict_compare, it's recommended to leave it None if possible
    def upsert_contact_dict(
        self, contact_dict: dict, data_dict_compare: dict = None
    ) -> int:
        UPSERT_CONTACT_DICT_METHOD_NAME = "upsert_contact_dict"
        logger.start(
            UPSERT_CONTACT_DICT_METHOD_NAME,
            object={
                "contact_dict": contact_dict,
                "data_dict_compare": data_dict_compare,
            },
        )
        try:
            contact_row_dict = self.upsert_contact_dict_with_return_dict(
                contact_dict=contact_dict,
                data_dict_compare=data_dict_compare,
                select_clause_value="contact_id",
            )
            contact_id = contact_row_dict["contact_id"]
            if contact_id is None:
                raise ContactInsertionException(
                    "contact_id is None after upserting contact_dict"
                )
        except Exception as exception:
            logger.error(
                f"Contact.insert Exception: {exception}",
                object={"exception": exception},
            )
            raise ContactInsertionException(
                "Exception occurred while inserting contact." + str(exception)
            )
        logger.end("contact added", object={"contact_id": contact_id})
        return contact_id

    # Warning! be careful when using data_dict_compare, it's recommended to leave it None if possible
    def upsert_contact_dict_with_return_dict(
        self,
        contact_dict: dict,
        data_dict_compare: dict = None,
        select_clause_value: str = "*",
    ) -> dict:
        UPSERT_CONTACT_DICT_METHOD_NAME = "upsert_contact_dict_with_return_dict"
        logger.start(
            UPSERT_CONTACT_DICT_METHOD_NAME,
            object={
                "contact_dict": contact_dict,
                "data_dict_compare": data_dict_compare,
            },
        )
        if not contact_dict:
            logger.error("contact_dict cannot be empty")
            logger.end()
            raise ContactInsertionException("contact_dict cannot be empty")
        if data_dict_compare is None:
            data_dict_compare = self.__get_data_dict_compare_for_upsert_contact_dict(
                contact_dict
            )
        if "contact_id" in data_dict_compare:
            where_compare = params_compare = None
        else:
            where_compare, params_compare = self.__get_where_compare_and_params(
                contact_dict
            )
        process_contact_info_details_dict = self.__process_contact_info_details(
            contact_dict
        )

        contact_id = None
        try:
            contact_dict = {
                "owner_profile_id": contact_dict.get("owner_profile_id", None),
                "data_source_instance_id": contact_dict.get(
                    "data_source_instance_id", None
                ),
                "account_name": contact_dict.get("account_name", None),
                "person_id": contact_dict.get("person_id", None),
                "name_prefix": contact_dict.get("name_prefix", None),
                "first_name": (
                    self.normalized_first_name
                    if self.normalized_first_name
                    else contact_dict.get("first_name")
                ),
                "original_first_name": (
                    self.first_name_original
                    if self.first_name_original
                    else contact_dict.get("first_name")
                ),
                "additional_name": contact_dict.get("additional_name", None),
                "last_name": (
                    self.normalized_last_names[0]
                    if self.normalized_last_names
                    else contact_dict.get("last_name")
                ),
                "original_last_name": (
                    self.last_names_original[0] if self.last_names_original else None
                ),
                "full_name": contact_dict.get("full_name", None),
                "name_suffix": contact_dict.get("name_suffix", None),
                "nickname": contact_dict.get("nickname", None),
                "display_as": contact_dict.get("display_as", None),
                "title": contact_dict.get("title", None),
                "organization": contact_dict.get("organization", None),
                "organization_profile_id": contact_dict.get(
                    "organization_profile_id", None
                ),
                "job_title": contact_dict.get("job_title", None),
                "department": contact_dict.get("department", None),
                "notes": contact_dict.get("notes", None),
                "email1": process_contact_info_details_dict.get("email_addresses"),
                "email2": contact_dict.get("email2", None),
                "email3": contact_dict.get("email3", None),
                "phone1": contact_dict.get("phone1", None),
                "phone2": contact_dict.get("phone2", None),
                "phone3": contact_dict.get("phone3", None),
                "address1_street": contact_dict.get("address1_street", None),
                "address1_city": contact_dict.get("address1_city", None),
                "address1_state": contact_dict.get("address1_state", None),
                "address1_postal_code": contact_dict.get("address1_postal_code", None),
                "address1_country": contact_dict.get("address1_country", None),
                "address2_street": contact_dict.get("address2_street", None),
                "address2_city": contact_dict.get("address2_city", None),
                "address2_state": contact_dict.get("address2_state", None),
                "address2_postal_code": contact_dict.get("address2_postal_code", None),
                "address2_country": contact_dict.get("address2_country", None),
                "birthday": contact_dict.get("birthday", None),
                "day": contact_dict.get("day", None),
                "month": contact_dict.get("month", None),
                "year": contact_dict.get("year", None),
                "cira": contact_dict.get("cira", None),
                "anniversary": contact_dict.get("anniversary", None),
                "website1": (
                    process_contact_info_details_dict.get("urls")[0]
                    if process_contact_info_details_dict.get("urls")
                    else None
                ),
                "website2": contact_dict.get("website2", None),
                "website3": contact_dict.get("website3", None),
                "photo_url": contact_dict.get("photo_url", None),
                "photo_file_name": contact_dict.get("photo_file_name", None),
                "source": contact_dict.get("source", None),
            }
            if contact_dict.get("display_as", None) is None:
                contact_dict["display_as"] = contact_dict.get(
                    "original_first_name", None
                )
                if contact_dict.get("original_last_name", None) is not None:
                    contact_dict["display_as"] += " " + contact_dict.get(
                        "original_last_name", ""
                    )
            if contact_dict.get("full_name") is None:
                contact_dict["full_name"] = contact_dict.get("first_name")
                if contact_dict.get("last_name") is not None:
                    contact_dict["full_name"] += " " + contact_dict.get("last_name")
            contact_row_dict = self.upsert_with_select_clause(
                data_dict=contact_dict,
                data_dict_compare=data_dict_compare,
                where_compare=where_compare,
                params_compare=params_compare,
                compare_with_or=True,
                select_clause_value=select_clause_value,
            )
            logger.end("contact added", object={"contact_id": contact_id})
        except Exception as exception:
            logger.error(
                f"Contact.insert Exception: {exception}",
                object={"exception": exception},
            )
            logger.end()
            raise ContactInsertionException(
                "Exception occurred while inserting contact." + str(exception)
            )

        return contact_row_dict

    def __process_contact_info_details(self, contact_dict: dict) -> dict:
        # TODO: The following is a more complex method to get the person information, fix it later
        first_name = contact_dict.get("first_name")
        last_name = contact_dict.get("last_name")
        if not first_name and not last_name:
            url = contact_dict.get("website1") or contact_dict.get("url")
            result_dict = {
                "email_addresses": contact_dict.get("email1"),
                "urls": [url] if url else [],
            }
            return result_dict
        email_address = (
            contact_dict.get("email1")
            or contact_dict.get("email2")
            or contact_dict.get("email3")
        )
        url = (
            contact_dict.get("website1")
            or contact_dict.get("website2")
            or contact_dict.get("website3")
            or contact_dict.get("url")
        )
        if first_name:
            if len(first_name.split()) > 1 and last_name is None:
                splitted_name_dict = PersonsLocal.split_first_name_field(
                    first_name=first_name
                )
                first_name = splitted_name_dict.get("first_name")
                last_name = splitted_name_dict.get("last_name")
        PeopleLocal.set_details(
            self,
            first_name_original=first_name,
            last_names_original=[last_name] if last_name else [],
            organizations_names_original=self.organizations_names_original,
            email_addresses=[email_address] if email_address else [],
            urls=[url] if url else [],
        )
        result_dict = {"email_addresses": email_address, "urls": [url] if url else []}
        return result_dict

    # TODO: Do we still need this method when we have update_contact_by_dict?
    def update(
        self,
        contact_id: int,
        person_id: int,
        name_prefix: str,
        first_name: str,
        additional_name: str,
        job_title: str,
    ) -> None:
        try:
            object1 = {
                "person_id": person_id,
                "name_prefix": name_prefix,
                "first_name": first_name,
                "additional_name": additional_name,
                "job_title": job_title,
                "contact_id": contact_id,
            }
            logger.start(object=object1)
            contact_data = {
                "person_id": person_id,
                "name_prefix": name_prefix,
                "first_name": first_name,
                "additional_name": additional_name,
                "job_title": job_title,
                "contact_id": contact_id,
            }
            self.update_by_column_and_value(
                column_name="contact_id",
                column_value=contact_id,
                data_dict=contact_data,
            )
            logger.end("contact updated", object={"contact_id": contact_id})
        except Exception as exception:
            logger.error(
                f"Contact.update Exception: {exception}",
                object={"exception": exception},
            )
            logger.end()
            raise ContactUpdateException(
                "Exception occurred while updating contact." + str(exception)
            )

    def update_contact_by_dict(self, contact_id, contact_dict: dict) -> None:
        logger.start(object={"contact_dict": contact_dict})
        processed_contact_info_details_dict = self.__process_contact_info_details(
            contact_dict
        )
        contact_dict = {
            "owner_profile_id": contact_dict.get("owner_profile_id", None),
            "data_source_instance_id": contact_dict.get(
                "data_source_instance_id", None
            ),
            "account_name": contact_dict.get("account_name", None),
            "person_id": contact_dict.get("person_id", None),
            "name_prefix": contact_dict.get("name_prefix", None),
            "first_name": (
                self.normalized_first_name
                if self.normalized_first_name
                else contact_dict.get("first_name")
            ),
            "original_first_name": (
                self.first_name_original
                if self.first_name_original
                else contact_dict.get("first_name")
            ),
            "additional_name": contact_dict.get("additional_name", None),
            "last_name": (
                self.normalized_last_names[0]
                if self.normalized_last_names
                else contact_dict.get("last_name")
            ),
            "original_last_name": (
                self.last_names_original[0] if self.last_names_original else None
            ),
            "full_name": contact_dict.get("full_name", None),
            "name_suffix": contact_dict.get("name_suffix", None),
            "nickname": contact_dict.get("nickname", None),
            "display_as": contact_dict.get("display_as", None),
            "title": contact_dict.get("title", None),
            "organization": contact_dict.get("organization", None),
            "organization_profile_id": contact_dict.get(
                "organization_profile_id", None
            ),
            "job_title": contact_dict.get("job_title", None),
            "department": contact_dict.get("department", None),
            "notes": contact_dict.get("notes", None),
            "email1": processed_contact_info_details_dict.get("email_addresses"),
            "email2": contact_dict.get("email2", None),
            "email3": contact_dict.get("email3", None),
            "phone1": contact_dict.get("phone1", None),
            "phone2": contact_dict.get("phone2", None),
            "phone3": contact_dict.get("phone3", None),
            "address1_street": contact_dict.get("address1_street", None),
            "address1_city": contact_dict.get("address1_city", None),
            "address1_state": contact_dict.get("address1_state", None),
            "address1_postal_code": contact_dict.get("address1_postal_code", None),
            "address1_country": contact_dict.get("address1_country", None),
            "address2_street": contact_dict.get("address2_street", None),
            "address2_city": contact_dict.get("address2_city", None),
            "address2_state": contact_dict.get("address2_state", None),
            "address2_postal_code": contact_dict.get("address2_postal_code", None),
            "address2_country": contact_dict.get("address2_country", None),
            "birthday": contact_dict.get("birthday", None),
            "day": contact_dict.get("day", None),
            "month": contact_dict.get("month", None),
            "year": contact_dict.get("year", None),
            "cira": contact_dict.get("cira", None),
            "anniversary": contact_dict.get("anniversary", None),
            "website1": (
                processed_contact_info_details_dict.get("urls")[0]
                if processed_contact_info_details_dict.get("urls")
                else None
            ),
            "website2": contact_dict.get("website2", None),
            "website3": contact_dict.get("website3", None),
            "photo_url": contact_dict.get("photo_url", None),
            "photo_file_name": contact_dict.get("photo_file_name", None),
            "source": contact_dict.get("source", None),
        }
        if contact_dict.get("display_as", None) is None:
            contact_dict["display_as"] = contact_dict.get("original_first_name", None)
            if contact_dict.get("original_last_name", None) is not None:
                contact_dict["display_as"] += " " + contact_dict.get(
                    "original_last_name", ""
                )
        if contact_dict.get("full_name") is None:
            contact_dict["full_name"] = contact_dict.get("first_name")
            if contact_dict.get("last_name") is not None:
                contact_dict["full_name"] += " " + contact_dict.get("last_name")
        self.update_by_column_and_value(
            column_name="contact_id", column_value=contact_id, data_dict=contact_dict
        )
        logger.end()

    def delete_by_contact_id(self, contact_id: any) -> None:
        try:
            logger.start(object={"contact_id": contact_id})
            self.delete_by_column_and_value(
                column_name="contact_id", column_value=contact_id
            )
            logger.end("contact deleted", object={"contact_id": contact_id})
        except Exception as err:
            logger.error(f"Contact.delete Exception: {err}", object=err)
            # cursor.close()
            logger.end()
            raise ContactDeletionException(
                "Exception occurred while deleting contact." + str(err)
            )

    # TODO: since we have upsert, is this method still useful?
    def insert_update_contact(self, contact_dict: dict) -> int:
        logger.start(object={"contact_dict": contact_dict})
        if not contact_dict:
            logger.error("contact_dict cannot be empty")
            logger.end()
            raise ContactInsertionException("contact_dict cannot be empty")

        try:
            existing_contact_dict = self.get_existing_contact_dict(contact_dict)
            if existing_contact_dict:
                # If the contact exists, update it
                contact_id = existing_contact_dict.get("contact_id", None)
                self.update_contact_by_dict(
                    contact_id=contact_id, contact_dict=contact_dict
                )
            else:
                # If the contact does not exist, insert it
                contact_id = self.insert_contact_dict(contact_dict)
        except Exception as e:
            logger.error(f"Failed to insert/update contact: {e}")
            logger.end()
            raise ContactInsertionException(f"Failed to insert/update contact: {e}")

        logger.end()
        return contact_id

    def insert_batch(self, contact_list: List[Dict]) -> List[int]:
        logger.start()
        inserted_ids = []
        try:
            for contact in contact_list:
                contact_id = self.insert_contact_dict(contact_dict=contact)
                inserted_ids.append(contact_id)
            logger.end("contacts added", object={"inserted_ids": inserted_ids})
        except Exception as err:
            inserted_ids_str = ",".join(str(x) for x in inserted_ids)
            logger.error(
                f"Contact.insert_batch Exception: {err} " + inserted_ids_str, object=err
            )
            raise ContactBatchInsertionException(
                "Exception occurred while batch inserting contacts." + str(err)
            )

        return inserted_ids

    def get_contact_by_contact_id(self, contact_id: int) -> dict:
        logger.start(object={"contact_id": contact_id})
        try:
            contact = self.select_one_dict_by_column_and_value(
                view_table_name=CONTACT_VIEW_TABLE_NAME,
                column_name=CONTACT_ID_COLUMN_NAME,
                column_value=contact_id,
            )
        except Exception as err:
            logger.error(f"Contact.get_contact_by_id Exception: {err}", object=err)
            logger.end()
            raise err
        return contact

    def insert_contact_object(self, contact: Contact) -> int:
        logger.start(object={"contact": contact})
        if not contact:
            logger.error("contact cannot be empty")
            logger.end()
            raise ContactBatchInsertionException("contact cannot be empty")

        required_fields = ["first_name", "last_name", "organization", "job_title"]
        if not any(getattr(contact, field, None) for field in required_fields):
            logger.error(
                "contact must have at least one of the following "
                + "fields: first_name, last_name, organization, job_title"
            )
            logger.end()
            raise ContactObjectInsertionException(
                "contact must have at least one of the following"
                + "fields: first_name, last_name, organization, job_title"
            )
        contact_id = None
        try:
            contact_dict = vars(contact)
            if contact.display_as is None:
                display_name = contact.first_name
                if contact.last_name is not None:
                    display_name += " " + contact.last_name
                contact_dict["display_as"] = display_name

            contact_id = self.insert(data_dict=contact_dict)
            logger.end("contact added", object={"contact_id": contact_id})
        except Exception as exception:
            logger.error(
                f"Contact.insert Exception: {exception}",
                object={"exception": exception},
            )
            logger.end()
            raise ContactObjectInsertionException(
                "Exception occurred while inserting contact." + str(exception)
            )

        return contact_id

    # TODO: Change it to a more sophisticated method later
    def get_existing_contact_dict(self, contact_dict: dict) -> dict:
        logger.start(object={"contact_dict": contact_dict})

        existing_contact = self._check_if_phone_exists(
            contact_dict
        ) or self._check_if_email_address_exists(contact_dict)

        logger.end(object={"existing_contact": existing_contact})
        return existing_contact

    def get_contact_phone_numbers_from_contact_dict(
        self, contact_dict: dict
    ) -> list[str]:
        """
        Get contact phones from contact dict
        :param contact_dict: contact dict
        :return: contact phones
        """
        logger.start(object={"contact_dict": contact_dict})
        phone_numbers_list: list[str] = []
        phone_number1: str = contact_dict.get("phone1")
        phone_number2: str = contact_dict.get("phone2")
        phone_number3: str = contact_dict.get("phone3")
        if phone_number1 is not None and phone_number1 != "":
            phone_numbers_list.append(phone_number1)
        if phone_number2 is not None and phone_number2 != "":
            phone_numbers_list.append(phone_number2)
        if phone_number3 is not None and phone_number3 != "":
            phone_numbers_list.append(phone_number3)
        logger.end(object={"phone_numbers_list": phone_numbers_list})
        return phone_numbers_list

    def get_contact_email_addresses_from_contact_dict(
        self, contact_dict: dict
    ) -> list[str]:
        logger.start(object={"contact_dict": contact_dict})
        email_addresses_list: list[str] = []
        # TODO use enum const for "email1" ....
        email_address1 = contact_dict.get("email1")
        email_address2 = contact_dict.get("email2")
        email_address3 = contact_dict.get("email3")
        if email_address1 is not None and email_address1 != "":
            email_addresses_list.append(email_address1)
        if email_address2 is not None and email_address2 != "":
            email_addresses_list.append(email_address2)
        if email_address3 is not None and email_address3 != "":
            email_addresses_list.append(email_address3)
        logger.end(object={"email_addresses_list": email_addresses_list})
        return email_addresses_list

    # I don't know if we need it right now
    # def _warn_if_phone_number_or_email_address_exist_with_different_name(self, contact_dict: dict) -> None:
    #     """
    #     Warn if phone number or email address already exists with different name
    #     :param contact_dict: contact dict
    #     :return: None
    #     """
    #     METHOD_NAME = "_warn_if_phone_number_or_email_address_exist_with_different_name"
    #     logger.start(METHOD_NAME)
    #     email_address1 = contact_dict.get("email1")
    #     email_address2 = contact_dict.get("email2")
    #     email_address3 = contact_dict.get("email3")
    #     phone_number1 = contact_dict.get("phone1")
    #     phone_number2 = contact_dict.get("phone2")
    #     phone_number3 = contact_dict.get("phone3")
    #     select_data_dict = {
    #         "email1": email_address1, "email2": email_address2, "email3": email_address3,
    #         "phone1": phone_number1, "phone2": phone_number2, "phone3": phone_number3
    #     }
    #     where, params = process_select_data_dict(data_dict=select_data_dict, select_with_or=True)
    #     try:
    #         contact_row_dict = self.select_one_dict_by_where(
    #             select_clause_value="contact_id", where=where, params=params)
    #     except Exception as exception:
    #         logger.error(f"Exception occurred while selecting contact: {exception}", object=exception)
    #         raise exception
    #     if contact_row_dict:
    #         logger.warning(f"Contact with the same phone number or email address already exists but the name is different")

    #     logger.end(METHOD_NAME)

    def _check_if_phone_exists(self, contact_dict: dict) -> dict:
        phone1 = contact_dict.get("phone1")
        phone2 = contact_dict.get("phone2")
        phone3 = contact_dict.get("phone3")

        if phone1:
            return self._check_if_name_exists(contact_dict, "phone1", phone1)
        elif phone2:
            return self._check_if_name_exists(contact_dict, "phone2", phone2)
        elif phone3:
            return self._check_if_name_exists(contact_dict, "phone3", phone3)

        return {}

    def _check_if_email_address_exists(self, contact_dict: dict) -> dict:
        email1 = contact_dict.get("email1")
        email2 = contact_dict.get("email2")
        email3 = contact_dict.get("email3")

        if email1:
            return self._check_if_name_exists(contact_dict, "email1", email1)
        elif email2:
            return self._check_if_name_exists(contact_dict, "email2", email2)
        elif email3:
            return self._check_if_name_exists(contact_dict, "email3", email3)

        return {}

    def _check_if_name_exists(
        self, contact_dict: dict, column_name: str, column_value: str
    ) -> dict:
        try:
            contact = self.select_one_dict_by_column_and_value(
                view_table_name=CONTACT_VIEW_TABLE_NAME,
                column_name=column_name,
                column_value=column_value,
            )
        except Exception as err:
            logger.error(
                f"Contact._check_if_contact_exists Exception: {err}", object=err
            )
            logger.end()
            raise err

        if contact:
            # Check if existing contact's name is not equal to the new contact's name
            if contact.get("first_name") != contact_dict.get(
                "first_name"
            ) or contact.get("last_name") != contact_dict.get("last_name"):
                # Warn about the different name
                logger.warning(
                    "Contact with the same phone number or email_address already exists but "
                    + "the name is different"
                    + str(contact)
                )
            return contact

        return {}

    def insert_contact(self, is_test_data: bool = False, **kwargs):
        data_dict = {"is_test_data": is_test_data}
        data_dict.update(kwargs)

        contact_id = self.insert(
            schema_name="contact", table_name="contact_table", data_dict=data_dict
        )
        return contact_id

    def delete_contact_by_id(self, contact_id: int) -> None:
        self.delete_by_column_and_value(
            column_name="contact_id", column_value=contact_id
        )

    def get_test_contact_id(self) -> int:
        return self.get_test_entity_id(
            entity_name="contact", insert_function=self.insert_contact
        )

    def __get_data_dict_compare_for_upsert_contact_dict(
        self, contact_dict: dict
    ) -> MultiDict:
        data_dict_compare = MultiDict()
        self.__process_resource_name(
            contact_dict=contact_dict, data_dict_compare=data_dict_compare
        )
        if data_dict_compare.get("contact_id"):
            return data_dict_compare
        if contact_dict.get("email1"):
            self.__add_email_address_to_data_dict_compare(
                email_address=contact_dict.get("email1"),
                data_dict_compare=data_dict_compare,
            )
        if contact_dict.get("phone1"):
            self.__add_phone_number_to_data_dict_compare(
                phone_number=contact_dict.get("phone1"),
                data_dict_compare=data_dict_compare,
            )
        if contact_dict.get("email2"):
            self.__add_email_address_to_data_dict_compare(
                email_address=contact_dict.get("email2"),
                data_dict_compare=data_dict_compare,
            )
        if contact_dict.get("phone2"):
            self.__add_phone_number_to_data_dict_compare(
                phone_number=contact_dict.get("phone2"),
                data_dict_compare=data_dict_compare,
            )
        if contact_dict.get("email3"):
            self.__add_email_address_to_data_dict_compare(
                email_address=contact_dict.get("email3"),
                data_dict_compare=data_dict_compare,
            )
        if contact_dict.get("phone3"):
            self.__add_phone_number_to_data_dict_compare(
                phone_number=contact_dict.get("phone3"),
                data_dict_compare=data_dict_compare,
            )
        if len(data_dict_compare) == 0:
            url = contact_dict.get("url")
            website = (
                contact_dict.get("website1")
                or contact_dict.get("website2")
                or contact_dict.get("website3")
            )
            if url:
                # This case is useful for linkedin contacts
                normalized_url = (
                    url.lower().replace("http://", "").replace("https://", "")
                )
                data_dict_compare.add("website1", url)
                data_dict_compare.add("website1", normalized_url)
            elif website:
                # TODO: use https://stackoverflow.com/questions/6170295/is-there-a-predefined-class-for-url-in-python
                # try the last comment
                normalized_website = (
                    website.lower().replace("http://", "").replace("https://", "")
                )
                data_dict_compare.add("website1", website)
                data_dict_compare.add("website1", normalized_website)
                data_dict_compare.add("website2", website)
                data_dict_compare.add("website2", normalized_website)
                data_dict_compare.add("website3", website)
                data_dict_compare.add("website3", normalized_website)
            elif contact_dict.get("first_name"):
                if contact_dict.get("display_as", None) is None:
                    contact_dict["display_as"] = contact_dict.get("first_name", None)
                    if contact_dict.get("last_name", None) is not None:
                        contact_dict["display_as"] += " " + contact_dict.get(
                            "last_name", ""
                        )
                    data_dict_compare.add("display_as", contact_dict.get("display_as"))
                else:
                    data_dict_compare.add("display_as", contact_dict.get("display_as"))
            # TODO: Shall we add oprganization name to data_dict_compare here?
        if not data_dict_compare:
            logger.warning(
                "can't find details in contact_dict for compare_data_dict, may insert duplicate contact"
            )
        return data_dict_compare

    def __process_resource_name(self, contact_dict: dict, data_dict_compare: dict):
        if contact_dict.get("resource_name"):
            resource_name = contact_dict.get("resource_name")
            if (
                contact_dict.get("data_source_type_id")
                == GOOGLE_CONTACT_PEOPLE_API_DATA_SOURCE_TYPE_ID
            ):
                try:
                    connection = Connector.connect("importer")
                    query_get = (
                        "SELECT c.contact_id FROM contact.contact_view c "
                        "JOIN importer.importer_view i ON c.contact_id = i.entity_id "
                        "WHERE i.google_people_api_resource_name = %s AND c.end_timestamp IS NULL"
                    )
                    cursor = connection.cursor()
                    cursor.execute(query_get, (resource_name,))
                    contact_id_tuples = cursor.fetchall()
                    if contact_id_tuples:
                        for index_fetch, contact_id_tuple in enumerate(
                            contact_id_tuples
                        ):
                            if index_fetch == 0:
                                contact_id = contact_id_tuple[0]
                                data_dict_compare["contact_id"] = contact_id
                            else:
                                logger.warning(
                                    f"Multiple contact_ids found for resource_name: {resource_name}",
                                    object={
                                        "resource_name": resource_name,
                                        "contact_id_tuple": contact_id_tuple,
                                        "index_fetch": index_fetch,
                                        },
                                    )
                except Exception as exception:
                    logger.error(
                        f"Error while getting contact_id from importer_view JOIN contact_view: {exception}"
                    )
                    raise exception
            self.set_schema(schema_name="contact")

    def process_last_name(contact_dict: dict) -> dict:

        if contact_dict["last_name"] is None:
            new_name = contact_dict["first_name"].split(" ")
            contact_dict["first_name"] = new_name[0]
            new_last_name = ""
            for item in new_name[1:]:
                new_last_name += item + " "
            contact_dict["last_name"] = new_last_name.strip()

        if contact_dict["last_name"].isalpha():
            contact_dict["first_name"] = contact_dict["first_name"].capitalize()
            contact_dict["last_name"] = contact_dict["last_name"].capitalize()
        return contact_dict

    def __add_email_address_to_data_dict_compare(
        self, email_address: str, data_dict_compare: dict
    ):
        data_dict_compare.add("email1", email_address)
        data_dict_compare.add("email2", email_address)
        data_dict_compare.add("email3", email_address)

    def __add_phone_number_to_data_dict_compare(
        self, phone_number: str, data_dict_compare: dict
    ):
        data_dict_compare.add("phone1", phone_number)
        data_dict_compare.add("phone2", phone_number)
        data_dict_compare.add("phone3", phone_number)

    def __get_where_compare_and_params(self, contact_dict: dict) -> tuple[str, tuple]:
        where_compare = ""
        params = ()
        owner_profile_id = contact_dict.get("owner_profile_id")
        if owner_profile_id:
            where_compare += "owner_profile_id = %s"
            params += (owner_profile_id,)
        source = contact_dict.get("source")
        if source:
            if where_compare:
                where_compare += " AND "
            where_compare += "source = %s"
            params += (source,)
        if where_compare:
            return where_compare, params
        else:
            return None, None

    def __get_details_for_people_local_from_contact_dict(
        self, *, contact_dict: dict
    ) -> tuple:
        if contact_dict:
            first_name_original = (
                contact_dict.get("first_name")
                if contact_dict.get("first_name")
                else None
            )
            last_names_original = (
                [contact_dict.get("last_name")]
                if contact_dict.get("last_name")
                else None
            )
            organizations_names_original = (
                [contact_dict.get("organization")]
                if contact_dict.get("organizations")
                else None
            )
            email_address1 = contact_dict.get("email1")
            email_address2 = contact_dict.get("email2")
            email_address3 = contact_dict.get("email3")
            # Some of the email addresses can be None, We add to the list only if they are not None
            email_addresses = []
            if email_address1:
                email_addresses.append(email_address1)
            if email_address2:
                email_addresses.append(email_address2)
            if email_address3:
                email_addresses.append(email_address3)
            # If email_addresses is empty, we set it to None
            email_addresses = email_addresses if email_addresses else None
        else:
            first_name_original = None
            last_names_original = None
            organizations_names_original = None
            email_addresses = None
        return (
            first_name_original,
            last_names_original,
            organizations_names_original,
            email_addresses,
        )

    def set_details(self, *, contact_dict) -> None:
        details_for_people_local = (
            self.__get_details_for_people_local_from_contact_dict(
                contact_dict=contact_dict
            )
        )
        (
            first_name_original,
            last_names_original,
            organizations_names_original,
            email_addresses,
        ) = details_for_people_local
        PeopleLocal.set_details(
            self,
            first_name_original=first_name_original,
            last_names_original=last_names_original,
            organizations_names_original=organizations_names_original,
            email_addresses=email_addresses,
        )

    @staticmethod
    def fix_contacts(order_by: str = None, limit: int = 1) -> None:
        contacts_local = ContactsLocal()
        contacts_ids_with_no_main_profile_id = (
            contacts_local.select_multi_value_by_where(
                select_clause_value="contact_id",
                where="main_profile_id IS NULL",
                limit=limit,
                order_by=order_by,
            )
        )
        for contact_id in contacts_ids_with_no_main_profile_id:
            # get profile id and person id from contact_profile_table if there's only one profile connected to the contact
            profile_ids = contacts_local.select_multi_value_by_where(
                schema_name="contact_profile",
                view_table_name="contact_profile_view",
                select_clause_value="profile_id",
                where="contact_id = %s",
                limit=2,
                params=(contact_id,),
            )
            if len(profile_ids) == 1:
                profile_id = profile_ids[0]
                data_dict = {"main_profile_id": profile_id}
                contacts_local.update_by_column_and_value(
                    schema_name="contact",
                    table_name="contact_table",
                    column_name="contact_id",
                    column_value=contact_id,
                    data_dict=data_dict,
                )
            persons_ids = contacts_local.select_multi_value_by_where(
                schema_name="contact_person",
                view_table_name="contact_person_view",
                select_clause_value="person_id",
                where="contact_id = %s",
                limit=2,
                params=(contact_id,),
            )
            if len(persons_ids) == 1:
                person_id = persons_ids[0]
                data_dict = {"person_id": person_id}
                contacts_local.update_by_column_and_value(
                    schema_name="contact",
                    table_name="contact_table",
                    column_name="contact_id",
                    column_value=contact_id,
                    data_dict=data_dict,
                )
            contact_dict = contacts_local.select_one_dict_by_column_and_value(
                select_clause_value="owner_profile_id, created_effective_profile_id",
                column_name="contact_id",
                column_value=contact_id,
            )
            if contact_dict.get("owner_profile_id") is None:
                data_dict = {
                    "owner_profile_id": contact_dict.get("created_effective_profile_id")
                }
                contacts_local.update_by_column_and_value(
                    column_name="contact_id",
                    column_value=contact_id,
                    data_dict=data_dict,
                )
