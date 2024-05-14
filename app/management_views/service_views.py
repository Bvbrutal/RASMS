import os
import re

from django.db.models import Q, Count
from django.shortcuts import render, get_object_or_404
from django.utils.timezone import now

from app.components.Dynamic_inheritance import Dynamic_inheritance
from app.components.Pagination import Pagination
from app.management_views.configuration import items_per_page
from app.models import ServiceOrder, Service, User, Elder
from django.http import JsonResponse


def modify_service(request):
    if request.method == "GET":
        key = request.GET.get('key', '')
        if key:
            status_mapping = {v: k for k, v in ServiceOrder.STATUS_CHOICES}
            types_mapping = {v: k for k, v in Service.SERVICE_TYPES}
            status_key = status_mapping.get(key.capitalize(), key)
            types_key = types_mapping.get(key.capitalize(), key)
            serviceOrder = ServiceOrder.objects.filter(
                (Q(id__icontains=key) |
                 Q(customerName__icontains=key) |
                 Q(service__name__icontains=key) |
                 Q(date_scheduled__icontains=key) |
                 Q(status=status_key) |
                 Q(service__type=types_key) |
                 Q(customerContact__icontains=key)) &
                Q(is_active=True)
            ).order_by("-date_scheduled")
        else:
            # 如果没有提供关键词，则返回所有用户
            serviceOrder = ServiceOrder.objects.filter(is_active=True).order_by("-date_scheduled")

        page_obj = Pagination(request, serviceOrder, items_per_page)
        context = {
            "page_obj": page_obj,
            "key": key
        }
        template_name = Dynamic_inheritance(request)
        context['template_name'] = template_name
        return render(request, "manager/service_management/modify_service.html", context)

    updated_by_id = request.session["info"]["user_id"]
    updated_by = User.objects.filter(user_id=updated_by_id).first()
    id = request.POST.get("id")
    op = request.POST.get("op")
    CA = ServiceOrder.objects.filter(id=id).first()
    if op == 'delete_service':
        CA.is_active = False
        CA.updated_by = updated_by
        CA.save()
        context = {
            'ret': 1,
            'msg': "删除成功"
        }

        return JsonResponse(context, safe=False)

    context = {
        'ret': 2,
        'msg': "删除失败"
    }
    return JsonResponse(context, safe=False)


def modify_service_type(request):
    if request.method == "GET":
        key = request.GET.get('key', '')
        if key:
            types_mapping = {v: k for k, v in Service.SERVICE_TYPES}
            types_key = types_mapping.get(key.capitalize(), key)
            services = Service.objects.filter(
                (Q(id__icontains=key) |
                 Q(name__icontains=key) |
                 Q(cost__icontains=key) |
                 Q(type=types_key)) &
                Q(is_active=True)
            ).order_by("id")
        else:
            # 如果没有提供关键词，则返回所有用户
            services = Service.objects.filter(is_active=True).order_by("id")

        page_obj = Pagination(request, services, items_per_page)
        context = {
            "page_obj": page_obj,
            "key": key
        }
        template_name = Dynamic_inheritance(request)
        context['template_name'] = template_name
        return render(request, "manager/service_management/modify_service_type.html", context)

    updated_by_id = request.session["info"]["user_id"]
    updated_by = User.objects.filter(user_id=updated_by_id).first()
    id = request.POST.get("id")
    op = request.POST.get("op")
    CA = Service.objects.filter(id=id).first()
    if op == 'delete':
        CA.is_active = False
        CA.updated_by = updated_by
        CA.save()
        context = {
            'ret': 1,
            'msg': "删除成功"
        }

        return JsonResponse(context, safe=False)

    context = {
        'ret': 2,
        'msg': "删除失败"
    }
    return JsonResponse(context, safe=False)


def add_service(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        if id:
            service = Service.objects.filter(id=id).first()
            context = {
                'item': service
            }
            template_name = Dynamic_inheritance(request)
            context['template_name'] = template_name
            return render(request, "manager/service_management/add_service_basic.html", context=context)

        services = Service.objects.all()
        context = {
            'services': services
        }
        template_name = Dynamic_inheritance(request)
        context['template_name'] = template_name
        return render(request, "manager/service_management/add_service.html", context=context)

    id = request.POST.get('id')
    customerName = request.POST.get('customerName')
    customerContact = request.POST.get('customerContact')
    date_scheduled = request.POST.get('date_scheduled', now())
    additionalNotes = request.POST.get('additionalNotes')
    created_by_user_id=request.session["info"]["user_id"]
    updated_by_user_id = created_by_user_id
    service=Service.objects.filter(id=id).first()
    if customerName and customerContact and date_scheduled:
        # Create new ServiceOrder instance
        service_order = ServiceOrder(
            customerName=customerName,
            customerContact=customerContact,
            service=service,
            date_scheduled=date_scheduled,
            remark=additionalNotes,
            created_by_id=created_by_user_id,
            updated_by_id=updated_by_user_id,
        )

        try:
            service_order.save()
            service.count += 1
            service.save()
            return JsonResponse({'ret': 1, 'msg': "服务订单已成功添加"})
        except Exception as e:
            # Handle errors in saving
            return JsonResponse({'ret': 0, 'msg': f"服务订单添加失败：{str(e)}"})

    return JsonResponse({'ret': 0, 'msg': "服务订单添加失败"})

def analyze_service(request):
    data1 = ServiceOrder.objects.values('status').annotate(total=Count('id')).order_by('status')
    context = {
        'data1':list(data1)
    }
    template_name = Dynamic_inheritance(request)
    context['template_name'] = template_name
    return render(request, "manager/service_management/analyze_service.html", context=context)





def service_info(request):
    id = request.GET.get('id')
    if id:
        service = Service.objects.filter(id=id, is_active=True).first()
        context = {
            'item': service
        }
        template_name = Dynamic_inheritance(request)
        context['template_name'] = template_name
        return render(request, "manager/service_management/service_info.html", context=context)

    service = Service.objects.last()
    context = {
        'item': service
    }
    template_name = Dynamic_inheritance(request)
    context['template_name'] = template_name
    return render(request, "manager/service_management/service_info.html", context=context)


def serviceorder_info(request):
    id = request.GET.get('id')
    if id:
        serviceorder = ServiceOrder.objects.filter(id=id, is_active=True).first()
        context = {
            'item': serviceorder
        }
        template_name = Dynamic_inheritance(request)
        context['template_name'] = template_name
        return render(request, "manager/service_management/serviceorder_info.html", context=context)

    service = ServiceOrder.objects.last()
    context = {
        'item': service
    }
    template_name = Dynamic_inheritance(request)
    context['template_name'] = template_name
    return render(request, "manager/service_management/serviceorder_info.html", context=context)

def add_service_type(request):
    if request.method == 'POST':
        # 获取表单数据
        name = request.POST.get('name')
        content = request.POST.get('content')
        description = request.POST.get('description') or None
        type = request.POST.get('type') or None
        target_group = request.POST.get('target_group') or None
        service_hours = request.POST.get('service_hours') or None
        service_area = request.POST.get('service_area') or None
        qualifications = request.POST.get('qualifications') or None
        customer_reviews = request.POST.get('customer_reviews') or None
        additional_costs = request.POST.get('additional_costs') or None
        cost = request.POST.get('cost') or None
        is_active = request.POST.get('is_active') == 'true'
        content_text = re.sub('<[^<]+?>', '', content.strip())
        if description is None:
            description = content_text[:30]
        # 处理文件上传
        service_photo = request.FILES.get('service_photo')
        if service_photo:
            _, ext = os.path.splitext(service_photo.name)
            service_photo.name = f"{name.replace(' ', '_')}_{now().strftime('%Y%m%d%H%M%S')}{ext}"

        # 创建Service实例并保存
        service = Service(
            name=name,
            content=content,
            description=description,
            type=type,
            target_group=target_group,
            service_hours=service_hours,
            service_area=service_area,
            qualifications=qualifications,
            customer_reviews=customer_reviews,
            additional_costs=additional_costs,
            cost=float(cost) if cost else 0.0,
            service_photo=service_photo,
            is_active=is_active
        )

        try:
            service.save()
            context = {
                'ret': 1,
                'msg': "服务添加成功"
            }
        except Exception as e:
            context = {
                'ret': 0,
                'msg': f"服务添加失败：{str(e)}"
            }

        return JsonResponse(context, safe=False)

    service = Service.objects.last()
    context = {
        'item': service
    }
    template_name = Dynamic_inheritance(request)
    context['template_name'] = template_name
    return render(request, "manager/service_management/add_service_type.html", context)


def service_list(request):
    mobile_phone = request.session["info"]["mobile_phone"]
    serviceorders1 = ServiceOrder.objects.filter(customerContact=mobile_phone).order_by('-date_scheduled')
    serviceorders2 = ServiceOrder.objects.filter(aceeptContact=mobile_phone).order_by('-date_scheduled')
    serviceorders=serviceorders1 if serviceorders1 else serviceorders2
    context = {
        'orders': serviceorders
    }
    template_name = Dynamic_inheritance(request)
    context['template_name'] = template_name
    return render(request, "manager/service_management/service_list.html", context)


def cancel_service(request):
    id = request.POST.get("id")
    print(id)
    service_order = ServiceOrder.objects.filter(id=id).first()
    if not service_order:
        return JsonResponse({'ret': 0, 'msg': "服务订单未找到"})
    try:
        service_order.status = 'cancelled'
        service_order.save()
        context = {
            'ret': 1,
            'msg': "服务订单已成功取消"
        }
    except Exception as e:
        context = {
            'ret': 0,
            'msg': f"服务取消失败：{str(e)}"
        }

    return JsonResponse(context, safe=False)


def submit_feedback(request):
    id = request.POST.get("order_id")
    rating = request.POST.get("rating") or None
    feedback = request.POST.get("feedback") or None
    service_order = ServiceOrder.objects.filter(id=id).first()
    print(rating)
    if not service_order:
        return JsonResponse({'ret': 0, 'msg': "服务订单未找到"})
    try:
        service_order.rating = rating
        service_order.feedback = feedback
        service_order.save()
        context = {
            'ret': 1,
            'msg': "服务订单已成功反馈"
        }
    except Exception as e:
        context = {
            'ret': 0,
            'msg': f"服务订单已成功失败：{str(e)}"
        }

    return JsonResponse(context, safe=False)