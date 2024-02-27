from django.shortcuts import render

from app.models import CommunityEvent


def activity_list(request):
    communityEvent=CommunityEvent.objects.all().order_by("-created")
    print(communityEvent)
    context={
        'communityEvent':communityEvent
    }

    return render(request,"manager/activity/activity_list.html",context)


def activity_info(request):
    activity_id=request.GET.get('activity_id')
    activity=CommunityEvent.objects.filter(id=activity_id).first()
    context = {
        'event': activity
    }
    return render(request,"manager/activity/activity_info.html",context)


def activity_add(request):
    if request.method=='GET':
        context={

        }
        return render(request, "manager/activity/activity_add.html", context)


def activity_modify(request):
    return None