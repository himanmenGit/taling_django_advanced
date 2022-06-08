from django import forms


class RegisterForm(forms.Form):
    email = forms.EmailField(label="이메일", error_messages={"invalid": "유효한 이메일 주소를 입력해주세요."})
    password = forms.CharField(label="비밀번호", min_length=6, max_length=20, widget=forms.PasswordInput)
    password_confirm = forms.CharField(label="비밀번호 확인", min_length=6, max_length=20, widget=forms.PasswordInput)
    nickname = forms.CharField(label="닉네임", min_length=2, max_length=10)
    profile_image = forms.ImageField(label="프로필 사진", required=False)

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()

        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password != password_confirm:
            raise forms.ValidationError({
                "password_confirm": ["2개의 비밀번호가 일치하지 않습니다."]
            })

        return cleaned_data


class LoginForm(forms.Form):
    email = forms.EmailField(label="이메일", error_messages={"invalid": "유효한 이메일 주소를 입력해주세요."})
    password = forms.CharField(label="비밀번호", min_length=6, max_length=20, widget=forms.PasswordInput)
