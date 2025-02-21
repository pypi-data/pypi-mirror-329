"""
APIs provided by data-table-mysql-server1-0

generated by model_code_gen.py
  - **filename** : ``data_table_mysql.py``
  - **json timestamp** : ``2021-06-29 10:49:22``
"""
from .base import get, post, DynamicRootAPI, ChildAPI
from .models.datatable_mysql import *
from deepfos.lib.decorator import cached_property
from typing import List, Dict, Union, Any, Awaitable


__all__ = ['MySQLAPI', 'ClickHouseAPI', 'SQLServerAPI', 'OracleAPI',
           'KingBaseAPI', 'GaussAPI', 'DaMengAPI', 'PostgreSQLAPI',
           'DeepEngineAPI', 'DeepModelAPI', 'DeepModelKingBaseAPI']


class DDLAPI(ChildAPI):
    endpoint = '/datatable-edit-view'

    @post('column-add')
    def column_add(self, datatableColumnAddDTO: DatatableColumnAddDTO) -> Union[Any, Awaitable[Any]]:
        """
        新增列字段信息（后端组件调用）

        给数据表新增列信息（后端组件调用）
        """
        return {'body': datatableColumnAddDTO}

    @post('datatable-save')
    def create_table(self, param: DatatableInfoSaveParam) -> Union[DatatableInfoSaveParam, Awaitable[DatatableInfoSaveParam]]:
        """
        数据表新建&编辑（后端组件调用）

        """
        return {'body': param}

    @post('datatable-save-edit')
    def datatable_save_edit(self, param: DatatableInfoSaveParam) -> Union[DatatableInfoSaveParam, Awaitable[DatatableInfoSaveParam]]:
        """
        数据表新建&编辑（前端调用）

        """
        return {'body': param}

    @post('generateActualTableName')
    def generateActualTableName(self, param: GenerateActualTableNameDTO) -> Union[Any, Awaitable[Any]]:
        """
        根据tableName生成ActualTableName

        """
        return {'body': param}

    @post('only-check')
    def only_check(self, param: DatatableInfoSaveParam) -> Union[DatatableInfoSaveParam, Awaitable[DatatableInfoSaveParam]]:
        """
        数据表编辑--仅校验（后端组件调用）

        数据表保存、编辑前的仅校验接口（后端组件调用）
        """
        return {'body': param}

    @post('only-save')
    def only_save(self, param: DatatableInfoSaveParam) -> Union[DatatableInfoSaveParam, Awaitable[DatatableInfoSaveParam]]:
        """
        数据表编辑--仅保存（后端组件调用，新建时实际表名的末尾加随机数）

        数据表保存、编辑前的仅保存接口（后端组件调用，新建时实际表名的末尾加随
        机数）
        """
        return {'body': param}

    @post('only-save-edit')
    def only_save_edit(self, param: DatatableInfoSaveParam) -> Union[DatatableInfoSaveParam, Awaitable[DatatableInfoSaveParam]]:
        """
        数据表编辑--仅保存（后端组件调用，带实际表名就不做任何处理）

        数据表保存、编辑前的仅保存接口（后端组件调用，带实际表名就不做任何处理
        ）
        """
        return {'body': param}


class DMLAPI(ChildAPI):
    endpoint = '/datatable'

    @post('actual-tablename')
    def get_tablename(self, table_info: BaseElementInfo) -> Union[str, Awaitable[str]]:
        """
        获取数据表实际表名

        通过elementName,folderId从元素信息获取数据表实际表
        名
        """
        return {'body': table_info}

    @post('batch-actual-tablename')
    def batch_tablename(self, paramList: List[BaseElementInfo]) -> Union[dict, Awaitable[dict]]:
        """
        根据元素名称批量获取实际表名

        """
        return {'body': paramList}

    @post('column-list')
    def list_column(self, table_name: str) -> Union[Any, Awaitable[Any]]:
        """
        返回数据表字段列表信息

        根据实际表名，查询数据表字段信息
        """
        return {'param': {'actualTableName': table_name}}

    @post('column/column-name')
    def column_column_name(self, param: DatatableColumnInfoDTO) -> Union[MiscModel, Awaitable[MiscModel]]:
        """
        根据列名获取数据表的Column信息

        根据列名获取列表的详细信息
        """
        return {'body': param}

    @post('custom-sql')
    def run_sql(self, sql: str) -> Union[CustomSqlRespDTO, Awaitable[CustomSqlRespDTO]]:
        """
        自定义SQL执行(后端调用)--增删改查，支持多表联合查询
        """
        return {'body': {'sql': sql}}

    @post('data-diff')
    def data_diff(self, param: DatatableInfoBasicInfoDTO) -> Union[str, Awaitable[str]]:
        """
        判断数据表与实际表是否一致

        判断数据表组件元素配置信息和实际物理数据表字段信息是否一致
        """
        return {'body': param}

    @post('datatable-info-batch')
    def datatable_info_batch(self, param: List[BaseElementInfo]) -> Union[List[DatatableInfoBasicInfoDTO], Awaitable[List[DatatableInfoBasicInfoDTO]]]:
        """
        批量获取数据表信息

        批量通过elementName,folderId从元素信息获取数据表信
        息
        """
        return {'body': param}

    @post('delete-data')
    def delete_data(self, param: DatatableDataDeleteDTO) -> Union[bool, Awaitable[bool]]:
        """
        删除数据表中的数据

        """
        return {'body': param}

    @post('distinct-column-members')
    def distinct_column_members(self, param: DatatableInfoMemberDTO) -> Union[List[str], Awaitable[List[str]]]:
        """
        查询数据表列字段，去重后的数据集合

        根据列名查询数据表，该列去重后的数据集合
        """
        return {'body': param}

    @post('execute-sql')
    def execute_sql(self, datatableSelectDTO: DatatableSelectDTO) -> Union[Any, Awaitable[Any]]:
        """
        查询数据表数据

        执行查询sql查询数据表的数据
        """
        return {'body': datatableSelectDTO}

    @post('executeBatchSql')
    def execute_batch_sql(self, sqls: List[str]):
        """
        执行多句增删改sql

        Args:
            sqls: 查询sql
        """
        return {'body': {
            "elementBaseInfoParamMap": {},
            "batchSql": sqls,
            },
        }

    @post('insert')
    def insert(self, param: DatatableInsertDTO) -> Union[bool, Awaitable[bool]]:
        """
        向数据表中写入数据

        """
        return {'body': param}

    @post('physical-table-exist')
    def physical_table_exist(self, param: PhysicalTableExistDTO) -> Union[str, Awaitable[str]]:
        """
        根据元素信息或者直接通过传参的实际表名，判断对应的物理数据表是否存在

        优先通过元素信息获取到实际表名后，再判断物理表是否存在
        """
        return {'body': param}

    @post('table-ifexists')
    def table_ifexists(self, param: DatatableInfoCheckDTO) -> Union[bool, Awaitable[bool]]:
        """
        数据表是否存在

        根据数据表名称判断数据表是否存在
        """
        return {'body': param}

    @post('table-ifexists-physical')
    def table_ifexists_physical(self, param: DatatableInfoCheckDTO) -> Union[bool, Awaitable[bool]]:
        """
        只判断物理数据表是否存在

        根据数据表名称，只判断物理数据表是否存在
        """
        return {'body': param}

    @post('table-info-field')
    def table_info_field(self, elementList: List[BaseElementInfo]) -> Union[List[DatatableInfoBasicInfoDTO], Awaitable[List[DatatableInfoBasicInfoDTO]]]:
        """
        获取数据表元素信息（从平台获取信息）

        返回数据表所有元素配置信息（从平台获取信息）
        """
        return {'body': elementList}

    @post('table-info-field-physical')
    def table_info_field_physical(self, elementList: List[BaseElementInfo]) -> Union[List[DatatableInfoBasicInfoDTO], Awaitable[List[DatatableInfoBasicInfoDTO]]]:
        """
        获取数据表元素信息（从物理表获取信息）

        返回数据表所有元素配置信息（从物理表获取信息）
        """
        return {'body': elementList}

    @post('update-data')
    def update_data(self, param: DatatableDataUpdateDTO) -> Union[bool, Awaitable[bool]]:
        """
        更新数据表中的数据

        """
        return {'body': param}

    @post('account')
    def create_account(self) -> Union[AccountInfo, Awaitable[AccountInfo]]:
        """
        获取/更新数据库账号

        """
        return {'body': {"serverType": "python"}}


class MySQLAPI(DynamicRootAPI, builtin=True):
    """MySQL数据表组件接口"""
    module_type = 'DAT_MYSQL'
    default_version = (1, 0)
    multi_version = False
    cls_name = 'MySQLAPI'
    module_name = 'deepfos.api.datatable'
    api_version = (1, 0)

    @cached_property
    def ddl(self) -> DDLAPI:
        """
        数据表新建&编辑相关接口
        """
        return DDLAPI(self)

    @cached_property
    def dml(self) -> DMLAPI:
        """
        外部组件访问数据表相关接口
        """
        return DMLAPI(self)


class ClickHouseAPI(MySQLAPI, builtin=True):
    """ClickHouse数据表组件接口"""
    module_type = 'DAT_CLICKHOUSE'
    cls_name = 'ClickHouseAPI'


class SQLServerAPI(MySQLAPI, builtin=True):
    """SQLServer数据表组件接口"""
    module_type = 'DAT_SQLSERVER'
    cls_name = 'SQLServerAPI'


class OracleAPI(MySQLAPI, builtin=True):
    """Oracle数据表组件接口"""
    module_type = 'DAT_ORACLE'
    cls_name = 'OracleAPI'


class KingBaseAPI(MySQLAPI, builtin=True):
    """KingBase数据表组件接口"""
    module_type = 'DAT_KINGBASE'
    cls_name = 'KingBaseAPI'


class GaussAPI(MySQLAPI, builtin=True):
    """GaussDB数据表组件接口"""
    module_type = 'DAT_GAUSS'
    cls_name = 'GaussAPI'


class DaMengAPI(OracleAPI, builtin=True):
    """达梦数据表组件接口"""
    module_type = 'DAT_DAMENG'
    cls_name = 'DaMengAPI'


class PostgreSQLAPI(MySQLAPI, builtin=True):
    """PostgreSQL数据表组件接口"""
    module_type = 'DAT_POSTGRESQL'
    cls_name = 'PostgreSQLAPI'


class DeepEngineAPI(MySQLAPI, builtin=True):
    """DeepEngine数据表组件接口"""
    module_type = 'DAT_DEEPENGINE'
    cls_name = 'DeepEngineAPI'


class DeepModelAPI(MySQLAPI, builtin=True):
    """DeepModel数据表组件接口"""
    module_type = 'DAT_DEEPMODEL'
    cls_name = 'DeepModelAPI'


class DeepModelKingBaseAPI(MySQLAPI, builtin=True):
    """DeepModel KingBase数据表组件接口"""
    module_type = 'DAT_DEEPMODEL_KB'
    cls_name = 'DeepModelKingBaseAPI'
