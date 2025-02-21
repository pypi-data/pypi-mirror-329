"""
Models used by /gateway-server,/reconciliation-report-server1-0

generated by model_code_gen.py
  - **filename** : ``reconciliation_report.py``
  - **json timestamp** : ``2022-01-07 11:09:47``
"""


from .base import BaseModel
from typing import List, Optional, Union
from pydantic import Field


__all__ = [
    'ErrorDTO',
    'ElementBaseInfo',
    'ReconciliationColumnInfo',
    'TransactionParamDto',
    'DimensionMatchAccountInfo',
    'MatchAccountInfo',
    'ReconciliationReportInfo'
]


class ErrorDTO(BaseModel):
    #: 异常key
    tipKey: Optional[str]
    #: 异常信息
    tipValue: Optional[str]


class ElementBaseInfo(BaseModel):
    """元素基础参数信息

    .. admonition:: 引用接口

        - **POST** ``/check-relation-element``
    """
    #: 元素名称
    elementName: str
    #: 元素类型
    elementType: str
    #: 文件夹id
    folderId: str
    #: 组件id
    moduleId: Optional[str]
    #: 路径
    path: Optional[str]
    #: 服务名
    serverName: Optional[str]


class ReconciliationColumnInfo(BaseModel):
    #: 列名称
    columnName: str
    #: 关联维度信息
    relationDimensionInfo: Optional[ElementBaseInfo]
    #: 展示在列明细，0：不展示；1：展示
    showColDetail: Optional[int]


class TransactionParamDto(BaseModel):
    """查询交易数据参数

    .. admonition:: 引用接口

        - **POST** ``/transaction-datas``
    """
    #: 内存财务模型编码
    cubeCode: str
    #: 内存财务模型文件夹id
    cubeFolderId: str
    #: 内存财务模型组件类型
    cubeModuleType: str
    #: 激活实体表编码
    dataTableCode: Optional[str]
    #: 激活实体表文件夹id
    dataTableFolderId: Optional[str]
    #: 激活实体表组件类型
    dataTableModuleType: Optional[str]
    #: 除科目类、交易伙伴类的其他维度参数
    dimParam: dict
    #: 匹配科目
    matchAccounts: List[str]


class DimensionMatchAccountInfo(BaseModel):
    #: 成员编码
    code: str
    #: 对账报告多语言描述
    description: Optional[dict]
    #: 自定义编码
    udKey: Optional[str]


class MatchAccountInfo(BaseModel):
    """匹配科目信息

    .. admonition:: 引用接口

        - **GET** ``/reconciliation/match-account-info`` (Response: 200)
    """
    #: 匹配科目成员信息
    dimensionSearchMember: Optional[List[DimensionMatchAccountInfo]]
    #: 错误信息
    errorList: Optional[List[ErrorDTO]]
    #: 错误标识
    errorTag: Optional[bool]
    #: 关联维度信息
    relationDimensionInfo: Optional[ElementBaseInfo]
    #: 字段类型
    valueType: int


class ReconciliationReportInfo(BaseModel):
    """对账报告信息dto

    .. admonition:: 引用接口

        - **GET** ``/reconciliation/reconciliation-report-info`` (Response: 200)
        - **POST** ``/reconciliation/save-or-edit-reconciliation-report``
        - **POST** ``/reconciliation/save-or-edit-reconciliation-report`` (Response: 200)
    """
    #: 对账报告编码
    code: str
    #: 对账报告关联内存财务模型
    cubeInfo: Optional[ElementBaseInfo]
    #: 对账报告多语言描述
    description: Optional[dict]
    #: 对账报告元素类型，类型：RR
    elementType: Optional[str]
    #: 错误信息
    errorList: Optional[List[ErrorDTO]]
    #: 错误标识
    errorTag: Optional[bool]
    #: 对账报告文件夹ID
    folderId: str
    #: id
    id: Optional[str]
    #: 关联多语言key
    languageKey: Optional[str]
    #: 匹配科目
    matchAccount: MatchAccountInfo
    #: 对账报告组件ID
    moduleId: Optional[str]
    #: 对账报告路径
    path: Optional[str]
    #: 对账报告元素权限
    permission: Optional[int]
    #: 对账报告列信息
    reconciliationColumnInfoList: List[ReconciliationColumnInfo]
    #: 对账报告备注
    remarks: Optional[str]
    #: 对账报告服务名
    serverName: Optional[str]
    #: 对账报告关联数据表，激活实体表
    stateEntityTableInfo: Optional[ElementBaseInfo]



