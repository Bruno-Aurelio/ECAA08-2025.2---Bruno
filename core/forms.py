from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Problema, PerfilOficina, Especialidade

# Formulário de Cadastro de Cliente
class ClienteSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_cliente = True
        if commit:
            user.save()
        return user

# Formulário de Cadastro de Oficina (CORRIGIDO)
class OficinaSignUpForm(UserCreationForm):
    # Campos extras para já criar o perfil junto
    nome_oficina = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome da Oficina'}))
    endereco = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Endereço Completo'}))

    class Meta(UserCreationForm.Meta):
        model = User
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_oficina = True
        if commit:
            user.save()
            # Cria o perfil da oficina automaticamente
            # CORREÇÃO FEITA AQUI: PerfilOficina com 'O' maiúsculo
            PerfilOficina.objects.create(
                usuario=user,
                nome_oficina=self.cleaned_data['nome_oficina'],
                endereco=self.cleaned_data['endereco']
            )
        return user

# Formulário de Problema (Com Imagem)
class ProblemaForm(forms.ModelForm):
    class Meta:
        model = Problema
        fields = ['titulo', 'modelo_carro', 'descricao', 'imagem']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'modelo_carro': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'imagem': forms.FileInput(attrs={'class': 'form-control'}),
        }

# Formulário de Perfil da Oficina (Edição)
class OficinaPerfilForm(forms.ModelForm):
    class Meta:
        model = PerfilOficina
        fields = ['nome_oficina', 'endereco', 'especialidades']
        widgets = {
            'nome_oficina': forms.TextInput(attrs={'class': 'form-control'}),
            'endereco': forms.TextInput(attrs={'class': 'form-control'}),
            'especialidades': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        }