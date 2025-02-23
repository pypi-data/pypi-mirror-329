
from database_mysql_local.generic_crud_ml import GenericCRUDML
from job_local.jobs_local import JobsLocal
from logger_local.MetaLogger import MetaLogger
from user_context_remote.user_context import UserContext
from .group_local_constants import GroupLocalConstants

user_context = UserContext()

DEFAULT_SCHEMA_NAME = "group"
DEFAULT_TABLE_NAME = "group_table"
DEFAULT_VIEW_TABLE_NAME = "group_view"
DEFAULT_COLUMN_NAME = "group_id"
DEFAULT_IS_MAIN_COLUMN_NAME = "is_main_title"


class InsertLink(GenericCRUDML, metaclass=MetaLogger, object=GroupLocalConstants.GROUP_PYTHON_PACKAGE_CODE_LOGGER_OBJECT):

    def __init__(self, is_test_data: bool = False):
        super().__init__(default_schema_name=DEFAULT_SCHEMA_NAME, default_table_name=DEFAULT_TABLE_NAME,
                         default_column_name=DEFAULT_COLUMN_NAME,
                         is_main_column_name=DEFAULT_IS_MAIN_COLUMN_NAME,
                         is_test_data=is_test_data)
        self.job_local = JobsLocal()

    def insert_link_job_title(self, group_dict: dict, group_id: int, group_ml_ids_list: list[int]) -> dict:
        group_ml_id = group_ml_ids_list[0] if group_ml_ids_list else None
        # Insert job title
        job_title_dict = {
            "job_title.name": group_dict.get('name'),
            "job_title_ml.title": group_dict.get('title'),
            "job_title_ml.is_title_approved": group_dict.get('is_title_approved'),
        }
        insert_job_result = self.job_local.insert_job_title(job_title_dict=job_title_dict)
        if insert_job_result:
            job_title_id, job_title_ml_id = insert_job_result
            self.logger.info("job_title inserted",
                             object={"job_title_id": job_title_id, "job_title_ml_id": job_title_ml_id})
        else:
            result_dict = {}
            return result_dict

        # Link job group_id to job title_id
        # TODO: add group_ml_id to select_clause_value when we have it in group_job_title_view
        group_job_title_dict = super().select_one_dict_by_where(
            schema_name="group_job_title", view_table_name="group_job_title_view",
            select_clause_value="group_job_title_id, job_title_id, job_title_ml_id, group_id",
            where="group_id = %s AND job_title_id = %s", params=(group_id, job_title_id))
        if group_job_title_dict:
            group_job_title_id = group_job_title_dict.get('group_job_title_id')
            if group_job_title_dict.get('job_title_ml_id') is None and group_job_title_dict.get('group_ml_id') is None:
                # update group_job_title
                group_job_title_id = super().update_by_column_and_value(
                    schema_name="group_job_title", table_name="group_job_title_table",
                    column_name="group_job_title_id", column_value=group_job_title_dict.get('group_job_title_id'),
                    data_dict={"job_title_ml_id": job_title_ml_id, "group_ml_id": group_ml_id}
                )
            elif group_job_title_dict.get('job_title_ml_id') is None:
                # update group_job_title
                group_job_title_id = super().update_by_column_and_value(
                    schema_name="group_job_title", table_name="group_job_title_table",
                    column_name="group_job_title_id", column_value=group_job_title_dict.get('group_job_title_id'),
                    data_dict={"job_title_ml_id": job_title_ml_id}
                )
            elif group_job_title_dict.get('group_ml_id') is None:
                # update group_job_title
                group_job_title_id = super().update_by_column_and_value(
                    schema_name="group_job_title", table_name="group_job_title_table",
                    column_name="group_job_title_id", column_value=group_job_title_dict.get('group_job_title_id'),
                    data_dict={"group_ml_id": group_ml_id}
                )
            result_dict = {
                "job_title_id": job_title_id,
                "job_title_ml_id": job_title_ml_id,
                "group_id": group_id,
                "group_ml_id": group_ml_id,
                "group_job_title_id": group_job_title_id
            }

            return result_dict
        data_dict = {
            "group_id": group_id,
            "job_title_id": job_title_id,
            "job_title_ml_id": job_title_ml_id
        }
        group_job_title_id = super().insert(
            schema_name="group_job_title", table_name="group_job_title_table",
            data_dict=data_dict, ignore_duplicate=True
        )
        result_dict = {
            "job_title_id": job_title_id,
            "job_title_ml_id": job_title_ml_id,
            "group_id": group_id,
            "group_ml_id": group_ml_id,
            "group_job_title_id": group_job_title_id
        }
        return result_dict
