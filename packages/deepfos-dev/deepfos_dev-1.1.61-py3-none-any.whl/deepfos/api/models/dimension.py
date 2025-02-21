"""
Models used by /dimension-server1-0

generated by model_code_gen.py
  - **filename** : ``dimension.py``
  - **json timestamp** : ``2022-09-02 19:26:55``
"""


from deepfos.api.models.base import BaseModel
from typing import List, Optional, Union, Any, Dict
from pydantic import Field


__all__ = [
    'AroundDimensionDto',
    'DateDimensionDto',
    'DimensionDescriptionDto',
    'DimensionDescriptionReDto',
    'DimensionExpressAndMemberDto',
    'DimensionExpressDto',
    'DimensionExpressExistsResult',
    'DimensionInfoSw',
    'DimensionMemberBean',
    'DimensionMemberByLevelDto',
    'DimensionMemberByNameFunctionDto',
    'DimensionMemberByParentDto',
    'DimensionMemberDto',
    'DimensionMemberLevelAuthorizedDto',
    'DimensionMemberListDto',
    'DimensionMemberOperationSw',
    'DimensionMemberQuerySw',
    'DimensionMembersDto',
    'ElementBaseInfoDto',
    'ElementBaseInfoParam',
    'ElementBaseQueryParam',
    'ElementDetailVo',
    'ElementQueryBaseDto',
    'Error',
    'MemberInExpressAndRsDto',
    'MemberInExpressAndRsResult',
    'MoreLevelMemberDto',
    'OpenErrorDto',
    'PeriodConfig',
    'PeriodConfigDto',
    'RelationDimension',
    'RelationVo',
    'ResultObj',
    'UdValueByExpressDto',
    'ViewDto',
    'ViewExpressDto',
    'YearPeriodDto',
    'AllYearPeriodOfSceanrioDto',
    'Dimension',
    'DimensionChangeSaveResult',
    'DimensionMemberChangeSaveSw',
    'DimensionMemberSaveDto',
    'DimensionRelationVo',
    'UpdateViewMemberSw'
]


class AroundDimensionDto(BaseModel):
    """Around Dimension Dto

    .. admonition:: 引用接口

        - **POST** ``/dimension/custom/get-around-dimension``
    """
    #: 查询表达式
    dimension_express: Optional[str]
    #: folderId
    folderId: Optional[str]
    #: path
    path: Optional[str]
    #: resultString
    resultString: Optional[str]
    #: 排序:0-正序,1-倒叙
    reverse_order: Optional[str]


class DateDimensionDto(BaseModel):
    """Date Dimension Dto

    .. admonition:: 引用接口

        - **POST** ``/dimension/query/date-dimension``
    """
    #: dimensionMemberNames
    dimensionMemberNames: Optional[str]
    #: folderId
    folderId: Optional[str]
    #: resultString
    resultString: Optional[str]


class DimensionDescriptionDto(BaseModel):
    """Dimension Description Dto

    .. admonition:: 引用接口

        - **POST** ``/dimension/custom/get-dimension-description``
    """
    #: 维度表达式
    express: Optional[str]
    #: folderId
    folderId: Optional[str]
    #: 维度成员名
    name: Optional[str]
    #: path
    path: Optional[str]


class DimensionDescriptionReDto(BaseModel):
    #: description
    description: Optional[str]
    #: 维度表达式
    express: Optional[str]
    #: folderId
    folderId: Optional[str]
    #: 维度成员名
    name: Optional[str]
    #: path
    path: Optional[str]


class DimensionExpressAndMemberDto(BaseModel):
    """Dimension Express And Member Dto

    .. admonition:: 引用接口

        - **POST** ``/dimension/check/member/express/contains``
        - **POST** ``/dimension/check/member/multi/express/contains``
    """
    #: 维度名
    dimensionName: Optional[str]
    #: 维度表达式
    express: Optional[str]
    #: folderId
    folderId: Optional[str]
    #: 维度成员列表
    members: Optional[List[str]]
    #: 是否需要返回存在的成员列表，此参数可不传
    needExistMember: Optional[bool]
    #: path
    path: Optional[str]


class DimensionExpressDto(BaseModel):
    """Dimension Express Dto

    .. admonition:: 引用接口

        - **POST** ``/dimension/check/member/exists/batch/express``
        - **POST** ``/dimension/check/member/exists/express``
    """
    #: 维度名
    dimensionName: Optional[str]
    #: 维度表达式
    express: Optional[str]
    #: folderId
    folderId: Optional[str]
    #: path
    path: Optional[str]


class DimensionExpressExistsResult(BaseModel):
    #: 维度名
    dimensionName: Optional[str]
    #: 错误信息，报错的时候有值
    errorMessage: Optional[str]
    #: 存在的维度成员,needExistMember为true时返回
    existingMembers: Optional[List[str]]
    #: 维度表达式
    express: Optional[str]
    #: folderId
    folderId: Optional[str]
    #: 是否都存在(于表达式)
    isAllExists: Optional[bool]
    #: 不存在的维度成员,isAllExists为false时有值
    nonexistentMembers: Optional[List[str]]
    #: path
    path: Optional[str]


class DimensionInfoSw(BaseModel):
    #: 文件夹id
    folderId: Optional[str]
    #: 值为1只进行校验，不保存
    isOnlyCheck: Optional[str]
    #: 维度名
    name: Optional[str]
    #: 元素路径
    path: Optional[str]


class DimensionMemberBean(BaseModel):
    #: 支付类型,科目类型特有
    accounttype: Optional[str]
    #: 实际天数,期间类型特有
    actualDate: Optional[str]
    #: 实际年份,年份类型特有
    actualYear: Optional[str]
    #: 比重
    aggweight: Optional[float]
    #: 数据长度,科目类型特有
    dataLength: Optional[int]
    #: 数据精度,科目类型特有
    dataPrecision: Optional[int]
    #: 数据类型,科目类型特有
    datatype: Optional[str]
    #: 结束期间
    end_period: Optional[str]
    #: 结束年份
    end_year: Optional[str]
    #: 流类型,科目类型特有
    flowtype: Optional[str]
    #: 公式
    formula: Optional[str]
    #: 半年,期间类型特有
    halfyear: Optional[str]
    #: 维度成员id
    id: Optional[int]
    #: 父节点,科目类型特有
    inputOnParentNode: Optional[bool]
    #: 自上而下,版本类型特有
    isTopDown: Optional[bool]
    #: 是否生效
    is_active: Optional[bool]
    #: 是否叶子节点
    is_base: Optional[bool]
    #: 是否计算
    is_calculated: Optional[bool]
    #: 是否模块化
    is_modula: Optional[bool]
    #: 层级
    level: Optional[int]
    #: 本位币,实体类型特有
    local_currency: Optional[str]
    #: 月,期间类型特有
    month: Optional[str]
    #: 多语言描述
    multilingual: Optional[dict]
    #: 成员编码
    name: Optional[str]
    #: 父节点编码
    parent_name: Optional[str]
    #: 期间级别,期间类型特有
    period_level: Optional[int]
    #: 季度,期间类型特有
    quarter: Optional[str]
    #: 是否共享节点
    sharedmember: Optional[bool]
    #: 排序字段
    sort_col: Optional[str]
    #: 开始期间
    start_period: Optional[str]
    #: 开始年份
    start_year: Optional[str]
    #: 自定义ud属性
    #: ud1
    ud1: Optional[str]
    #: ud2
    ud2: Optional[str]
    #: ud3
    ud3: Optional[str]
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
    #: ud30
    ud30: Optional[str]
    #: ud31
    ud31: Optional[str]
    #: ud32
    ud32: Optional[str]
    #: ud33
    ud33: Optional[str]
    #: ud34
    ud34: Optional[str]
    #: ud35
    ud35: Optional[str]
    #: ud36
    ud36: Optional[str]
    #: ud37
    ud37: Optional[str]
    #: ud38
    ud38: Optional[str]
    #: ud39
    ud39: Optional[str]
    #: ud40
    ud40: Optional[str]
    #: ud41
    ud41: Optional[str]
    #: ud42
    ud42: Optional[str]
    #: ud43
    ud43: Optional[str]
    #: ud44
    ud44: Optional[str]
    #: ud45
    ud45: Optional[str]
    #: ud46
    ud46: Optional[str]
    #: ud47
    ud47: Optional[str]
    #: ud48
    ud48: Optional[str]
    #: ud49
    ud49: Optional[str]
    #: ud50
    ud50: Optional[str]
    #: ud51
    ud51: Optional[str]
    #: ud52
    ud52: Optional[str]
    #: ud53
    ud53: Optional[str]
    #: ud54
    ud54: Optional[str]
    #: ud55
    ud55: Optional[str]
    #: ud56
    ud56: Optional[str]
    #: ud57
    ud57: Optional[str]
    #: ud58
    ud58: Optional[str]
    #: ud59
    ud59: Optional[str]
    #: ud60
    ud60: Optional[str]
    #: 周,期间类型特有
    week: Optional[str]


class DimensionMemberByLevelDto(BaseModel):
    """Dimension Member By Level Dto

    .. admonition:: 引用接口

        - **POST** ``/dimension/custom/get-dimension-member-by-level``
    """
    #: 维度表达式
    dimensionMemberNames: Optional[str]
    #: folderId
    folderId: Optional[str]
    #: 返回数据格式:0-list,1-map
    outFormat: Optional[str]
    #: path
    path: Optional[str]
    #: resultString
    resultString: Optional[str]
    #: 排序:0-正序,1-倒叙
    reverse_order: Optional[str]
    #: 展示层级
    showLevel: Optional[str]


class DimensionMemberByNameFunctionDto(BaseModel):
    """Dimension Member By Name Function Dto

    .. admonition:: 引用接口

        - **POST** ``/dimension/query/select-dimension-member-by-name-function``
        - **POST** ``/dimension/query/select-dimension-member-by-name-function-batch``
    """
    #: 是否校验表达式
    check_express: Optional[str]
    #: 维度表达式
    dimensionMemberNames: Optional[str]
    #: 是否去重
    duplicate: Optional[str]
    #: folderId
    folderId: Optional[str]
    #: 是否忽略不存在的维度成员
    ignoreIllegalMember: Optional[bool]
    #: 返回数据格式:0-list,1-map
    outFormat: Optional[str]
    #: path
    path: Optional[str]
    #: 返回字段
    resultString: Optional[str]
    #: 排序:0-正序,1-倒叙
    reverse_order: Optional[str]
    #: 角色方案角色
    role: Optional[str]
    #: 角色方案文件夹id
    roleFolderId: Optional[str]
    #: 角色方案路径
    rolePath: Optional[str]
    #: 角色方案角色组
    rolegroup: Optional[str]
    #: 角色方案行号
    rsMapping: Optional[int]
    #: 角色方案名
    rsName: Optional[str]
    #: 是否前端调用
    web: Optional[str]


class DimensionMemberByParentDto(BaseModel):
    """Dimension Member By Parent Dto

    .. admonition:: 引用接口

        - **POST** ``/dimension/custom/get-dimension-member-by-parent``
    """
    #: 维度表达式
    dimensionMemberNames: Optional[str]
    #: dimension_name
    dimension_name: Optional[str]
    #: folderId
    folderId: Optional[str]
    #: path
    path: Optional[str]
    #: resultString
    resultString: Optional[str]
    #: 排序:0-正序,1-倒叙
    reverse_order: Optional[str]
    #: 自定义字段名称
    ud_name: Optional[str]


class DimensionMemberDto(BaseModel):
    """Dimension Member Dto

    .. admonition:: 引用接口

        - **POST** ``/finance/dimension/check-and-save-dimension-member``
    """
    #: dimensions
    dimensions: Optional[Any]
    #: typeMap
    typeMap: Optional[Any]


class DimensionMemberLevelAuthorizedDto(BaseModel):
    """Dimension Member Level Authorized Dto

    .. admonition:: 引用接口

        - **POST** ``/dimension/query/get-authorized-dimension-member-level``
    """
    #: dimensionExpression
    dimensionExpression: Optional[str]
    #: dimensionName
    dimensionName: Optional[str]
    #: 维度name展示样式:0-维度成员名,1-维度成员描述，2-维度成员名-维度成员描述
    displayType: Optional[str]
    #: 是否返回维度信息:0-不返回,1-返回
    edit: Optional[str]
    #: folderId
    folderId: Optional[str]
    #: 当前维度成员id,返回该节点下级成员列表
    id: Optional[int]
    #: 当前维度成员名,返回该节点下级成员列表
    name: Optional[str]
    #: 父级节点是否可选:true-可选,false-不可选
    parentClick: Optional[str]
    #: path
    path: Optional[str]
    #: resultString
    resultString: Optional[str]
    #: 角色方案角色
    role: Optional[str]
    #: 角色方案文件夹id
    roleFolderId: Optional[str]
    #: 角色方案路径
    rolePath: Optional[str]
    #: 角色方案角色组
    rolegroup: Optional[str]
    #: 角色方案行号
    rsMapping: Optional[int]
    #: 角色方案名
    rsName: Optional[str]
    #: searchValue
    searchValue: Optional[str]


class DimensionMemberListDto(BaseModel):
    """Dimension Member List Dto

    .. admonition:: 引用接口

        - **POST** ``/dimension/custom/select-dimension-member-list``
    """
    #: folderId
    folderId: Optional[str]
    #: name
    name: Optional[str]
    #: path
    path: Optional[str]


class DimensionMemberOperationSw(BaseModel):
    #: 支付类型,科目类型特有
    accounttype: Optional[str]
    #: 实际天数,期间类型特有
    actualDate: Optional[str]
    #: 实际年份,年份类型特有
    actualYear: Optional[str]
    #: 比重
    aggweight: Optional[float]
    #: 数据长度,科目类型特有
    dataLength: Optional[int]
    #: 数据精度,科目类型特有
    dataPrecision: Optional[int]
    #: 数据类型,科目类型特有
    datatype: Optional[str]
    #: 结束期间
    end_period: Optional[str]
    #: 结束年份
    end_year: Optional[str]
    #: 流类型,科目类型特有
    flowtype: Optional[str]
    #: 公式
    formula: Optional[str]
    #: 半年,期间类型特有
    halfyear: Optional[str]
    #: 维度成员id
    id: Optional[int]
    #: 排序，指该节点在同一个父节点下的排序，从0开始
    index: Optional[int]
    #: 父节点,科目类型特有
    inputOnParentNode: Optional[bool]
    #: 自上而下,版本类型特有
    isTopDown: Optional[bool]
    #: 是否生效
    is_active: Optional[bool]
    #: 是否叶子节点
    is_base: Optional[bool]
    #: 是否计算
    is_calculated: Optional[bool]
    #: 是否模块化
    is_modula: Optional[bool]
    #: 层级
    level: Optional[int]
    #: 本位币,实体类型特有
    local_currency: Optional[str]
    #: 月,期间类型特有
    month: Optional[str]
    #: 多语言描述
    multilingual: Optional[Any]
    #: 成员编码
    name: Optional[str]
    #: 操作类型
    operation: Optional[str]
    #: 原成员编码
    origin_name: Optional[str]
    #: 原父节点编码
    origin_parent_name: Optional[str]
    #: 父节点编码
    parent_name: Optional[str]
    #: 期间级别,期间类型特有
    period_level: Optional[int]
    #: 季度,期间类型特有
    quarter: Optional[str]
    #: 是否共享节点
    sharedmember: Optional[bool]
    #: 排序字段
    sort_col: Optional[str]
    #: 开始期间
    start_period: Optional[str]
    #: 开始年份
    start_year: Optional[str]
    #: 自定义ud属性
    #: ud1
    ud1: Optional[str]
    #: ud2
    ud2: Optional[str]
    #: ud3
    ud3: Optional[str]
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
    #: ud30
    ud30: Optional[str]
    #: ud31
    ud31: Optional[str]
    #: ud32
    ud32: Optional[str]
    #: ud33
    ud33: Optional[str]
    #: ud34
    ud34: Optional[str]
    #: ud35
    ud35: Optional[str]
    #: ud36
    ud36: Optional[str]
    #: ud37
    ud37: Optional[str]
    #: ud38
    ud38: Optional[str]
    #: ud39
    ud39: Optional[str]
    #: ud40
    ud40: Optional[str]
    #: ud41
    ud41: Optional[str]
    #: ud42
    ud42: Optional[str]
    #: ud43
    ud43: Optional[str]
    #: ud44
    ud44: Optional[str]
    #: ud45
    ud45: Optional[str]
    #: ud46
    ud46: Optional[str]
    #: ud47
    ud47: Optional[str]
    #: ud48
    ud48: Optional[str]
    #: ud49
    ud49: Optional[str]
    #: ud50
    ud50: Optional[str]
    #: ud51
    ud51: Optional[str]
    #: ud52
    ud52: Optional[str]
    #: ud53
    ud53: Optional[str]
    #: ud54
    ud54: Optional[str]
    #: ud55
    ud55: Optional[str]
    #: ud56
    ud56: Optional[str]
    #: ud57
    ud57: Optional[str]
    #: ud58
    ud58: Optional[str]
    #: ud59
    ud59: Optional[str]
    #: ud60
    ud60: Optional[str]
    #: 周,期间类型特有
    week: Optional[str]


class DimensionMemberQuerySw(BaseModel):
    """Dimension Member Query Sw

    .. admonition:: 引用接口

        - **POST** ``/dimension/query/get-access-dimension-member-list``
    """
    #: 维度展示方式 0名称 1描述 2名称-描述 
    dimensionDisplay: Optional[str]
    #: 维度表达式 
    dimensionExpression: Optional[str]
    #: 维度名
    dimensionName: Optional[str]
    #: 是否去重
    duplicate: Optional[str]
    #: 启用多表达式分页
    enablePager: Optional[str]
    #: 文件夹id
    folderId: Optional[str]
    #: 维度成员id 
    id: Optional[str]
    #: 分页长度
    length: Optional[int]
    #: 是否返回成员路径
    memberPath: Optional[bool]
    #: 维度成员名
    name: Optional[str]
    #: 1：不分页 
    noPage: Optional[str]
    #: 元素路径
    path: Optional[str]
    #: 期间
    period: Optional[str]
    #: 返回字段
    resultString: Optional[str]
    #: 角色方案角色
    role: Optional[str]
    #: 角色方案文件夹id
    roleFolderId: Optional[str]
    #: 角色方案路径
    rolePath: Optional[str]
    #: 角色方案角色组
    rolegroup: Optional[str]
    #: 角色方案行号
    rsMapping: Optional[int]
    #: 角色方案名
    rsName: Optional[str]
    #: 搜索值
    searchValue: Optional[str]
    #: 分页起始
    start: Optional[int]
    #: 年份
    year: Optional[str]


class DimensionMembersDto(BaseModel):
    #: accounttype
    accounttype: Optional[str]
    #: actualDate
    actualDate: Optional[str]
    #: actualYear
    actualYear: Optional[str]
    #: aggweight
    aggweight: Optional[float]
    #: curr_level_sort
    curr_level_sort: Optional[int]
    #: dataLength
    dataLength: Optional[int]
    #: dataPrecision
    dataPrecision: Optional[int]
    #: datatype
    datatype: Optional[str]
    #: description_1
    description_1: Optional[str]
    #: description_2
    description_2: Optional[str]
    #: description_3
    description_3: Optional[str]
    #: description_4
    description_4: Optional[str]
    #: description_5
    description_5: Optional[str]
    #: description_6
    description_6: Optional[str]
    #: description_7
    description_7: Optional[str]
    #: description_8
    description_8: Optional[str]
    #: end_period
    end_period: Optional[str]
    #: end_year
    end_year: Optional[str]
    #: flowtype
    flowtype: Optional[str]
    #: formula
    formula: Optional[str]
    #: halfyear
    halfyear: Optional[str]
    #: id
    id: Optional[int]
    #: inputOnParentNode
    inputOnParentNode: Optional[bool]
    #: isTopDown
    isTopDown: Optional[bool]
    #: is_active
    is_active: Optional[bool]
    #: is_base
    is_base: Optional[bool]
    #: is_calculated
    is_calculated: Optional[bool]
    #: is_modula
    is_modula: Optional[bool]
    #: level
    level: Optional[int]
    #: local_currency
    local_currency: Optional[str]
    #: month
    month: Optional[str]
    #: multilingual
    multilingual: Optional[Any]
    #: name
    name: Optional[str]
    #: parent_id
    parent_id: Optional[str]
    #: parent_name
    parent_name: Optional[str]
    #: period_level
    period_level: Optional[str]
    #: quarter
    quarter: Optional[str]
    #: sharedmember
    sharedmember: Optional[bool]
    #: sort_col
    sort_col: Optional[str]
    #: start_period
    start_period: Optional[str]
    #: start_year
    start_year: Optional[str]
    #: 自定义ud属性
    #: ud1
    ud1: Optional[str]
    #: ud2
    ud2: Optional[str]
    #: ud3
    ud3: Optional[str]
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
    #: ud30
    ud30: Optional[str]
    #: ud31
    ud31: Optional[str]
    #: ud32
    ud32: Optional[str]
    #: ud33
    ud33: Optional[str]
    #: ud34
    ud34: Optional[str]
    #: ud35
    ud35: Optional[str]
    #: ud36
    ud36: Optional[str]
    #: ud37
    ud37: Optional[str]
    #: ud38
    ud38: Optional[str]
    #: ud39
    ud39: Optional[str]
    #: ud40
    ud40: Optional[str]
    #: ud41
    ud41: Optional[str]
    #: ud42
    ud42: Optional[str]
    #: ud43
    ud43: Optional[str]
    #: ud44
    ud44: Optional[str]
    #: ud45
    ud45: Optional[str]
    #: ud46
    ud46: Optional[str]
    #: ud47
    ud47: Optional[str]
    #: ud48
    ud48: Optional[str]
    #: ud49
    ud49: Optional[str]
    #: ud50
    ud50: Optional[str]
    #: ud51
    ud51: Optional[str]
    #: ud52
    ud52: Optional[str]
    #: ud53
    ud53: Optional[str]
    #: ud54
    ud54: Optional[str]
    #: ud55
    ud55: Optional[str]
    #: ud56
    ud56: Optional[str]
    #: ud57
    ud57: Optional[str]
    #: ud58
    ud58: Optional[str]
    #: ud59
    ud59: Optional[str]
    #: ud60
    ud60: Optional[str]
    #: week
    week: Optional[str]


class ElementBaseInfoDto(BaseModel):
    """Element Base Info Dto

    .. admonition:: 引用接口

        - **POST** ``/dimension/check/member/exists``
        - **POST** ``/dimension/check/member/exists/single``
        - **POST** ``/dimension/query/open-dimension-info-by-id``
    """
    #: elementName
    elementName: Optional[str]
    #: elementType
    elementType: Optional[str]
    #: folderId
    folderId: Optional[str]
    #: memberName
    memberName: Optional[str]
    #: memberNames
    memberNames: Optional[List[str]]
    #: moduleId
    moduleId: Optional[str]
    #: path
    path: Optional[str]


class ElementBaseInfoParam(BaseModel):
    """Element Base Info Param

    .. admonition:: 引用接口

        - **POST** ``/dimension/check/exists``
        - **POST** ``/dimension/info/initialization-tables``
        - **POST** ``/dimension/query/get-dimension-list``
    """
    #: 元素具体名称
    elementName: Optional[str]
    #: 元素类型
    elementType: Optional[str]
    #: 文件夹id
    folderId: Optional[str]
    #: 组件id
    moduleId: Optional[str]
    #: 文件夹
    path: Optional[str]


class ElementBaseQueryParam(BaseModel):
    """Element Base Query Param

    .. admonition:: 引用接口

        - **POST** ``/dimension/query/get-open-period-config``
    """
    #: 元素具体名称
    elementName: Optional[str]
    #: 元素类型
    elementType: Optional[str]
    #: 文件夹id
    folderId: Optional[str]
    #: 元素路径
    path: Optional[str]


class ElementDetailVo(BaseModel):
    #: 绝对相对标志
    absoluteTag: Optional[bool]
    #: 元素名称
    elementName: Optional[str]
    #: 元素类型
    elementType: Optional[str]
    #: 文件夹id
    folderId: Optional[str]
    #: 绝对路径
    path: Optional[str]
    #: 相对路径
    relativePath: Optional[str]
    #: 元素服务名
    serverName: Optional[str]


class ElementQueryBaseDto(BaseModel):
    """Element Query Base Dto

    .. admonition:: 引用接口

        - **POST** ``/dimension/query/get-view-by-period``
    """
    #: elementName
    elementName: Optional[str]
    #: folderId
    folderId: Optional[str]
    #: path
    path: Optional[str]
    #: showAll
    showAll: Optional[bool]


class Error(BaseModel):
    #: code
    code: Optional[str]
    #: msg
    msg: Optional[str]


class MemberInExpressAndRsDto(BaseModel):
    """Member In Express And Rs Dto

    .. admonition:: 引用接口

        - **POST** ``/dimension/check/member/multi/express-rs/contains``
    """
    #: 维度表达式
    express: Optional[str]
    #: folderId
    folderId: Optional[str]
    #: 维度成员列表
    members: Optional[List[str]]
    #: path
    path: Optional[str]
    #: 角色方案角色
    role: Optional[str]
    #: 角色方案名文件夹id
    roleFolderId: Optional[str]
    #: 角色方案角色组
    rolegroup: Optional[str]
    #: 角色方案行号
    rsMapping: Optional[int]
    #: 角色方案名 非必传 决定是否需要权限校验
    rsName: Optional[str]


class MemberInExpressAndRsResult(BaseModel):
    #: 错误信息，报错的时候有值
    errorMessage: Optional[str]
    #: 表达式存在（且有权限）的成员 
    existingAuthorizedMembers: Optional[List[str]]
    #: 维度表达式
    express: Optional[str]
    #: 是否表达式都包含 且 满足权限
    flag: Optional[bool]
    #: folderId
    folderId: Optional[str]
    #: 表达式存在但无权限的成员 
    noAuthorizedMembers: Optional[List[str]]
    #: 表达式不存在的成员
    nonexistentMembers: Optional[List[str]]
    #: path
    path: Optional[str]
    #: 角色
    role: Optional[str]
    #: 角色方案folderId
    roleFolderId: Optional[str]
    #: 角色组
    rolegroup: Optional[str]
    #: 角色方案行号
    rsMapping: Optional[int]
    #: 角色方案名
    rsName: Optional[str]


class MoreLevelMemberDto(BaseModel):
    """More Level Member Dto

    .. admonition:: 引用接口

        - **POST** ``/dimension/custom/get-more-level-member``
    """
    #: 当前层级
    currentLevel: Optional[str]
    #: 默认维度成员名
    defaultValue: Optional[str]
    #: 维度表达式
    dimensionMemberNames: Optional[str]
    #: folderId
    folderId: Optional[str]
    #: length
    length: Optional[int]
    #: path
    path: Optional[str]
    #: resultString
    resultString: Optional[str]
    #: 查询方向  1向上  2本层级  3向下
    searchDirection: Optional[str]
    #: 查询层级
    showLevel: Optional[str]
    #: start
    start: Optional[int]


class OpenErrorDto(BaseModel):
    #: 报错信息
    errorMessage: Optional[str]
    #: 报错字段
    field: Optional[str]
    #: 字段细分属性
    field2: Optional[str]
    #: 页面区域
    region: Optional[str]


class PeriodConfig(BaseModel):
    #: isActive
    isActive: Optional[int]
    #: periodLevel
    periodLevel: Optional[str]


class PeriodConfigDto(BaseModel):
    """Period Config Dto

    .. admonition:: 引用接口

        - **POST** ``/dimension/info/build-period-config-and-member``
    """
    #: dimensionName
    dimensionName: Optional[str]
    #: folderId
    folderId: Optional[str]
    #: levelManage
    levelManage: Optional[List[Dict]]
    #: path
    path: Optional[str]


class RelationDimension(BaseModel):
    #: absoluteTag
    absoluteTag: Optional[bool]
    #: dimensionType
    dimensionType: Optional[int]
    #: elementName
    elementName: Optional[str]
    #: filed
    filed: Optional[str]
    #: folderId
    folderId: Optional[str]
    #: path
    path: Optional[str]


class RelationVo(BaseModel):
    #: elementDetail
    elementDetail: Optional[ElementDetailVo]
    #: relationField
    relationField: Optional[str]
    #: relationPosition
    relationPosition: Optional[str]


class ResultObj(BaseModel):
    #: errorCode
    errorCode: Optional[str]
    #: errorList
    errorList: Optional[List[Any]]
    #: resultCode
    resultCode: Optional[int]
    #: resultList
    resultList: Optional[List[Any]]
    #: resultObj
    resultObj: Optional[Any]
    #: resultString
    resultString: Optional[str]
    #: success
    success: Optional[bool]
    #: tipMsg
    tipMsg: Optional[str]


class UdValueByExpressDto(BaseModel):
    """Ud Value By Express Dto

    .. admonition:: 引用接口

        - **POST** ``/dimension/custom/get-ud-value-by-express``
    """
    #: 维度表达式
    dimensionMemberNames: Optional[str]
    #: folderId
    folderId: Optional[str]
    #: 返回数据格式:0-list,1-map
    outFormat: Optional[str]
    #: path
    path: Optional[str]
    #: resultString
    resultString: Optional[str]
    #: 排序:0-正序,1-倒叙
    reverse_order: Optional[str]
    #: 自定义字段表达式
    ud_express: Optional[str]


class ViewDto(BaseModel):
    #: is_access
    is_access: Optional[bool]
    #: is_active
    is_active: Optional[bool]
    #: multilingual
    multilingual: Optional[Any]
    #: name
    name: Optional[str]
    #: value
    value: Optional[str]


class ViewExpressDto(BaseModel):
    """View Express Dto

    .. admonition:: 引用接口

        - **POST** ``/dimension/query/get-view-by-express``
    """
    #: elementName
    elementName: Optional[str]
    #: express
    express: Optional[str]
    #: folderId
    folderId: Optional[str]
    #: path
    path: Optional[str]
    #: showAll
    showAll: Optional[bool]


class YearPeriodDto(BaseModel):
    #: end_period
    end_period: Optional[str]
    #: end_year
    end_year: Optional[str]
    #: start_period
    start_period: Optional[str]
    #: start_year
    start_year: Optional[str]


class AllYearPeriodOfSceanrioDto(BaseModel):
    """All Year Period Of Sceanrio Dto

    .. admonition:: 引用接口

        - **POST** ``/dimension/query/get-all-year-period-of-sceanrio``
    """
    #: 是否查询period所有层级 1是
    allParam: Optional[str]
    #: 场景维度名
    dimensionName: Optional[str]
    #: 文件夹id
    folderId: Optional[str]
    #: 年份期间组合
    paramList: Optional[List[YearPeriodDto]]
    #: 路径
    path: Optional[str]


class Dimension(BaseModel):
    """dimension

    .. admonition:: 引用接口

        - **POST** ``/dimension-save/dimension-member-change-save``
        - **POST** ``/dimension/info/update-view-member``
    """
    #: accessTable_dim_col_table
    accessTable_dim_col_table: Optional[str]
    #: accessTable_dim_col_table_column
    accessTable_dim_col_table_column: Optional[str]
    #: addFieldValAsDimMember
    addFieldValAsDimMember: Optional[bool]
    #: application_name
    application_name: Optional[str]
    #: auto_sub_name
    auto_sub_name: Optional[int]
    #: create_time
    create_time: Optional[str]
    #: creator
    creator: Optional[str]
    #: creator_email
    creator_email: Optional[str]
    #: databaseServerName
    databaseServerName: Optional[str]
    #: description
    description: Optional[str]
    #: description1
    description1: Optional[str]
    #: description2
    description2: Optional[str]
    #: description3
    description3: Optional[str]
    #: description4
    description4: Optional[str]
    #: description5
    description5: Optional[str]
    #: description6
    description6: Optional[str]
    #: description7
    description7: Optional[str]
    #: description8
    description8: Optional[str]
    #: dimMemberParentName
    dimMemberParentName: Optional[str]
    #: dimensionType
    dimensionType: Optional[int]
    #: dimensionUd
    dimensionUd: Optional[List[Dict]]
    #: dimension_info
    dimension_info: Optional[str]
    #: end_year
    end_year: Optional[str]
    #: errors
    errors: Optional[List[OpenErrorDto]]
    #: file_name
    file_name: Optional[str]
    #: folderId
    folderId: Optional[str]
    #: id
    id: Optional[str]
    #: isSelected
    isSelected: Optional[str]
    #: is_sub_default
    is_sub_default: Optional[int]
    #: is_sub_dimension
    is_sub_dimension: Optional[int]
    #: language
    language: Optional[str]
    #: languageKey
    languageKey: Optional[str]
    #: last_modify_time
    last_modify_time: Optional[str]
    #: last_modify_user
    last_modify_user: Optional[str]
    #: last_modify_user_email
    last_modify_user_email: Optional[str]
    #: levelManage
    levelManage: Optional[List[Dict]]
    #: moduleId
    moduleId: Optional[str]
    #: multilingual
    multilingual: Optional[Any]
    #: name
    name: Optional[str]
    #: no_create_table
    no_create_table: Optional[int]
    #: owner
    owner: Optional[str]
    #: parentId
    parentId: Optional[str]
    #: path
    path: Optional[str]
    #: periodConfig
    periodConfig: Optional[List[PeriodConfig]]
    #: period_dimension
    period_dimension: Optional[str]
    #: period_level
    period_level: Optional[int]
    #: relationDimensions
    relationDimensions: Optional[List[RelationDimension]]
    #: scenario_sub
    scenario_sub: Optional[int]
    #: security_level
    security_level: Optional[str]
    #: start_year
    start_year: Optional[str]
    #: status
    status: Optional[str]
    #: system
    system: Optional[str]
    #: system_security_level
    system_security_level: Optional[str]
    #: tableClosure
    tableClosure: Optional[ElementDetailVo]
    #: tableDimension
    tableDimension: Optional[ElementDetailVo]
    #: tablePeriodView
    tablePeriodView: Optional[str]
    #: tablePeriodViewElement
    tablePeriodViewElement: Optional[ElementDetailVo]
    #: table_calendar_full
    table_calendar_full: Optional[str]
    #: table_calendar_info
    table_calendar_info: Optional[str]
    #: table_closure
    table_closure: Optional[str]
    #: table_dimension
    table_dimension: Optional[str]
    #: table_member_access
    table_member_access: Optional[str]
    #: table_ud_byperiod
    table_ud_byperiod: Optional[str]
    #: table_ud_duration
    table_ud_duration: Optional[str]
    #: tcFolderId
    tcFolderId: Optional[str]
    #: tcServerName
    tcServerName: Optional[str]
    #: tdFolderId
    tdFolderId: Optional[str]
    #: tdServerName
    tdServerName: Optional[str]
    #: ud1_alias
    ud1_alias: Optional[str]
    #: ud2_alias
    ud2_alias: Optional[str]
    #: ud3_alias
    ud3_alias: Optional[str]
    #: useLevelManage
    useLevelManage: Optional[bool]
    #: use_active_duration
    use_active_duration: Optional[int]
    #: version_sub
    version_sub: Optional[int]
    #: viewDtos
    viewDtos: Optional[List[ViewDto]]


class DimensionChangeSaveResult(BaseModel):
    #: code
    code: Optional[str]
    #: dimensionName
    dimensionName: Optional[str]
    #: errors
    errors: Optional[List[Error]]


class DimensionMemberChangeSaveSw(BaseModel):
    #: dimensionInfo
    dimensionInfo: Optional[DimensionInfoSw]
    #: dimensionMemberList
    dimensionMemberList: Optional[List[DimensionMemberOperationSw]]


class DimensionMemberSaveDto(BaseModel):
    """Dimension Member Save Dto

    .. admonition:: 引用接口

        - **POST** ``/dimension/member/save-dimension-member``
    """
    #: dimensionMemberList
    dimensionMemberList: Optional[List[DimensionMembersDto]]
    #: dimensionName
    dimensionName: Optional[str]
    #: folderId
    folderId: Optional[str]
    #: 保存类型:0-全量,1-增量
    increment: Optional[str]
    #: path
    path: Optional[str]


class DimensionRelationVo(BaseModel):
    """Dimension Relation Vo

    .. admonition:: 引用接口

        - **POST** ``/dimension/info/relation``
    """
    #: elementInfoRelationList
    elementInfoRelationList: Optional[List[RelationVo]]
    #: 文件夹id
    templateFolderId: Optional[str]
    #: 元素名称
    templateName: Optional[str]


class UpdateViewMemberSw(BaseModel):
    #: 文件夹id
    folderId: Optional[str]
    #: 维度名
    name: Optional[str]
    #: 元素路径
    path: Optional[str]
    #: view数据
    viewDtos: Optional[List[ViewDto]]



