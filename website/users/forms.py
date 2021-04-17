from django import forms
from django.contrib.auth.hashers import check_password

from .models import User


class LoginForm(forms.Form):
    name = forms.CharField(
        error_messages={
            'required': '아이디를 입력해주세요.'
        },
        max_length=32, label="사용자 이름")
    password = forms.CharField(
        error_messages={
            'required': '비밀번호를 입력해주세요.'
        },
        widget=forms.PasswordInput, label="비밀번호")

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        password = cleaned_data.get('password')

        if name and password:
            try:
                user = User.objects.get(name=name)
            except User.DoesNotExist:
                self.add_error('name', '아이디가 없습니다')
                return

            if not check_password(password, user.password):
                self.add_error('password', '비밀번호를 틀렸습니다')
            else:
                self.user_id = user.id
