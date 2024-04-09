from django import forms
from .models import Artwork

class ArtworkForm(forms.ModelForm):
    image = forms.FileField(label="Изображение",widget=forms.FileInput(attrs={'class': 'txt-input','id':'img_file'}))
    title = forms.CharField(label="Название",widget=forms.TextInput(attrs={'class': 'txt-input'}),help_text="Введите название")
    desc = forms.CharField(label="Описание",widget=forms.Textarea(attrs={'class': 'txt-input'}))
    date = forms.DateField(label="Дата",widget=forms.DateInput(attrs={'class': 'txt-input', 'type':'date'}))
    url = forms.CharField(label="В сотрудничестве",widget=forms.TextInput(attrs={'class': 'txt-input'}))
    id = forms.CharField(label="id_img", widget=forms.TextInput(attrs={'class': 'txt-input', 'hidden':"hidden"}))
    # title.label = ('port_label',)
    class Meta:
        model = Artwork
        fields = [
            'image',
            # 'thumb',
            'title',
            'desc',
            'date',
            'url',
            'id',
        ]
