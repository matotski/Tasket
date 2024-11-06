# from django import forms
# from django.contrib.auth.forms import UserCreationForm
# from .models import User
#
#
# class UserRegistration(UserCreationForm):
#     ROLES = ["РП", "МРП", "Cт.специалист", "Мл.Специалист"]
#     first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Введите имя'}))
#     last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Введите фамилию"}))
#     email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Введите email"}))
#     role = forms.ChoiceField(widget=forms.Select(attrs={"placeholder": "Выберите вашу роль"}, choices=ROLES))
#     password1 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Придумайте пароль"}))
#     password2 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Подтвердите пароль"}))
#
#     class Meta:
#         model = User
#         fields = ['first_name', 'last_name', 'email', 'role', 'password']
