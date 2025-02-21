"""
Models used by /reconciliation-engine-server1-0

generated by model_code_gen.py
  - **filename** : ``reconciliation_engine.py``
  - **json timestamp** : ``2022-12-26 11:11:22``
"""


from deepfos.api.models.base import BaseModel
from typing import List, Optional, Union, Any, Dict
from pydantic import Field


__all__ = [
    'AccountInfoParam',
    'CanDoParam',
    'ElementBaseInfoParam',
    'OffTaskItem',
    'OnTaskItem',
    'OrderType',
    'QueryColumnDataItem',
    'QueryTaskListItem',
    'RctDO',
    'ReconSignByHand',
    'ReconciliationExecDto',
    'ReconciliationExecCreate',
    'CancelItem',
    'CancelReconMatch',
    'CancelSignByHand',
    'ConfirmItem',
    'DeleteDsItem',
    'DeleteTaskItem',
    'PageInfoRctDO'
]


class AccountInfoParam(BaseModel):
    #: 参数编码
    code: Optional[str]
    #: 默认值
    defaultValue: Optional[str]
    #: 参数描述
    description: Optional[str]
    #: 长度
    length: Optional[str]
    #: realValue
    realValue: Optional[Any]
    #: 类型 1.文本; 2.整数 3.小数 4.日期 5.日期时间;
    valueType: Optional[int]


class CanDoParam(BaseModel):
    #: 是否清理数据
    isClean: Optional[bool]
    #: 是否确认
    isConfirm: Optional[bool]


class ElementBaseInfoParam(BaseModel):
    """Element Base Info Param

    .. admonition:: 引用接口

        - **POST** ``/data_get/element_column``
    """
    #: 是否绝对路径
    absoluteTag: Optional[bool]
    #: 路径
    elementId: Optional[str]
    #: 元素名
    elementName: str
    #: 元素中英文
    elementNameDesAll: Optional[Any]
    #: 元素类型
    elementType: str
    #: 文件夹id
    folderId: str
    #: 组件id
    moduleId: str
    #: 路径
    path: Optional[str]
    #: 相对路径
    relativePath: Optional[str]
    #: 服务名
    serverName: Optional[str]


class OffTaskItem(BaseModel):
    """Off Task Item

    .. admonition:: 引用接口

        - **POST** ``/reconciliation/off_task``
    """
    #: 批次id
    dsBatchId: Optional[str]
    #: 批次id集合
    dsBatchIds: Optional[List[str]]
    #: 任务id集合
    rcTaskIds: Optional[List[str]]
    #: 对账元素
    reconElement: Optional[ElementBaseInfoParam]


class OnTaskItem(BaseModel):
    """On Task Item

    .. admonition:: 引用接口

        - **POST** ``/reconciliation/on_task``
    """
    #: 批次id
    dsBatchId: Optional[str]
    #: 任务id
    rcTaskId: Optional[str]
    #: 任务id集合
    rcTaskIds: Optional[List[str]]
    #: 对账元素
    reconElement: Optional[ElementBaseInfoParam]


class OrderType(BaseModel):
    #: columnName
    columnName: Optional[str]
    #: orderType
    orderType: Optional[str]


class QueryColumnDataItem(BaseModel):
    """Query Column Data Item

    .. admonition:: 引用接口

        - **POST** ``/data_get/get_column_data``
    """
    #: 自动执行条件
    canDoParam: CanDoParam
    #: 清单表元素
    dsBatchId: Optional[str]
    #: 清单表元素
    dsBatchName: Optional[str]
    #: 清单表元素
    elementBaseInfoParamTable: Optional[ElementBaseInfoParam]
    #: 手动参数
    params: Optional[List[AccountInfoParam]]


class QueryTaskListItem(BaseModel):
    """Query Task List Item

    .. admonition:: 引用接口

        - **POST** ``/reconciliation/get_task_list``
    """
    #: pov条件
    fields: Optional[Any]
    #: 排序
    orderType: Optional[OrderType]
    #: 页码
    pageNum: Optional[int]
    #: 每页个数
    pageSize: Optional[int]
    #: 对账元素
    reconElement: Optional[ElementBaseInfoParam]
    #: 匹配编码
    taskStatus: Optional[str]


class RctDO(BaseModel):
    #: baseAuto
    baseAuto: Optional[int]
    #: baseMnl
    baseMnl: Optional[int]
    #: baseNot
    baseNot: Optional[int]
    #: baseProportion
    baseProportion: Optional[str]
    #: baseTotal
    baseTotal: Optional[int]
    #: baseUn
    baseUn: Optional[int]
    #: cprAuto
    cprAuto: Optional[int]
    #: cprMnl
    cprMnl: Optional[int]
    #: cprNot
    cprNot: Optional[int]
    #: cprProportion
    cprProportion: Optional[str]
    #: cprTotal
    cprTotal: Optional[int]
    #: cprUn
    cprUn: Optional[int]
    #: dsBatchId
    dsBatchId: Optional[str]
    #: lastExecStatus
    lastExecStatus: Optional[str]
    #: lastRunTime
    lastRunTime: Optional[str]
    #: rcTaskId
    rcTaskId: Optional[str]
    #: rcTaskName
    rcTaskName: Optional[str]
    #: rcTaskStatus
    rcTaskStatus: Optional[str]
    #: ruleInfo
    ruleInfo: Optional[str]


class ReconSignByHand(BaseModel):
    """Recon Sign By Hand

    .. admonition:: 引用接口

        - **POST** ``/recon-cfg/mark-by-hand``
    """
    #: 选择的基础数据ids
    baseDataIds: Optional[List[str]]
    #: 选择的对比数据ids
    cprDataIds: Optional[List[str]]
    #: 说明
    description: Optional[str]
    #: 附件对应的id,多个英文逗号分割
    enclosures: Optional[str]
    #: 匹配批次ID
    rcTaskId: Optional[str]
    #: 匹配原因
    reason: Optional[str]
    #: 对账元素
    reconElement: Optional[ElementBaseInfoParam]
    #: 操作类型: 4 手工匹配  6 暂挂 5 不参与匹配
    type: Optional[str]


class ReconciliationExecDto(BaseModel):
    """Reconciliation Exec Dto

    .. admonition:: 引用接口

        - **POST** ``/reconciliationExecution/reconciliation``
    """
    #: 对账元素
    elementBaseInfoParam: ElementBaseInfoParam
    #: 前端传入的参数
    params: List[AccountInfoParam]
    #: pov信息
    povParams: Any
    #: 对账任务id，不为空表示执行旧的对账
    rcTaskId: Optional[str]
    #: 对账任务名称，对账id为空，用来新建对账任务
    rcTaskName: Optional[str]

class ReconciliationExecCreate(BaseModel):
    """Reconciliation Exec Create

    .. admonition:: 引用接口

        - **POST** ``/reconciliationExecution/create``
    """
    #: 创建成功后是否自动执行
    autoRunning: bool
    #: 对账元素
    elementBaseInfoParam: ElementBaseInfoParam
    #: 前端传入的参数
    params: List[AccountInfoParam]
    #: pov信息
    povParams: Any
    #: 对账任务id，不为空表示执行旧的对账
    rcTaskId: Optional[str]
    #: 对账任务名称，对账id为空，用来新建对账任务
    rcTaskName: Optional[str]

class CancelItem(BaseModel):
    """Cancel Item

    .. admonition:: 引用接口

        - **POST** ``/data_get/cancel_ds``
    """
    #: 批次号
    dsId: Optional[str]
    #: 批次号
    dsIds: Optional[str]
    #: 基础元素
    elementBaseInfoParamData: Optional[ElementBaseInfoParam]


class CancelReconMatch(BaseModel):
    """Cancel Recon Match

    .. admonition:: 引用接口

        - **POST** ``/recon-cfg/cancel_recon_match``
    """
    #: 匹配编码列表
    matchIds: Optional[List[str]]
    #: 对账任务ID
    rcTaskId: Optional[str]
    #: 对账元素
    reconElement: Optional[ElementBaseInfoParam]


class CancelSignByHand(BaseModel):
    """Cancel Sign By Hand

    .. admonition:: 引用接口

        - **POST** ``/recon-cfg/cancel-by-hand``
    """
    #: 选择的基础数据ids
    baseDataIds: Optional[List[str]]
    #: 选择的对比数据ids
    cprDataIds: Optional[List[str]]
    #: 对账任务ID
    rcTaskId: Optional[str]
    #: 对账元素
    reconElement: Optional[ElementBaseInfoParam]
    #: 操作类型: 0 取消挂起  1 取消不参与匹配
    type: Optional[int]


class ConfirmItem(BaseModel):
    """Confirm Item

    .. admonition:: 引用接口

        - **POST** ``/data_get/confirm_ds``
        - **POST** ``/data_get/confirm_ds_batch``
    """
    #: 批次号
    dsId: Optional[str]
    #: 批次号
    dsIds: Optional[str]
    #: 基础元素
    elementBaseInfoParamData: Optional[ElementBaseInfoParam]


class DeleteDsItem(BaseModel):
    """Delete Ds Item

    .. admonition:: 引用接口

        - **POST** ``/data_get/delete_ds``
        - **POST** ``/data_get/delete_ds_batch``
    """
    #: 批次号
    dsId: Optional[str]
    #: 批次号
    dsIds: Optional[str]
    #: 基础元素
    elementBaseInfoParamData: Optional[ElementBaseInfoParam]


class DeleteTaskItem(BaseModel):
    """Delete Task Item

    .. admonition:: 引用接口

        - **POST** ``/reconciliation/delete_task``
    """
    #: 批次id
    dsBatchId: Optional[str]
    #: 批次id集合
    dsBatchIds: Optional[List[str]]
    #: 任务id集合
    rcTaskIds: Optional[List[str]]
    #: 对账元素
    reconElement: Optional[ElementBaseInfoParam]


class PageInfoRctDO(BaseModel):
    #: endRow
    endRow: Optional[int]
    #: hasNextPage
    hasNextPage: Optional[bool]
    #: hasPreviousPage
    hasPreviousPage: Optional[bool]
    #: isFirstPage
    isFirstPage: Optional[bool]
    #: isLastPage
    isLastPage: Optional[bool]
    #: list
    list: Optional[List[RctDO]]
    #: navigateFirstPage
    navigateFirstPage: Optional[int]
    #: navigateLastPage
    navigateLastPage: Optional[int]
    #: navigatePages
    navigatePages: Optional[int]
    #: navigatepageNums
    navigatepageNums: Optional[List[int]]
    #: nextPage
    nextPage: Optional[int]
    #: pageNum
    pageNum: Optional[int]
    #: pageSize
    pageSize: Optional[int]
    #: pages
    pages: Optional[int]
    #: prePage
    prePage: Optional[int]
    #: size
    size: Optional[int]
    #: startRow
    startRow: Optional[int]
    #: total
    total: Optional[int]



