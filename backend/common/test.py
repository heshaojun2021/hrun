import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "primaryApp.settings.dev")
import django
django.setup()

from django.utils import timezone
from datetime import timedelta
from projects.models import newInterface
from projects.models import Project

def statistics(model, time_field):

    today = timezone.now().date()
    this_week_start = today - timedelta(days=today.weekday())
    this_week_end = this_week_start + timedelta(days=7)

    last_week_start = this_week_start - timedelta(weeks=1)
    last_week_end = last_week_start + timedelta(days=7)
    project = Project.objects.get(id=4)
    this_week_count = model.objects.filter(project=project, **{f"{time_field}__range": [this_week_start, this_week_end]})
    last_week_count = model.objects.filter(**{f"{time_field}__range": [last_week_start, last_week_end]}).count()
    this_week_count = 2
    last_week_count = 0
    #计算新增或减少的用例数量
    case_difference = this_week_count - last_week_count
    # 如果用例数量减少了，则计算减少的百分比；如果用例数量增加了，则计算增加的百分比
    if case_difference < 0:
        percentage_difference = (abs(case_difference) / last_week_count) * 100 * -1
        if percentage_difference:
            return "{:.2f}%".format(percentage_difference)
        return '暂无数据'
    elif case_difference > 0:
        try:
            percentage_difference = (case_difference / last_week_count) * 100
            return "{:.2f}%".format(percentage_difference)
        except ZeroDivisionError:
            return '暂无数据'
    else:
        percentage_difference = 0
        return "{:.2f}%".format(percentage_difference)

print(statistics(newInterface, "create_time"))