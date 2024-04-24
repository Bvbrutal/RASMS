from django.shortcuts import render


def medication_list(request):
    context = {

    }
    return render(request, "manager/medication_management/medication_list.html", context=context)


def medication_add(request):
    context = {

    }
    return render(request, "manager/medication_management/medication_add.html", context=context)


def medication_modify(request):
    context = {

    }
    return render(request, "manager/medication_management/medication_modify.html", context=context)