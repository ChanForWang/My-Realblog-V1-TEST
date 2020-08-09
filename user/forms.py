from django import forms
from django.contrib import auth
from django.contrib.auth.models import User



class LoginForm(forms.Form):
    username = forms.CharField(label='用户名',widget=forms.TextInput({'class':'form-control','placeholder':'请输入用户名'}))
    password = forms.CharField(label='密码', widget=forms.PasswordInput({'class':'form-control','placeholder':'请输入密码'}))

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        user = auth.authenticate(username=username,password=password)
        if user is None:
            raise forms.ValidationError('用户名或密码不正确，请重新输入')
        else:
            self.cleaned_data['user'] = user
        return self.cleaned_data


class RegForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=30, min_length=3,
                               widget=forms.TextInput({'class':'form-control','placeholder':'请输入3-30位长度的用户名'}))
    email = forms.EmailField(label='邮箱',
                               widget=forms.EmailInput({'class': 'form-control', 'placeholder': '请输入邮箱'}))
    password = forms.CharField(label='密码', min_length=6, widget=forms.PasswordInput({'class': 'form-control', 'placeholder': '请输入密码'}))
    password_again = forms.CharField(label='再次输入密码', min_length=6,
                                     widget=forms.PasswordInput({'class': 'form-control', 'placeholder': '再次输入密码'}))

    def clean_username(self):
        username = self.cleaned_data['username']
        # 验证注册的用户名之前存不存在
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('用户名已存在')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        # 验证注册的用户名之前存不存在
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('邮箱已注册过')
        return email

    def clean_password_again(self):
        password = self.cleaned_data['password']
        password_again = self.cleaned_data['password_again']
        if password_again != password :
            raise forms.ValidationError('两次输入的密码不一致！')
        return password_again