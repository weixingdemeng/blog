from django import forms

from user.models import User


class StuForm(forms.Form):
    username = forms.CharField(max_length=10,min_length=2,required=True,
                               error_messages={'required':'姓名是必填值',
                                                'min_length': '不能少于2个字符',
                                                'max_length': '不能超过10个字符'})

    password1 = forms.CharField(required=True, error_messages={'required': '密码必填'
                                                             })
    password2 = forms.CharField(required=True, error_messages={'required': '密码必填'})

    def clean_username(self):
        username = self.cleaned_data.get('username')
        user = User.objects.filter(u_username=username).first()
        if user:
            raise forms.ValidationError('你输入的用户名已经注册过了')
        return self.cleaned_data['username']

    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError('您输入的密码不一致')
        return self.cleaned_data