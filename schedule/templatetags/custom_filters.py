# myapp/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter(name='get_dayofweek_kor')
def get_dayofweek_kor(number):
    days_of_week = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]

    if 0 <= number <= 6:
        return days_of_week[number][0]
    else:
        return "잘못된 숫자 입력. 0부터 6까지의 숫자를 입력하세요."


@register.filter(name='get_category')
def get_category(number):
    category = ["school", "class", "EC", "clinic", "social", "todo", "etc"]

    if 0 <= number <= 6:
        return category[number]
    else:
        return "잘못된 숫자 입력. 0부터 6까지의 숫자를 입력하세요."


# category_choice = (
#         (0,'0 school: no school..'),
#         (1,'1 class: math, bookclub, korean..'),
#         (2,'2 EC: music, art, sports, volunteer..'),
#         (3,'3 clinic'),
#         (4,'4 social: party..'),
#         (5,'5 todo'),
#         (6,'6 etc'),
#     )
