# 统一分页组件一个页面展示的数据条数
items_per_page = 8

GENDER_CHOICES = (
    ('M', '男'),
    ('F', '女'),
    ('U', '未知'),
)

GRADE_CHOICES = (
    ('0', '管理员'),
    ('1', '工作人员'),
    ('2', '老年用户'),
    ('3', '义工用户'),
    ('4', '其他'),
)

EVENT_TYPES = (
    (0, '情感纠纷'),
    (1, '意外事件'),
    (2, '特殊事件'),
    (3, '服务求助'),
    (4, '日常协助'),
)

OPERATION_CHOICES = (
    ('ADD_RESIDENT', '添加居民'),
    ('UPDATE_RESIDENT', '更新居民信息'),
    ('DELETE_RESIDENT', '删除居民'),

    ('ADD_STAFF', '添加员工'),
    ('UPDATE_STAFF', '更新员工信息'),
    ('DELETE_STAFF', '删除员工'),

    ('ADD_SCHEDULE', '添加排班'),
    ('UPDATE_SCHEDULE', '更新排班信息'),
    ('DELETE_SCHEDULE', '删除排班'),

    ('ADD_MEDICATION', '添加用药记录'),
    ('UPDATE_MEDICATION', '更新用药记录'),
    ('DELETE_MEDICATION', '删除用药记录'),

    ('ADD_ACTIVITY', '添加活动'),
    ('UPDATE_ACTIVITY', '更新活动信息'),
    ('DELETE_ACTIVITY', '删除活动'),

    ('ADD_ANNOUNCEMENT', '发布公告'),
    ('UPDATE_ANNOUNCEMENT', '更新公告'),
    ('DELETE_ANNOUNCEMENT', '删除公告'),

    ('ADD_FEEDBACK', '收集反馈'),
    ('UPDATE_FEEDBACK', '处理反馈'),
    ('DELETE_FEEDBACK', '删除反馈'),

    ('ADD_HEALTH_RECORD', '添加健康记录'),
    ('UPDATE_HEALTH_RECORD', '更新健康记录'),
    ('DELETE_HEALTH_RECORD', '删除健康记录'),
)
