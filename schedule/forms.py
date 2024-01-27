from django.contrib.admin.widgets import AdminDateWidget
from django.contrib.admin import widgets
from django import forms
from .models import Person, Event, Schedule

class DateInput(forms.DateInput):
     input_type = 'date'
     input_formats = '%Y-%m-%d'

class TimeInput(forms.DateInput):
     input_type = 'time'

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = '__all__'

        memo = forms.CharField(
                # label='Memo',
                # help_text='자유롭게 작성해주세요.',
                widget=forms.Textarea(
                        attrs={
                            'row': 10,
                            'col': 80,
                        }
                    )
        )

        history = forms.CharField(
                # help_text='자유롭게 작성해주세요.',
                widget=forms.Textarea(
                        attrs={
                            'row': 20,
                            'col': 200,
                        }
                    )
        )

    def __init__(self, *args, **kwargs):
        super(PersonForm, self).__init__(*args, **kwargs)
        self.fields['birthday'].widget = widgets.AdminDateWidget()
        self.fields['memo'].widget.attrs = { 'class': 'form-control' }

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'

        memo = forms.CharField(
                widget=forms.Textarea(
                        attrs={
                            'row': 5,
                            'col': 50,
                        }
                    )
        )

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields['time'].widget = widgets.AdminTimeWidget()
        self.fields['startdate'].widget = widgets.AdminDateWidget()
        self.fields['enddate'].widget = widgets.AdminDateWidget()
        self.fields['memo'].widget.attrs = {
            'class': 'form-control',
            # 'placeholder': "자유롭게 작성해주세요."
        }


from django.core.exceptions import ValidationError
class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        exclude = ['date']

        fields = '__all__'

        memo = forms.CharField(
                # label='Memo',
                # help_text='자유롭게 작성해주세요.',
                widget=forms.Textarea(
                        attrs={
                            'row': 5,
                            'col': 50,
                        }
                    )
        )

    def __init__(self, *args, **kwargs):
        super(ScheduleForm, self).__init__(*args, **kwargs)
        self.fields['dateday'].widget = widgets.AdminDateWidget()
        self.fields['datetime'].widget = widgets.AdminTimeWidget()
        self.fields['personid'].widget.attrs = {
            'class': 'form-control',
            'placeholder': "사람을 선택해 주세요"
        }
        self.fields['eventid'].widget.attrs = {
            'class': 'form-control',
            'placeholder': "이벤트를 선택해 주세요"
        }
        self.fields['memo'].widget.attrs = {
            'class': 'form-control',
            # 'placeholder': "자유롭게 작성해주세요."
        }


    def clean_memo(self):
        data = self.cleaned_data['memo']
        if "비속어" == data:
            raise ValidationError("'비속어'는 사용하실 수 없습니다.")

        return data


# class MyMenuForm1(forms.ModelForm):
#     class Meta:
#         model = MyMenu
#         # fields = '__all__'
#         fields = ['userid', 'menu', 'category']
#         widgets = { 'userid': forms.HiddenInput() }

#     def __init__(self, *args, **kwargs):
#         super(MyMenuForm1, self).__init__(*args, **kwargs)
#         self.fields['category'].widget.attrs = {
#             'class': 'form-control',
#             'placeholder': "카테고리를 선택해 주세요"
#         }

# class MyMenuForm(forms.ModelForm):
#     class Meta:
#         model = MyMenu
#         # fields = '__all__'
#         fields = ['userid', 'menu', 'category']
#         widgets = { 'userid': forms.HiddenInput() }

#     def __init__(self, *args, **kwargs):
#         super(MyMenuForm, self).__init__(*args, **kwargs)
#         self.fields['category'].widget.attrs = {
#             'class': 'form-control',
#             'placeholder': "카테고리를 선택해 주세요"
#         }

# class MyItemForm(forms.ModelForm):
#     class Meta:
#         model = MyItem
#         # fields = '__all__'
#         fields = ['userid', 'item', 'category']
#         widgets = { 'userid': forms.HiddenInput() }

#     def __init__(self, *args, **kwargs):
#         super(MyItemForm, self).__init__(*args, **kwargs)
#         self.fields['category'].widget.attrs = {
#             'class': 'form-control',
#             'placeholder': "카테고리를 선택해 주세요"
#         }