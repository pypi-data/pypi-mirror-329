"""
Models used by /approval-process-server1-0

generated by model_code_gen.py
  - **filename** : ``approval_process.py``
  - **json timestamp** : ``2022-06-27 17:44:05``
"""


from .base import BaseModel
from typing import List, Optional, Union
from pydantic import Field


__all__ = [
    'ApprovalButton',
    'DataTableColumnDTO',
    'DataTableInfoDTO',
    'DimensionMemberForOperatorDto',
    'DimensionMemberVo',
    'ElementFixInfoDTO',
    'ErrorTips',
    'InitOperationDto',
    'OperationDto',
    'OperationRecordDto',
    'OperationRecordVo',
    'PrimaryKeyByDimensionMemberDto',
    'ProcessControlInfoDto',
    'ProcessControlInfoVo',
    'ProcessRoleDto',
    'ProcessTargetStatusVo',
    'QueryOperationAuthorityDto',
    'QueryOperationOperatorDto',
    'QueryRecordDto',
    'RecordDeleteDto',
    'RecordDeleteVo',
    'RoleMessageDto',
    'SmartList',
    'SmartListInfo',
    'SmartListUd',
    'SmartListVo',
    'SmartlistValueDto',
    'UserDto',
    'ApprovalRecordVo',
    'CustomOperation',
    'CustomOperationVo',
    'DataTableBasicDTO',
    'NextOperationOperatorVo',
    'PrimaryKeyByDimensionDto',
    'ProcessSmartlistDto',
    'QueryOperationOperatorByDimensionDto',
    'RoleDto',
    'SmartListSaveForm',
    'SmartListSaveFormVo',
    'ApprovalRecordTableVo',
    'ProcessOperationDto',
    'ProcessOperationVo',
    'ProcessRoleVo',
    'NextOperationBacthVo',
    'NextOperationVo',
    'ProcessConfigBasicsVo',
    'ProcessInfoDto',
    'ProcessInfoVo',
    'ProcessTargetStatusAndOperatorBatchVo',
    'ProcessTargetStatusAndOperatorVo',
    'ProcessConfigureDto',
    'ProcessConfigureVo'
]


class ApprovalButton(BaseModel):
    #: 操作描述
    description: str
    #: 操作id
    id: str
    #: 操作是否为提交
    isSubmit: Optional[bool]
    #: 操作名称
    name: str


class DataTableColumnDTO(BaseModel):
    #: 创建时间
    createTime: Optional[str]
    #: 创建者
    creator: Optional[str]
    #: 数据表基本信息的id值
    datatableId: str
    #: 数据表名称(简名)
    datatableName: str
    #: 字段的默认值
    defaultValue: Optional[str]
    #: 字段的描述信息
    description: Optional[str]
    #: 最后一次更新的时间
    lastModifyTime: Optional[str]
    #: 最后一次编辑的用户
    lastModifyUser: Optional[str]
    #: 字段长度(datatime类型不用传值)
    length: str
    #: 字段名称
    name: str
    #: 字段对应的排序信息
    sort: int
    #: 字段类型
    type: str
    #: 唯一key
    uniqueKey: Optional[str]
    #: 是否可以为空
    whetherEmpty: Optional[bool]
    #: 是否自增
    whetherIncrement: Optional[bool]
    #: 是否唯一
    whetherOnly: Optional[bool]
    #: 是否为主键
    whetherPrimary: Optional[bool]
    #: 是否为系统字段
    whetherSystemColumn: Optional[bool]


class DataTableInfoDTO(BaseModel):
    #: 实际表名
    actualTableName: Optional[str]
    #: 创建时间
    createTime: Optional[str]
    #: 创建者
    creator: Optional[str]
    #: deleteFlag
    deleteFlag: Optional[bool]
    #: 多语言描述信息
    description: Optional[dict]
    #: 数据表id
    id: str
    #: 最后一次编辑的时间
    lastModifyTime: Optional[str]
    #: 最后一次编辑的用户
    lastModifyUser: Optional[str]
    #: 数据表名称(简名)
    name: str
    #: parentId
    parentId: Optional[str]


class DimensionMemberForOperatorDto(BaseModel):
    #: 维度名
    dimensionName: Optional[str]
    #: 元素类型
    elementType: Optional[str]
    #: 文件夹id
    folderId: Optional[str]
    #: 权限方案配置中的维度序号，1-5
    line: Optional[int]
    #: 路径
    path: Optional[str]


class DimensionMemberVo(BaseModel):
    #: 维度成员
    dimensionMember: Optional[str]
    #: 权限方案配置中的维度序号，1-5
    line: Optional[int]


class ElementFixInfoDTO(BaseModel):
    #: absoluteTag
    absoluteTag: Optional[bool]
    #: elementName
    elementName: Optional[str]
    #: elementType
    elementType: Optional[str]
    #: folderId
    folderId: Optional[str]
    #: path
    path: Optional[str]
    #: relativePath
    relativePath: Optional[str]
    #: serverName
    serverName: Optional[str]


class ErrorTips(BaseModel):
    #: 错误字段
    tipKey: Optional[str]
    #: 错误描述
    tipValue: Optional[str]


class InitOperationDto(BaseModel):
    #: 文件夹id，folderId与path，必须传一个
    folderId: Optional[str]
    #: 路径
    path: Optional[str]
    #: 审批流名称
    pcName: str


class OperationDto(BaseModel):
    """Operation Dto

    .. admonition:: 引用接口

        - **POST** ``/process/interface/operation``
        - **POST** ``/process/interface/operation/init``
    """
    #: 文件夹id，folderId与path，必须传一个
    folderId: Optional[str]
    #: 操作
    name: str
    #: 路径
    path: Optional[str]
    #: 审批流名称
    pcName: str


class OperationRecordDto(BaseModel):
    """Operation Record Dto

    .. admonition:: 引用接口

        - **POST** ``/process/operation/record``
    """
    #: 父文件夹id，folderId与path，必须传一个
    folderId: Optional[str]
    #: 源状态
    originStatus: Optional[str]
    #: 路径
    path: Optional[str]
    #: 审批流名称
    pcName: str
    #: 业务主键字段(key为业务主键的key,value为业务主键对应的值)
    primaryKeyValue: dict
    #: 操作id
    processOperationId: str
    #: 审批备注
    remark: Optional[str]
    #: 角色(全部角色传-1)
    roles: List[str]
    #: 是否跳过后置操作
    skipPost: Optional[bool]
    #: 是否跳过前置操作
    skipPre: Optional[bool]


class OperationRecordVo(BaseModel):
    """Operation Record Vo

    .. admonition:: 引用接口

        - **POST** ``/process/operation/record`` (Response: 200)
    """
    #: 错误信息
    errors: Optional[List[dict]]
    #: 操作结果
    success: bool
    #: 警告信息
    warnings: Optional[List[dict]]


class PrimaryKeyByDimensionMemberDto(BaseModel):
    #: 权限方案配置中的维度序号，1-5
    line: int
    #: 维度成员
    member: str


class ProcessControlInfoDto(BaseModel):
    #: 审批记录表表元素类型
    approvalRecordTableElementType: Optional[str]
    #: 审批记录表表父文件夹id
    approvalRecordTableFolderId: Optional[str]
    #: 审批记录表表名
    approvalRecordTableName: Optional[str]
    #: 审批记录表表路径
    approvalRecordTablePath: Optional[str]
    #: 描述
    descriptionMap: Optional[dict]
    #: 元素名称
    elementName: str
    #: 父文件夹id
    folderId: str
    #: 组件id
    moduleId: str
    #: 元素路径
    path: Optional[str]
    #: 权限方案元素类型
    rsElementType: str
    #: 权限方案父文件夹id
    rsFolderId: str
    #: 权限方案名称
    rsName: str
    #: 权限方案路径
    rsPath: str
    #: 审批流状态对应的smartlist的name
    statusSmartlist: str
    #: 前端样式参数
    style: Optional[str]


class ProcessControlInfoVo(BaseModel):
    #: 审批记录表表元素类型
    approvalRecordTableElementType: Optional[str]
    #: 审批记录表表父文件夹id
    approvalRecordTableFolderId: Optional[str]
    #: 审批记录表表名
    approvalRecordTableName: Optional[str]
    #: 审批记录表表路径
    approvalRecordTablePath: Optional[str]
    #: 描述
    descriptionMap: Optional[dict]
    #: 元素名称
    elementName: str
    #: 校验错误标记
    errorList: Optional[List[ErrorTips]]
    #: 父文件夹id
    folderId: str
    #: 组件id
    moduleId: str
    #: 元素路径
    path: Optional[str]
    #: 权限方案元素类型
    rsElementType: str
    #: 权限方案父文件夹id
    rsFolderId: str
    #: 权限方案名称
    rsName: str
    #: 权限方案路径
    rsPath: str
    #: 审批流状态对应的smartlist的name
    statusSmartlist: str
    #: 前端样式参数
    style: Optional[str]


class ProcessRoleDto(BaseModel):
    """Process Role Dto

    .. admonition:: 引用接口

        - **POST** ``/process/interface/get-action``
    """
    #: 文件夹id，folderId与path，必须传一个
    folderId: Optional[str]
    #: 路径
    path: Optional[str]
    #: 审批流名称
    pcName: str
    #: 角色
    role: List[str]


class ProcessTargetStatusVo(BaseModel):
    """Process Target Status Vo

    .. admonition:: 引用接口

        - **GET** ``/process/interface/operation/target-status`` (Response: 200)
    """
    #: 元素名称
    elementName: str
    #: 父文件夹id
    folderId: str
    #: 目标状态
    targetStatus: Optional[str]


class QueryOperationAuthorityDto(BaseModel):
    """Query Operation Authority Dto

    .. admonition:: 引用接口

        - **POST** ``/process/interface/operation/roles-status``
    """
    #: 审批流父文件夹id，folderId与path，必须传一个
    folderId: Optional[str]
    #: 审批流名称
    name: str
    #: 源状态
    originStatus: str
    #: 审批流父路径
    path: Optional[str]
    #: 角色
    roles: List[str]


class QueryOperationOperatorDto(BaseModel):
    """Query Operation Operator Dto

    .. admonition:: 引用接口

        - **POST** ``/process/interface/operation/operator``
    """
    #: 父文件夹id，folderId与path，必须传一个
    folderId: Optional[str]
    #: 状态
    originStatus: str
    #: 路径
    path: Optional[str]
    #: 审批流名称
    pcName: str
    #: 主键字段
    primaryKeyValue: dict


class QueryRecordDto(BaseModel):
    """Query Record Dto

    .. admonition:: 引用接口

        - **POST** ``/process/operation/get-record``
    """
    #: 父文件夹id，folderId与path，必须传一个
    folderId: Optional[str]
    #: 路径
    path: Optional[str]
    #: 审批流名称
    pcName: str
    #: 主键字段
    primaryKeyValue: dict
    #: 角色(全部角色传-1)
    roles: Optional[List[str]]


class RecordDeleteDto(BaseModel):
    """Record Delete Dto

    .. admonition:: 引用接口

        - **POST** ``/process/operation/delete/record``
        - **POST** ``/process/operation/delete/record/batch``
    """
    #: 父文件夹id，folderId与path，必须传一个
    folderId: Optional[str]
    #: 路径
    path: Optional[str]
    #: 审批流名称
    pcName: str
    #: 主键字段
    primaryKeyValue: dict


class RecordDeleteVo(BaseModel):
    """Record Delete Vo

    .. admonition:: 引用接口

        - **POST** ``/process/operation/delete/record/batch`` (Response: 200)
    """
    #: 错误信息
    error: Optional[str]
    #: 父文件夹id，folderId与path，必须传一个
    folderId: Optional[str]
    #: 路径
    path: Optional[str]
    #: 审批流名称
    pcName: str
    #: 主键字段
    primaryKeyValue: dict
    #: 删除结果
    success: bool


class RoleMessageDto(BaseModel):
    #: 描述
    description: Optional[dict]
    #: 说明
    instruction: Optional[dict]
    #: 名称
    name: str


class SmartList(BaseModel):
    #: 描述
    desc: Optional[dict]
    #: 值列表成员唯一标识
    key: Optional[str]
    #: 排序字段
    sortId: Optional[int]
    #: 状态
    status: Optional[bool]
    #: 成员值
    subjectValue: str
    #: 自定义属性值1
    ud1: Optional[str]
    #: ud10
    ud10: Optional[str]
    #: ud11
    ud11: Optional[str]
    #: ud12
    ud12: Optional[str]
    #: ud13
    ud13: Optional[str]
    #: ud14
    ud14: Optional[str]
    #: ud15
    ud15: Optional[str]
    #: ud16
    ud16: Optional[str]
    #: ud17
    ud17: Optional[str]
    #: ud18
    ud18: Optional[str]
    #: ud19
    ud19: Optional[str]
    #: ud2
    ud2: Optional[str]
    #: ud20
    ud20: Optional[str]
    #: ud21
    ud21: Optional[str]
    #: ud22
    ud22: Optional[str]
    #: ud23
    ud23: Optional[str]
    #: ud24
    ud24: Optional[str]
    #: ud25
    ud25: Optional[str]
    #: ud26
    ud26: Optional[str]
    #: ud27
    ud27: Optional[str]
    #: ud28
    ud28: Optional[str]
    #: ud29
    ud29: Optional[str]
    #: ud3
    ud3: Optional[str]
    #: ud30
    ud30: Optional[str]
    #: ud4
    ud4: Optional[str]
    #: ud5
    ud5: Optional[str]
    #: ud6
    ud6: Optional[str]
    #: ud7
    ud7: Optional[str]
    #: ud8
    ud8: Optional[str]
    #: ud9
    ud9: Optional[str]


class SmartListInfo(BaseModel):
    #: 描述
    desc: Optional[dict]
    #: 值列表id
    id: Optional[str]
    #: 值列表名称
    name: str


class SmartListUd(BaseModel):
    #: 状态
    active: Optional[bool]
    #: 描述
    decs: Optional[dict]
    #: 自定义属性名称
    udName: Optional[str]


class SmartListVo(BaseModel):
    #: 描述
    desc: Optional[dict]
    #: 校验错误标记
    errorList: Optional[List[ErrorTips]]
    #: 值列表成员唯一标识
    key: Optional[str]
    #: 排序字段
    sortId: Optional[int]
    #: 状态
    status: Optional[bool]
    #: 成员值
    subjectValue: str
    #: 自定义属性值1
    ud1: Optional[str]
    #: ud10
    ud10: Optional[str]
    #: ud11
    ud11: Optional[str]
    #: ud12
    ud12: Optional[str]
    #: ud13
    ud13: Optional[str]
    #: ud14
    ud14: Optional[str]
    #: ud15
    ud15: Optional[str]
    #: ud16
    ud16: Optional[str]
    #: ud17
    ud17: Optional[str]
    #: ud18
    ud18: Optional[str]
    #: ud19
    ud19: Optional[str]
    #: ud2
    ud2: Optional[str]
    #: ud20
    ud20: Optional[str]
    #: ud21
    ud21: Optional[str]
    #: ud22
    ud22: Optional[str]
    #: ud23
    ud23: Optional[str]
    #: ud24
    ud24: Optional[str]
    #: ud25
    ud25: Optional[str]
    #: ud26
    ud26: Optional[str]
    #: ud27
    ud27: Optional[str]
    #: ud28
    ud28: Optional[str]
    #: ud29
    ud29: Optional[str]
    #: ud3
    ud3: Optional[str]
    #: ud30
    ud30: Optional[str]
    #: ud4
    ud4: Optional[str]
    #: ud5
    ud5: Optional[str]
    #: ud6
    ud6: Optional[str]
    #: ud7
    ud7: Optional[str]
    #: ud8
    ud8: Optional[str]
    #: ud9
    ud9: Optional[str]


class SmartlistValueDto(BaseModel):
    #: 多语言描述
    desc: Optional[dict]
    #: 成员值
    value: Optional[str]


class UserDto(BaseModel):
    #: 是否管理员标识
    adminTag: Optional[str]
    #: 头像
    avatar: Optional[str]
    #: 邮箱
    email: Optional[str]
    #: 手机号
    mobilePhone: Optional[str]
    #: 昵称
    nickName: Optional[str]
    #: 状态
    status: Optional[str]
    #: 用户id
    userId: Optional[str]
    #: 用户名
    userName: Optional[str]


class ApprovalRecordVo(BaseModel):
    """Approval Record Vo

    .. admonition:: 引用接口

        - **POST** ``/process/operation/get-record`` (Response: 200)
    """
    #: 按钮
    buttons: List[ApprovalButton]
    #: 操作是否为提交
    isSubmit: Optional[bool]
    #: 行号
    line_no: int
    #: 操作时间
    operate_time: str
    #: 操作人
    operate_user: str
    #: 审批备注
    pc_remark: Optional[str]
    #: 业务主键字段(key为业务主键的key,value为业务主键对应的值)
    primaryKeyValue: dict
    #: 审批操作描述
    process_operation_des: str
    #: 审批操作id
    process_operation_id: str
    #: 审批后的状态
    result_status: str
    #: 审批后的状态描述
    result_status_des: str
    #: 用户信息,用户不存在为null
    user_detail: Optional[UserDto]


class CustomOperation(BaseModel):
    #: 同步异步 1异步,0同步
    async_: int = Field(..., alias='async')
    #: elementDetail
    elementDetail: Optional[ElementFixInfoDTO]
    #: 父文件夹id
    elementFolderId: Optional[str]
    #: 元素名称
    elementName: Optional[str]
    #: 路径
    elementPath: Optional[str]
    #: 元素类型
    elementType: Optional[str]
    #: 前后置操作id
    id: str
    #: 操作排序
    sort: int
    #: url路径
    url: Optional[str]


class CustomOperationVo(BaseModel):
    #: 同步异步 1异步,0同步
    async_: int = Field(..., alias='async')
    #: 父文件夹id
    elementFolderId: Optional[str]
    #: elementName
    elementName: Optional[Union[ElementFixInfoDTO, str]]
    #: 路径
    elementPath: Optional[str]
    #: 元素类型
    elementType: Optional[str]
    #: 校验错误标记
    errorFlag: Optional[bool]
    #: 校验错误描述
    errorMsg: Optional[str]
    #: 前后置操作id
    id: str
    #: 操作排序
    sort: int
    #: url路径
    url: Optional[str]


class DataTableBasicDTO(BaseModel):
    #: 当前数据表的所有列
    datatableColumn: List[DataTableColumnDTO]
    #: 数据表相关信息
    datatableInfo: DataTableInfoDTO


class NextOperationOperatorVo(BaseModel):
    #: 是否所有用户
    allUsers: Optional[bool]
    #: 可执行的操作人
    operators: Optional[List[UserDto]]
    #: 维度字段
    primaryKeyValue: Optional[List[DimensionMemberVo]]


class PrimaryKeyByDimensionDto(BaseModel):
    #: 权限方案配置中的维度
    members: List[PrimaryKeyByDimensionMemberDto]


class ProcessSmartlistDto(BaseModel):
    """Process Smartlist Dto

    .. admonition:: 引用接口

        - **GET** ``/process/interface/pc-smartlist`` (Response: 200)
    """
    #: 父文件夹id
    folderId: Optional[str]
    #: 审批流name
    pcName: Optional[str]
    #: 对应值列表成员+描述
    smart: Optional[List[SmartlistValueDto]]


class QueryOperationOperatorByDimensionDto(BaseModel):
    """Query Operation Operator By Dimension Dto

    .. admonition:: 引用接口

        - **POST** ``/process/interface/operation/get-operator-by-dimensions``
    """
    #: 维度
    dimensions: List[DimensionMemberForOperatorDto]
    #: 父文件夹id，folderId与path，必须传一个
    folderId: Optional[str]
    #: 状态
    originStatus: str
    #: 路径
    path: Optional[str]
    #: 审批流名称
    pcName: str
    #: 维度字段
    primaryKeyValues: List[PrimaryKeyByDimensionDto]


class RoleDto(BaseModel):
    #: 是否全部角色
    allRoles: Optional[bool]
    #: 角色组
    groupInfo: Optional[List[RoleMessageDto]]
    #: 角色
    roleInfo: Optional[List[RoleMessageDto]]


class SmartListSaveForm(BaseModel):
    #: 元素类型(新建时可以为空)
    elementType: Optional[str]
    #: 父文件夹id
    folderId: str
    #: 组件id
    moduleId: Optional[str]
    #: 元素路径
    path: str
    #: 值列表成员值(多个)
    smartList: Optional[List[SmartList]]
    #: 值列表基本信息
    smartListInfo: SmartListInfo
    #: 值列表ud信息(多个)
    smartListUd: Optional[List[SmartListUd]]
    #: ADD-新建,EDIT-编辑
    type: Optional[str]


class SmartListSaveFormVo(BaseModel):
    #: 元素类型(新建时可以为空)
    elementType: Optional[str]
    #: 校验错误标记
    errorList: Optional[List[ErrorTips]]
    #: 父文件夹id
    folderId: str
    #: 组件id
    moduleId: Optional[str]
    #: 元素路径
    path: str
    #: 值列表成员值(多个)
    smartList: Optional[List[SmartListVo]]
    #: 值列表基本信息
    smartListInfo: SmartListInfo
    #: 值列表ud信息(多个)
    smartListUd: Optional[List[SmartListUd]]
    #: ADD-新建,EDIT-编辑
    type: Optional[str]


class ApprovalRecordTableVo(BaseModel):
    """Approval Record Table Vo

    .. admonition:: 引用接口

        - **GET** ``/process/operation/record-table`` (Response: 200)
    """
    #: 审批记录表信息
    dataTableBasic: Optional[DataTableBasicDTO]
    #: 审批记录表父文件夹id
    folderId: Optional[str]
    #: 审批记录表名称
    name: Optional[str]
    #: 审批记录表路径
    path: Optional[str]


class ProcessOperationDto(BaseModel):
    """Process Operation Dto

    .. admonition:: 引用接口

        - **POST** ``/process/interface/operation`` (Response: 200)
        - **POST** ``/process/interface/operation/init`` (Response: 200)
        - **POST** ``/process/interface/operation/roles-status`` (Response: 200)
    """
    #: 描述
    descriptionMap: Optional[dict]
    #: 操作id,0为初始操作
    id: str
    #: 操作是否为提交
    isSubmit: Optional[bool]
    #: 操作名称
    name: str
    #: 源状态值 逗号分隔
    originStatusList: Optional[str]
    #: 后置操作
    postOpe: Optional[List[CustomOperation]]
    #: 前置操作
    preOpe: Optional[List[CustomOperation]]
    #: 角色
    role: RoleDto
    #: 目标状态值
    targetStatus: str


class ProcessOperationVo(BaseModel):
    #: 描述
    descriptionMap: Optional[dict]
    #: 校验错误标记
    errorList: Optional[List[ErrorTips]]
    #: 操作id,0为初始操作
    id: str
    #: 操作是否为提交
    isSubmit: Optional[bool]
    #: 操作名称
    name: str
    #: 源状态值 逗号分隔
    originStatusList: Optional[str]
    #: 后置操作
    postOpe: Optional[List[CustomOperationVo]]
    #: 前置操作
    preOpe: Optional[List[CustomOperationVo]]
    #: 角色
    role: RoleDto
    #: 目标状态值
    targetStatus: str


class ProcessRoleVo(BaseModel):
    """Process Role Vo

    .. admonition:: 引用接口

        - **POST** ``/process/interface/get-action`` (Response: 200)
    """
    #: 文件夹id
    folderId: str
    #: 操作信息
    operation: List[ProcessOperationDto]
    #: 审批流名称
    pcName: str
    #: 角色
    roleName: List[str]


class NextOperationBacthVo(BaseModel):
    #: 下一步的可行操作
    operation: Optional[ProcessOperationDto]
    #: 对应的可执行操作人
    operators: Optional[List[NextOperationOperatorVo]]


class NextOperationVo(BaseModel):
    #: 是否所有用户
    allUsers: Optional[bool]
    #: 下一步的可行操作
    operation: Optional[ProcessOperationDto]
    #: 可执行的操作人
    operators: Optional[List[UserDto]]


class ProcessConfigBasicsVo(BaseModel):
    """Process Config Basics Vo

    .. admonition:: 引用接口

        - **GET** ``/process/configure/basics`` (Response: 200)
    """
    #: 审批流信息
    controlInfo: ProcessControlInfoDto
    #: 审批流操作信息
    operationInfo: List[ProcessOperationDto]


class ProcessInfoDto(BaseModel):
    #: 审批流信息
    controlInfo: ProcessControlInfoDto
    #: 审批流操作信息
    operationInfo: List[ProcessOperationDto]
    #: ADD-新建,EDIT-编辑
    type: Optional[str]


class ProcessInfoVo(BaseModel):
    #: 审批流信息
    controlInfo: ProcessControlInfoVo
    #: 审批流操作信息
    operationInfo: List[ProcessOperationVo]
    #: ADD-新建,EDIT-编辑
    type: Optional[str]


class ProcessTargetStatusAndOperatorBatchVo(BaseModel):
    """Process Target Status And Operator Batch Vo

    .. admonition:: 引用接口

        - **POST** ``/process/interface/operation/get-operator-by-dimensions`` (Response: 200)
    """
    #: 元素名称
    elementName: str
    #: 父文件夹id
    folderId: str
    #: 下一步的可行操作
    nextOperations: Optional[List[NextOperationBacthVo]]
    #: 路径
    path: str


class ProcessTargetStatusAndOperatorVo(BaseModel):
    """Process Target Status And Operator Vo

    .. admonition:: 引用接口

        - **POST** ``/process/interface/operation/operator`` (Response: 200)
    """
    #: 元素名称
    elementName: str
    #: 父文件夹id
    folderId: str
    #: 下一步的可行操作
    nextOperations: Optional[List[NextOperationVo]]
    #: 路径
    path: str


class ProcessConfigureDto(BaseModel):
    """Process Configure Dto

    .. admonition:: 引用接口

        - **POST** ``/process/configure/pt``
    """
    #: 审批流内容
    processInfo: ProcessInfoDto
    #: 1为保存,0为保存前置获取影响关系,暂时写死为1
    saveType: Optional[int]
    #: 值列表内容
    smartListInfo: SmartListSaveForm


class ProcessConfigureVo(BaseModel):
    """Process Configure Vo

    .. admonition:: 引用接口

        - **GET** ``/process/configure`` (Response: 200)
    """
    #: 审批流内容
    processInfo: ProcessInfoVo
    #: 1为保存,0为保存前置获取影响关系,暂时写死为1
    saveType: Optional[int]
    #: 值列表内容
    smartListInfo: Optional[SmartListSaveFormVo]



