"""
Models used by /deepfos-task-server

generated by model_code_gen.py
  - **filename** : ``deepfos_task.py``
  - **json timestamp** : ``2022-07-27 15:41:09``
"""


from .base import BaseModel
from typing import List, Optional, Union, Any
from pydantic import Field


__all__ = [
    'JobCreateDto',
    'JobSearchDTO',
    'TJobContent',
    'TTaskInfo',
    'TaskSearchDTO',
    'PeriodicTaskCreateInfo',
    'PeriodicTaskViewInfo',
    'ScheduledTaskCreateInfo',
    'ScheduledTaskViewInfo',
    'JobCurrentContentDTO',
    'JobCurrentContentDTOResp'
]


class JobCreateDto(BaseModel):
    """Job Create Dto

    .. admonition:: 引用接口

        - **POST** ``/job/batch-add``
    """
    #: 批次ID,传入将会设置为同一批次job,可以通过后续查询获取一批次作业
    batchId: Optional[int]
    #: 自定义参数
    customParams: Optional[Any]
    #: 作业明细信息，jobContentNameEn,jobContentNameZhcn,jobContentNameZhtw为系统字段其中jobContentNameZhcn必填
    jobContent: Optional[List[dict]]
    #: 任务编码
    taskCode: str
    #: 如果是上游系统触发的节点操作，这个字段填入上游系统所携带的id,此id应该全局唯一，该字段可以为空
    upStreamId: Optional[str]
    #: 上游系统的身份信息，任务流: 1；计算流: 2；数据流: 3；python计算: 4
    upStreamIdentity: Optional[int]


class JobSearchDTO(BaseModel):
    """Job Search DTO

    .. admonition:: 引用接口

        - **POST** ``/job/current-content``
        - **POST** ``/job/current-content/end``
    """
    #: 明细状态：SUCCESS、FAIL
    contentStatus: Optional[str]
    #: 创建时间结束区间
    createTimeEnd: Optional[str]
    #: 创建时间开始区间
    createTimeStart: Optional[str]
    #: 主作业状态：SUCCESS、PARTIAL_FAIL、FAIL
    currentStatus: Optional[str]
    #: 作业ID
    jobId: Optional[int]
    #: 页数
    pageNum: Optional[int]
    #: 每页行数
    pageSize: Optional[int]
    #: 运行时间结束区间
    runTimeEnd: Optional[str]
    #: 运行时间开始区间
    runTimeStart: Optional[str]
    #: 分批ID
    shareId: Optional[int]
    #: 任务类型
    taskType: Optional[str]


class TJobContent(BaseModel):
    #: 创建时间
    createTime: Optional[str]
    #: 创建人
    createUser: Optional[str]
    #: 明细时间属性
    datePropertyValue: Optional[str]
    #: 结束时间
    endTime: Optional[str]
    #: 明细是否过滤
    existTag: Optional[bool]
    #: 明细ID
    id: Optional[int]
    #: 明细名称英文
    jobContentNameEn: Optional[str]
    #: 明细名称简体中文
    jobContentNameZhcn: Optional[str]
    #: 明细名称繁体中文
    jobContentNameZhtw: Optional[str]
    #: 作业ID
    jobId: Optional[int]
    #: 明细日志
    logContent: Optional[str]
    #: 修改时间
    modifyTime: Optional[str]
    #: 修改人
    modifyUser: Optional[str]
    #: 明细参数
    params: Optional[str]
    #: 主键数据
    pkKey: Optional[str]
    #: 运行时间
    runTime: Optional[str]
    #: 批次ID
    shareId: Optional[int]
    #: 明细状态
    status: Optional[str]


class TTaskInfo(BaseModel):
    """T Task Info

    .. admonition:: 引用接口

        - **POST** ``/api/deepfos/task/search`` (Response: 200)
    """
    #: app
    app: Optional[str]
    #: autoEndFlag
    autoEndFlag: Optional[int]
    #: compositeKeys
    compositeKeys: Optional[str]
    #: contentParams
    contentParams: Optional[str]
    #: createTime
    createTime: Optional[str]
    #: createUser
    createUser: Optional[str]
    #: dateProperty
    dateProperty: Optional[str]
    #: dependency
    dependency: Optional[int]
    #: filterDateProperty
    filterDateProperty: Optional[int]
    #: filterFields
    filterFields: Optional[str]
    #: groupBy
    groupBy: Optional[str]
    #: id
    id: Optional[int]
    #: jobContentMaxNumOfPeriod
    jobContentMaxNumOfPeriod: Optional[int]
    #: lifeCallBackMapping
    lifeCallBackMapping: Optional[str]
    #: lifeCallBackServer
    lifeCallBackServer: Optional[str]
    #: maxBatchCount
    maxBatchCount: Optional[int]
    #: maxConcurrency
    maxConcurrency: Optional[int]
    #: modifyTime
    modifyTime: Optional[str]
    #: modifyUser
    modifyUser: Optional[str]
    #: oppositesCode
    oppositesCode: Optional[str]
    #: requestHealthMapping
    requestHealthMapping: Optional[str]
    #: requestHealthServer
    requestHealthServer: Optional[str]
    #: requestMapping
    requestMapping: Optional[str]
    #: requestServer
    requestServer: Optional[str]
    #: space
    space: Optional[str]
    #: taskCode
    taskCode: Optional[str]
    #: taskFilter
    taskFilter: Optional[str]
    #: taskNameEn
    taskNameEn: Optional[str]
    #: taskNameZhcn
    taskNameZhcn: Optional[str]
    #: taskNameZhtw
    taskNameZhtw: Optional[str]
    #: taskObjEn
    taskObjEn: Optional[str]
    #: taskObjZhcn
    taskObjZhcn: Optional[str]
    #: taskObjZhtw
    taskObjZhtw: Optional[str]
    #: taskType
    taskType: Optional[str]
    #: timeout
    timeout: Optional[int]
    #: version
    version: Optional[int]


class TaskSearchDTO(BaseModel):
    """Task Search DTO

    .. admonition:: 引用接口

        - **POST** ``/api/deepfos/task/search``
    """
    #: 是否只查询最大版本任务
    maxVersionTask: Optional[bool]
    #: 任务编码
    taskCode: Optional[str]


class PeriodicTaskCreateInfo(BaseModel):
    """周期任务创建信息

    .. admonition:: 引用接口

        - **POST** ``/api/deepfos/task/instance/period/create``
        - **POST** ``/api/deepfos/task/period/create``
    """
    #: 批次ID，可以理解为就是作业ID，一个作业下面关联多条明细。第一次创建离线任务，该字段为空，更新作业明细时，需要加入该字段。
    batchId: Optional[int]
    #: 该周期任务的 Cron 表达式
    cron: str
    #: 用户自定义的参数信息
    customParams: Optional[Any]
    #: 周期任务结束时间
    endTime: str
    #: 明细数据信息
    jobContent: Optional[List[dict]]
    #: 是否为最后一批明细，默认为 true
    lastBatch: Optional[bool]
    #: 周期任务开始时间
    startTime: str
    #: 任务ID
    taskId: int
    #: 如果是上游系统触发的节点操作，这个字段填入上游系统所携带的id,此id应该全局唯一，该字段可以为空
    upStreamId: Optional[str]
    #: 上游系统的身份信息，任务流: 1；计算流: 2；数据流: 3；python计算: 4
    upStreamIdentity: Optional[int]


class PeriodicTaskViewInfo(BaseModel):
    """周期任务视图信息

    .. admonition:: 引用接口

        - **POST** ``/api/deepfos/task/instance/period/create`` (Response: 200)
        - **POST** ``/api/deepfos/task/period/create`` (Response: 200)
    """
    #: 周期任务的批次ID
    batchId: int
    #: 周期任务主键ID
    id: int


class ScheduledTaskCreateInfo(BaseModel):
    """定时任务创建信息

    .. admonition:: 引用接口

        - **POST** ``/api/deepfos/task/instance/scheduled/create``
        - **POST** ``/api/deepfos/task/scheduled/create``
    """
    #: 批次ID，可以理解为就是作业ID，一个作业下面关联多条明细。第一次创建离线任务，该字段为空，更新作业明细时，需要加入该字段。
    batchId: Optional[int]
    #: 用户自定义参数信息
    customParams: Optional[Any]
    #: 定时执行时间
    executeTime: str
    #: 作业明细信息
    jobContent: Optional[List[dict]]
    #: 是否为最后一批明细，默认为 true
    lastBatch: Optional[bool]
    #: 任务配置ID
    taskId: int
    #: 如果是上游系统触发的节点操作，这个字段填入上游系统所携带的id,此id应该全局唯一，该字段可以为空
    upStreamId: Optional[str]
    #: 上游系统的身份信息，任务流: 1；计算流: 2；数据流: 3；python计算: 4
    upStreamIdentity: Optional[int]


class ScheduledTaskViewInfo(BaseModel):
    """定时任务视图信息

    .. admonition:: 引用接口

        - **POST** ``/api/deepfos/task/instance/scheduled/create`` (Response: 200)
        - **POST** ``/api/deepfos/task/scheduled/create`` (Response: 200)
    """
    #: 定时任务的批次ID
    batchId: Optional[int]
    #: 定时任务主键ID
    id: int


class JobCurrentContentDTO(BaseModel):
    """Job Current Content DTO

    .. admonition:: 引用接口

        - **GET** ``/job/current-content`` (Response: 200)
        - **GET** ``/job/current-content/end`` (Response: 200)
    """
    #: 应用ID
    app: Optional[str]
    #: 创建时间
    createTime: Optional[str]
    #: 创建人
    createUser: Optional[str]
    #: 自定义参数
    customParams: Optional[str]
    #: 结束时间
    endTime: Optional[str]
    #: 作业明细
    jobContents: Optional[List[TJobContent]]
    #: 作业ID
    jobId: Optional[int]
    #: 作业名称英文
    jobNameEn: Optional[str]
    #: 作业名称简体中文
    jobNameZhcn: Optional[str]
    #: 作业名称繁体中文
    jobNameZhtw: Optional[str]
    #: 作业对象英文
    jobObjEn: Optional[str]
    #: 作业对象简体中文
    jobObjZhcn: Optional[str]
    #: 作业对象繁体中文
    jobObjZhtw: Optional[str]
    #: 作业日志ID
    logFile: Optional[str]
    #: 消息状态
    messageStatus: Optional[str]
    #: 修改时间
    modifyTime: Optional[str]
    #: 修改人
    modifyUser: Optional[str]
    #: 作业结果状态
    resultStatus: Optional[str]
    #: 运行时间
    runTime: Optional[str]
    #: 批次ID
    shareId: Optional[int]
    #: 空间ID
    space: Optional[str]
    #: 作业状态
    status: Optional[str]
    #: 任务ID
    taskId: Optional[int]
    #: upStreamId
    upStreamId: Optional[str]
    #: upStreamIdentity
    upStreamIdentity: Optional[int]


class JobCurrentContentDTOResp(BaseModel):
    """Resp Page«Job Current Content DTO»

    .. admonition:: 引用接口

        - **POST** ``/job/current-content`` (Response: 200)
        - **POST** ``/job/current-content/end`` (Response: 200)
    """
    #: 是否为最后一页
    lastPage: Optional[bool]
    #: 数据信息
    list: Optional[List[JobCurrentContentDTO]]
    #: 顺序：desc、asc，默认是倒序查询
    order: Optional[str]
    #: 当前页码
    pageNo: Optional[int]
    #: 一页大小
    pageSize: Optional[int]
    #: 一共多少页
    pages: Optional[int]
    #: 排序属性
    sort: Optional[str]
    #: 一共多少数据
    total: Optional[int]



