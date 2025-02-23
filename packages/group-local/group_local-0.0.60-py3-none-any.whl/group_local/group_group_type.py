
from database_mysql_local.generic_crud_ml import GenericCRUDML
from logger_local.MetaLogger import MetaLogger
from user_context_remote.user_context import UserContext
from .group_local_constants import GroupLocalConstants

user_context = UserContext()

GROUP_GROUP_SCHEMA_NAME = "group_group"
GROUP_GROUP_TYPE_TABLE_NAME = "group_group_type_table"
DEFAULT_VIEW_TABLE_NAME = "group_view"
DEFAULT_COLUMN_NAME = "group_id"
DEFAULT_IS_MAIN_COLUMN_NAME = "is_main_title"


class GroupGroupTypesLocal(GenericCRUDML, metaclass=MetaLogger, object=GroupLocalConstants.GROUP_PYTHON_PACKAGE_CODE_LOGGER_OBJECT):

    def __init__(self, is_test_data: bool = False):
        super().__init__(default_schema_name=GROUP_GROUP_SCHEMA_NAME, default_table_name=GROUP_GROUP_TYPE_TABLE_NAME,
                         default_column_name=DEFAULT_COLUMN_NAME,
                         is_main_column_name=DEFAULT_IS_MAIN_COLUMN_NAME,
                         is_test_data=is_test_data)

    def link_group_to_group_types(self, *, group_id: int, group_type_ids: list[int]) -> list[int]:
        temp = self.default_schema_name
        self.default_schema_name = 'group'
        group_group_types_ids = []
        for group_type_id in group_type_ids:
            group_group_type_data_dict = {
                "group_id": group_id,
                "group_type_id": group_type_id
            }
            group_group_type_id = super().insert(
                data_dict=group_group_type_data_dict, ignore_duplicate=True)
            group_group_types_ids.append(group_group_type_id)
        self.default_schema_name = temp
        return group_group_types_ids
