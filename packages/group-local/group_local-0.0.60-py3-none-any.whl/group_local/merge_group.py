from database_mysql_local.generic_crud_ml import GenericCRUDML
from logger_local.MetaLogger import MetaLogger
from user_context_remote.user_context import UserContext
from .group_local_constants import GroupLocalConstants

user_context = UserContext()

DEFAULT_SCHEMA_NAME = "group"
DEFAULT_TABLE_NAME = "group_table"
DEFAULT_VIEW_TABLE_NAME = "group_view"
DEFAULT_COLUMN_NAME = "group_id"
DEFAULT_IS_MAIN_COLUMN_NAME = "is_main_title"


class MergeGroup(GenericCRUDML, metaclass=MetaLogger, object=GroupLocalConstants.GROUP_PYTHON_PACKAGE_CODE_LOGGER_OBJECT):

    def __init__(self, is_test_data: bool = False):
        super().__init__(default_schema_name=DEFAULT_SCHEMA_NAME, default_table_name=DEFAULT_TABLE_NAME,
                         default_column_name=DEFAULT_COLUMN_NAME,
                         is_main_column_name=DEFAULT_IS_MAIN_COLUMN_NAME,
                         is_test_data=is_test_data)

    def merge_group_ml_entities(self, entity_id1: int, entity_id2: int, main_entity_ml_id: int):
        super().merge_ml_entities(entity_id1=entity_id1, entity_id2=entity_id2, main_entity_ml_id=main_entity_ml_id)

    """
        def merge_group_entities(self, entity_id1 : int, entity_id2 : int, main_entity_ml_id: int):
            super().merge_entities(entity_id1=entity_id1, entity_id2=entity_id2)
    """
