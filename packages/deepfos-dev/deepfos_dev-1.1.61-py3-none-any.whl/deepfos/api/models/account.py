"""
Models used by /

generated by model_code_gen.py
  - **filename** : ``account.py``
  - **json timestamp** : ``2024-07-16 14:17:08``
"""


from deepfos.api.models.base import BaseModel
from typing import List, Optional, Union, Any, Dict
from pydantic import Field


__all__ = [
    'EnterpriseListVO',
    'ImportSendEmailDTO',
    'ImportUserErrorDTO',
    'PlatFormSecretVO',
    'RoleInfoDetailSaveDTO',
    'SpaceVO',
    'UserGroupChildrenVO',
    'UserGroupImportDTO',
    'UserGroupRelationshipDTO',
    'UserImportCheckDTO',
    'UserImportCheckVO',
    'UserImportDTO',
    'UserInfoVO',
    'UserRoleImportDTO',
    'UserRoleInfoSaveDTO',
    'ImportUserListParamsUserGroupImportDTO',
    'ImportUserListParamsUserGroupRelationshipDTO',
    'ImportUserListParamsUserImportDTO',
    'ImportUserListParamsUserRoleImportDTO',
    'UserGroupDetailVO',
    'UserGroupModifyDTO'
]


class EnterpriseListVO(BaseModel):
    """Enterprise List VO

    .. admonition:: 引用接口

        - **GET** ``/api/enterprise/list`` (Response: 200)
        - **POST** ``/s/enterprise/list`` (Response: 200)
    """
    #: 企业banner内容
    bannerText: Optional[str]
    #: 是否合作伙伴：0否，1是
    cooperativePartner: Optional[int]
    #: 有默认企业 : 1,非默认企业: 2
    defaultEnterprise: Optional[int]
    #: 修改权限
    edit: Optional[bool]
    #: 企业编码
    enterpriseCode: Optional[str]
    #: 企业banner图
    enterpriseImg: Optional[str]
    #: 企业名称
    enterpriseName: Optional[str]
    #: 企业名称英文
    enterpriseNameEn: Optional[str]
    #: 企业类型
    enterpriseType: Optional[str]
    #: 企业类型描述
    enterpriseTypeName: Optional[str]
    #: 外观css文件uri
    fileUri: Optional[str]
    #: 企业id
    id: Optional[str]
    #: 锁定
    locking: Optional[bool]
    #: 企业logo
    logo: Optional[str]
    #: 主营业务
    mainBusiness: Optional[str]
    #: 1：个人；2：企业
    type: Optional[str]
    #: 工作台banner图
    workbenchImg: Optional[str]


class ImportSendEmailDTO(BaseModel):
    #: 邮箱
    email: Optional[str]
    #: 昵称
    nickname: Optional[str]
    #: 操作类型
    operate: Optional[str]
    #: 操作内容
    operateContent: Optional[str]
    #: 用户id
    userId: Optional[str]
    #: 用户名
    username: Optional[str]


class ImportUserErrorDTO(BaseModel):
    #: 错误内容
    context: Optional[str]
    #: 字段名
    fieldName: Optional[str]
    #: rowNum
    rowNum: Optional[int]


class PlatFormSecretVO(BaseModel):
    """Plat Form Secret VO

    .. admonition:: 引用接口

        - **GET** ``/api/platform/secret`` (Response: 200)
    """
    #: platformCode
    platformCode: Optional[str]
    #: platformSecret
    platformSecret: Optional[str]


class RoleInfoDetailSaveDTO(BaseModel):
    #: 父级角色编码
    code: str
    #: 选中的角色code
    roleList: List[str]
    #: 父级标识
    tag: str


class SpaceVO(BaseModel):
    """Space VO

    .. admonition:: 引用接口

        - **GET** ``/api/space/enterprise-space-hierarchy`` (Response: 200)
        - **GET** ``/s/space/enterprise-space-hierarchy`` (Response: 200)
    """
    #: logo路径
    logoPath: Optional[str]
    #: 平台Code
    platformCode: Optional[str]
    #: 平台名
    platformName: Optional[str]
    #: 空间id
    spaceId: Optional[str]
    #: 空间名
    spaceName: Optional[str]


class UserGroupChildrenVO(BaseModel):
    #: groupId
    groupId: Optional[str]
    #: groupName
    groupName: Optional[str]
    #: status
    status: Optional[str]


class UserGroupImportDTO(BaseModel):
    #: 用户组描述
    description: Optional[str]
    #: 用户组编码
    groupCode: Optional[str]
    #: 用户组id
    groupId: Optional[str]
    #: 用户组名称
    groupName: Optional[str]


class UserGroupRelationshipDTO(BaseModel):
    #: 子用户组编码
    childrenGroupCode: Optional[str]
    #: 子用户组名
    childrenGroupName: Optional[str]
    #: 描述
    description: Optional[str]
    #: 邮箱
    email: Optional[str]
    #: 用户组编码（必填）
    groupCode: Optional[str]
    #: 用户组ID
    groupId: Optional[str]
    #: 用户组名
    groupName: Optional[str]
    #: 用户标识（1：用户；2：子用户组）
    importTag: Optional[str]
    #: 手机号
    mobilePhone: Optional[str]
    #: 昵称
    nickname: Optional[str]
    #: 用户ID
    userId: Optional[str]
    #: 导入用户标识（1：用户ID；2用户名；3：手机号；4：邮箱）
    userTag: Optional[str]
    #: 用户名
    username: Optional[str]


class UserImportCheckDTO(BaseModel):
    #: 新增影响数据
    addNumber: Optional[int]
    #: 删除影响数据
    deleteNumber: Optional[int]
    #: 错误信息
    errorList: Optional[List[ImportUserErrorDTO]]
    #: 错误总数
    errorSum: Optional[int]
    #: 导入总数
    importSum: Optional[int]
    #: sendEmailList
    sendEmailList: Optional[List[ImportSendEmailDTO]]
    #: 表名
    sheetName: Optional[str]
    #: 修改影响数据
    updateNumber: Optional[int]


class UserImportCheckVO(BaseModel):
    """User Import Check VO

    .. admonition:: 引用接口

        - **POST** ``/api/user/import`` (Response: 200)
        - **POST** ``/api/user/import/check`` (Response: 200)
        - **POST** ``/api/user/import/space`` (Response: 200)
        - **POST** ``/api/user/import/space/check`` (Response: 200)
        - **POST** ``/s/user/import/user`` (Response: 200)
        - **POST** ``/s/user/import/user-group`` (Response: 200)
        - **POST** ``/s/user/import/user-role`` (Response: 200)
        - **POST** ``/s/user/import/userGroupUser`` (Response: 200)
    """
    #: 导入数据
    data: Optional[List[UserImportCheckDTO]]
    #: 日志ID
    logId: Optional[str]
    #: 状态
    status: Optional[bool]


class UserImportDTO(BaseModel):
    #: 邮箱
    email: Optional[str]
    #: 手机号
    mobilePhone: Optional[str]
    #: 昵称
    nickname: Optional[str]
    #: 初始密码
    password: Optional[str]
    #: 状态（1：启用；2：禁用）
    status: str
    #: 用户ID
    userId: Optional[str]
    #: 导入用户标识（1：用户ID；2用户名；3：手机号；4：邮箱）
    userTag: str
    #: 用户名
    username: Optional[str]


class UserInfoVO(BaseModel):
    """User Info VO

    .. admonition:: 引用接口

        - **GET** ``/api/user/get-enterprise-user-list`` (Response: 200)
        - **GET** ``/api/user/get-user-info`` (Response: 200)
        - **GET** ``/api/user/space/get-enterprise-user-list`` (Response: 200)
        - **POST** ``/api/user/username-only``
        - **POST** ``/s/user/get-user-by-user-group-code`` (Response: 200)
        - **POST** ``/s/user/get-user-by-user-group-id`` (Response: 200)
        - **GET** ``/s/user/get-user-info`` (Response: 200)
    """
    #: 头像
    avatar: Optional[str]
    #: 生日
    birthday: Optional[str]
    #: 颜色
    color: Optional[str]
    #: 创建时间
    createTime: Optional[str]
    #: 创建人
    createUser: Optional[str]
    #: 邮箱
    email: Optional[str]
    #: 员工是否离开企业 0 离职  1  未离职
    leave: Optional[int]
    #: 手机号
    mobilePhone: Optional[str]
    #: 更新时间
    modifyTime: Optional[str]
    #: 更新用户
    modifyUser: Optional[str]
    #: 昵称
    nickname: Optional[str]
    #: 注册方式 1：自己注册；2：邀请邮箱注册；3：手机号注册 ;4:邮箱注册 9:未知；默认为9
    registerWay: Optional[int]
    #: 性别 1：男；2：女；3：未知
    sex: Optional[int]
    #: 是否为sso用户
    ssoUser: Optional[bool]
    #: 状态 1：可用；2：禁用；3：未激活；默认为3
    status: Optional[int]
    #: 用户id
    userId: Optional[str]
    #: 用户名
    username: Optional[str]
    #: 用户名修改次数
    usernameModifyTimes: Optional[int]


class UserRoleImportDTO(BaseModel):
    #: 应用名称
    appName: Optional[str]
    #: 邮箱
    email: Optional[str]
    #: 用户组编码
    groupCode: Optional[str]
    #: 用户组名
    groupName: Optional[str]
    #: 手机号
    mobilePhone: Optional[str]
    #: 昵称
    nickname: Optional[str]
    #: 角色编码
    roleCode: str
    #: 角色导入标识（1：用户；2：用户组）
    roleExportTag: str
    #: 角色名称
    roleName: Optional[str]
    #: 用户ID
    userId: Optional[str]
    #: 导入用户标识（1：用户ID；2用户名；3：手机号；4：邮箱）
    userTag: str
    #: 用户名
    username: Optional[str]


class UserRoleInfoSaveDTO(BaseModel):
    #: 角色列表
    children: Optional[List[RoleInfoDetailSaveDTO]]
    #: 平台code
    platformCode: str


class ImportUserListParamsUserGroupImportDTO(BaseModel):
    """Import User List Params DTO«User Group Import DTO»

    .. admonition:: 引用接口

        - **POST** ``/s/user/import/user-group``
    """
    #: 导入数据不能为空
    data: List[UserGroupImportDTO]
    #: 企业id
    enterpriseId: Optional[str]
    #: 平台编码(空间ID与平台编码需要同时存在)
    platformCode: Optional[str]
    #: 是否发送邮件,非必填 默认 true
    sendEmail: Optional[bool]
    #: 空间id(空间ID与平台编码需要同时存在)
    spaceId: Optional[str]
    #: 空间名称
    spaceName: Optional[str]
    #: 标记(全量导FULL 增量导 INCREMENT)
    tag: str


class ImportUserListParamsUserGroupRelationshipDTO(BaseModel):
    """Import User List Params DTO«User Group Relationship DTO»

    .. admonition:: 引用接口

        - **POST** ``/s/user/import/userGroupUser``
    """
    #: 导入数据不能为空
    data: List[UserGroupRelationshipDTO]
    #: 企业id
    enterpriseId: Optional[str]
    #: 平台编码(空间ID与平台编码需要同时存在)
    platformCode: Optional[str]
    #: 是否发送邮件,非必填 默认 true
    sendEmail: Optional[bool]
    #: 空间id(空间ID与平台编码需要同时存在)
    spaceId: Optional[str]
    #: 空间名称
    spaceName: Optional[str]
    #: 标记(全量导FULL 增量导 INCREMENT)
    tag: str


class ImportUserListParamsUserImportDTO(BaseModel):
    """Import User List Params DTO«User Import DTO»

    .. admonition:: 引用接口

        - **POST** ``/s/user/import/user``
    """
    #: 导入数据不能为空
    data: List[UserImportDTO]
    #: 企业id
    enterpriseId: Optional[str]
    #: 平台编码(空间ID与平台编码需要同时存在)
    platformCode: Optional[str]
    #: 是否发送邮件,非必填 默认 true
    sendEmail: Optional[bool]
    #: 空间id(空间ID与平台编码需要同时存在)
    spaceId: Optional[str]
    #: 空间名称
    spaceName: Optional[str]
    #: 标记(全量导FULL 增量导 INCREMENT)
    tag: str


class ImportUserListParamsUserRoleImportDTO(BaseModel):
    """Import User List Params DTO«User Role Import DTO»

    .. admonition:: 引用接口

        - **POST** ``/s/user/import/user-role``
    """
    #: 导入数据不能为空
    data: List[UserRoleImportDTO]
    #: 企业id
    enterpriseId: Optional[str]
    #: 平台编码(空间ID与平台编码需要同时存在)
    platformCode: Optional[str]
    #: 是否发送邮件,非必填 默认 true
    sendEmail: Optional[bool]
    #: 空间id(空间ID与平台编码需要同时存在)
    spaceId: Optional[str]
    #: 空间名称
    spaceName: Optional[str]
    #: 标记(全量导FULL 增量导 INCREMENT)
    tag: str


class UserGroupDetailVO(BaseModel):
    """User Group Detail VO

    .. admonition:: 引用接口

        - **GET** ``/api/user/group/get-user-group-detail`` (Response: 200)
    """
    #: 子组列表
    childrenGroupList: Optional[List[UserGroupChildrenVO]]
    #: 描述
    description: Optional[Any]
    #: 用户组code
    groupCode: Optional[str]
    #: 用户组名
    groupName: Optional[str]
    #: 用户组id
    id: Optional[str]
    #: 状态
    status: Optional[str]
    #: 用户组内用户id
    userList: Optional[List[UserInfoVO]]


class UserGroupModifyDTO(BaseModel):
    """User Group Modify DTO

    .. admonition:: 引用接口

        - **POST** ``/api/user/group/space/modify-group``
        - **POST** ``/s/user/group/space/modify-group-batch``
    """
    #: 子组列表
    childrenGroupIdList: Optional[List[str]]
    #: 描述
    description: Optional[Any]
    #: 用户组id
    groupId: str
    #: 用户组名
    groupName: str
    #: 空间
    spaceId: Optional[str]
    #: 用户id
    userList: Optional[List[str]]
    #: 角色列表
    userRoleInfoSaveDTOList: Optional[List[UserRoleInfoSaveDTO]]



