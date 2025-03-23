from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

class SignUpForm(forms.ModelForm):
    confirm_password = forms.CharField(max_length=200, required=True, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError("Parollar mos kelmadi.")
        return cleaned_data
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Bu emailda foydalanuvchi mavjud.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            User.objects.create(user=user, color=self.cleaned_data['color'])
        return user
    
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'lebel':'Username', 'class':'form_control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'lebel':'Password', 'class':'form_control'}))

    def clean_username(self):
        username = self.cleaned_data['username']
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError('Bunday foydalanuvchi nomi mavjud emas.')
        return username
    
class UpdateUserForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=False, widget=forms.PasswordInput, label="Yangi parol")
    confirm_password = forms.CharField(required=False, widget=forms.PasswordInput, label="Yangi parolni tasdiqlash")

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(id=self.instance.id).exists():
            raise forms.ValidationError("Bu pochta mavjud.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password') 
        if password != confirm_password:
            raise forms.ValidationError("Parollar to'g'ri kelmadi.")
        if len(password)==0 or len(confirm_password)==0:
            raise forms.ValidationError("Parol bo'sh bo'lmaydi")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password: 
            user.set_password(password)
        if commit:
            user.save()
        return user