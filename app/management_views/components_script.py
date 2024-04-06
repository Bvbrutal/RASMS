from app.models import User, Logging
from django.utils import timezone
import hashlib
def record_admin_operation(operator_id, operation_content):
    """
    记录管理员操作的函数。
    :param operator_id: 操作员（管理员）的ID。
    :param operation_content: 操作内容。
    """
    try:
        operator = User.objects.get(id=operator_id)
        Logging.objects.create(
            operator=operator,
            operation_content=operation_content,
            operation_time=timezone.now()  # 默认值已经是timezone.now，也可以省略此参数
        )
        return True
    except User.DoesNotExist:
        print("操作员不存在。")
        return False



if __name__ == '__main__':
    passwd='123456'
    print(hashlib.md5(passwd.encode()).hexdigest())
