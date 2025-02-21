"""
Models used by /smart-list-server1-0

generated by model_code_gen.py
  - **filename** : ``smart_list.py``
  - **json timestamp** : ``2021-07-28 16:26:08``
"""


from .base import BaseModel
from typing import List, Optional
from pydantic import Field


__all__ = [
    'ElementBaseInfoParamDTO',
    'ElementFixInfoDTO',
    'SmartList',
    'SmartListInfo',
    'SmartListUd',
    'SmartListDTO'
]


class ElementBaseInfoParamDTO(BaseModel):
    """Element Base Info Param DTO

    .. admonition:: 引用接口

        - **POST** ``/smart-list/list``
    """
    #: 元素名称
    elementName: Optional[str]
    #: 组件名称
    elementType: Optional[str]
    #: 文件夹id
    folderId: Optional[str]
    #: 路径
    path: Optional[str]


class ElementFixInfoDTO(BaseModel):
    """Element Fix Info DTO

    .. admonition:: 引用接口

        - **POST** ``/smart-list/add`` (Response: 200)
        - **POST** ``/smart-list/update`` (Response: 200)
    """
    #: 元素名称
    elementName: Optional[str]
    #: 文件夹id
    folderId: Optional[str]
    #: 组件id
    moduleId: Optional[str]
    #: 组件类型
    moduleType: Optional[str]
    #: 路径
    path: Optional[str]


class SmartList(BaseModel):
    #: 值列表成员多语言
    desc: Optional[dict]
    #: 描述
    description: Optional[str]
    #: 描述1
    description1: Optional[str]
    #: 描述2
    description2: Optional[str]
    #: 描述3
    description3: Optional[str]
    #: 描述4
    description4: Optional[str]
    #: 描述5
    description5: Optional[str]
    #: 描述6
    description6: Optional[str]
    #: 描述7
    description7: Optional[str]
    #: 描述8
    description8: Optional[str]
    #: 值列表成员唯一标识
    key: Optional[str]
    #: 多语言的key
    languageKey: Optional[str]
    #: 值列表成员顺序
    sortId: Optional[int]
    #: 状态 true/false 默认true开启
    status: Optional[bool]
    #: 值列表成员名称
    subjectValue: Optional[str]
    #: ud1的值
    ud1: Optional[str]
    #: ud10的值
    ud10: Optional[str]
    #: ud11的值
    ud11: Optional[str]
    #: ud12的值
    ud12: Optional[str]
    #: ud13的值
    ud13: Optional[str]
    #: ud14的值
    ud14: Optional[str]
    #: ud15的值
    ud15: Optional[str]
    #: ud16的值
    ud16: Optional[str]
    #: ud17的值
    ud17: Optional[str]
    #: ud18的值
    ud18: Optional[str]
    #: ud19的值
    ud19: Optional[str]
    #: ud2的值
    ud2: Optional[str]
    #: ud20的值
    ud20: Optional[str]
    #: ud21的值
    ud21: Optional[str]
    #: ud22的值
    ud22: Optional[str]
    #: ud23的值
    ud23: Optional[str]
    #: ud24的值
    ud24: Optional[str]
    #: ud25的值
    ud25: Optional[str]
    #: ud26的值
    ud26: Optional[str]
    #: ud27的值
    ud27: Optional[str]
    #: ud28的值
    ud28: Optional[str]
    #: ud29的值
    ud29: Optional[str]
    #: ud3的值
    ud3: Optional[str]
    #: ud30的值
    ud30: Optional[str]
    #: ud4的值
    ud4: Optional[str]
    #: ud5的值
    ud5: Optional[str]
    #: ud6的值
    ud6: Optional[str]
    #: ud7的值
    ud7: Optional[str]
    #: ud8的值
    ud8: Optional[str]
    #: ud9的值
    ud9: Optional[str]


class SmartListInfo(BaseModel):
    #: 值列表多语言
    desc: Optional[dict]
    #: 描述
    description: Optional[str]
    #: 描述1
    description1: Optional[str]
    #: 描述2
    description2: Optional[str]
    #: 描述3
    description3: Optional[str]
    #: 描述4
    description4: Optional[str]
    #: 描述5
    description5: Optional[str]
    #: 描述6
    description6: Optional[str]
    #: 描述7
    description7: Optional[str]
    #: 描述8
    description8: Optional[str]
    #: 值列表id
    id: Optional[str]
    #: 多语言标记
    languageKey: Optional[str]
    #: 值列表名称
    name: Optional[str]


class SmartListUd(BaseModel):
    #: 状态(1-启用/0-未启用)
    active: Optional[bool]
    #: 值列表ud多语言
    desc: Optional[dict]
    #: 描述
    description: Optional[str]
    #: 描述1
    description1: Optional[str]
    #: 描述2
    description2: Optional[str]
    #: 描述3
    description3: Optional[str]
    #: 描述4
    description4: Optional[str]
    #: 描述5
    description5: Optional[str]
    #: 描述6
    description6: Optional[str]
    #: 描述7
    description7: Optional[str]
    #: 描述8
    description8: Optional[str]
    #: 值列表多语言
    languageKey: Optional[str]
    #: ud名称
    udName: Optional[str]


class SmartListDTO(BaseModel):
    """Smart List DTO

    .. admonition:: 引用接口

        - **GET** ``/smart-list/`` (Response: 200)
        - **POST** ``/smart-list/add``
        - **POST** ``/smart-list/list`` (Response: 200)
        - **POST** ``/smart-list/update``
    """
    #: 文件夹id
    folderId: Optional[str]
    #: 组件id
    moduleId: Optional[str]
    #: 路径
    path: Optional[str]
    #: 值列表成员（多个）
    smartList: Optional[List[SmartList]]
    #: 值列表基本信息
    smartListInfo: Optional[SmartListInfo]
    #: 值列表ud信息（多个）
    smartListUd: Optional[List[SmartListUd]]



