from app.models import User

'''
后端：

template_name = Dynamic_inheritance(request)
context['template_name']=template_name

'''


def Dynamic_inheritance(request):
    info_dic = request.session.get('info')
    mobile_phone = info_dic['mobile_phone']
    item = User.objects.filter(mobile_phone=mobile_phone).first()
    if item.grade == '0':
        template_name = "template/index_manager_tem.html"
    elif item.grade == '1':
        template_name = "template/index_staff_tem.html"
    elif item.grade == '3':
        template_name = "template/index_volunteer_tem.html"
    else:
        template_name = "template/index_elder_tem.html"
    # elif item.grade == 4:
    #     template_name = "template/index_user_tem.html"
    # else:
    #     template_name = "template/some_other_template.html"

    return template_name
