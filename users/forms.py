from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        label="Usuário",
        required=True,
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "digite seu usuário"
            }
        )
    )

    email = forms.EmailField(
        label="Email",
        required=True,
        max_length=100,
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Ex.: joao_silva@xpto.com"
            }
        ) 
    )

    password1 = forms.CharField(
        label="Senha",
        required=True,
        max_length=30,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Digite uma senha"
            }
        )
    )

    password2 = forms.CharField(
        label="Confirmação de Senha",
        required=True,
        max_length=30,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Confirme sua senha"
            }
        )
    )

    def clean_username(self):
        name = self.cleaned_data.get('username')

        if name:
            name = name.strip()
            if ' ' in name:
                raise forms.ValidationError('Não utilize espaços no nome de usuário.')
            elif not name.islower():
                raise forms.ValidationError("Nome de usuário não deve conter letras maiúsculas.")
            else:
                return name
            
    def clean_password2(self):
        pass_1 = self.cleaned_data.get('password1')
        pass_2 = self.cleaned_data.get('password2')

        if pass_1 and pass_2:
            if pass_1 != pass_2:
                raise forms.ValidationError("As senhas não são iguais!")
            elif len(pass_2) < 8:
                raise forms.ValidationError("A senha deve conter pelo menos 8 caracteres.")
            elif pass_2.lower() == pass_2:
                raise forms.ValidationError("A senha deve conter pelo menos um caractere maiúsculo.")
            elif pass_2.upper() == pass_2:
                raise forms.ValidationError("A senha deve conter pelo menos um caractere minúsculo.")
            else:
                return pass_2
            
    class Meta:
        model = CustomUser
        fields = UserCreationForm.Meta.fields
        widgets = {'transactions':forms.HiddenInput(), 'wallet':forms.HiddenInput()}

    field_order = ["username", "email", "password1", "password2"]

class CustomUserChangeForm(UserChangeForm):
    username = forms.CharField(
        label="Usuário",
        required=True,
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Digite seu usuário."
            }
        )
    )

    password = forms.CharField(
        label="Senha",
        required=True,
        max_length=30,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Digite sua senha"
            }
        )
    )

class LoginForms(forms.Form):
    username = forms.CharField(
        label="Usuário",
        required=True,
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Digite seu usuário."
            }
        )
    )

    password = forms.CharField(
        label="Senha",
        required=True,
        max_length=30,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Digite sua senha"
            }
        )
    )

class DepositForm(forms.Form):
    amount = forms.FloatField(
        label="Digite o valor que deseja depositar.",
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control text-center",
                "placeholder": "Digite aqui.",
                "onkeydown": "javascript: return event.keyCode == 69 ? false : true",
                "min": "1",
                "step": ".01"
            }
        )
    )

class TransferForm(forms.Form):

    email = forms.CharField(
        label="Email",
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Digite aqui o email do Usuário."
            }
        )
    )

    amount = forms.FloatField(
        label="Valor da Transferência.",
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Digite aqui.",
                "onkeydown": "javascript: return event.keyCode == 69 ? false : true",
                "min": "1",
                "step": ".01"
            }
        )
    )