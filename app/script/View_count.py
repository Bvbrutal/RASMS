from app.models import VisitNumber


def view_count(id,type):
    count_nums = VisitNumber.objects.filter(id=id,type=type)
    if count_nums:
        count_nums = count_nums[0]
        count_nums.count += 1
    else:
        count_nums = VisitNumber(id=id,type=type)
        count_nums.count = 1
    count_nums.save()