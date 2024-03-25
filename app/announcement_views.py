from django.shortcuts import render

from app.models import CommunityEvent, CommunityAnnouncement


def announcement_list(request):
    communityAnnouncements=CommunityAnnouncement.objects.all().order_by("-published_date")
    context={
        "items":communityAnnouncements
    }
    return render(request, "manager/announcement/announcement_list.html",context)


def announcement_info(request):
    id=request.GET.get("id")
    item=CommunityAnnouncement.objects.filter(id=id).first()
    context={
        'item':item
    }
    return render(request, "manager/announcement/announcement_info.html",context)


def announcement_add(request):
    context={

    }
    return render(request, "manager/announcement/announcement_add.html",context)