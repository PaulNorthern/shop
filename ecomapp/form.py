from django import forms 
from django.utils import timezone



class OrderForm(forms.Form):
    name = forms.CharField()
    last_name = forms.CharField(required=False)
    phone = forms.CharField()
    buying_type = forms.ChoiceField(widget=forms.Select(), choices=([("self", "Самовызов"), ("delivery", "Доставка")]))
    date = forms.DateField(widget=forms.SelectDateWidget(), initial=timezone.now())
    address = forms.CharField(required=False)
    comments = forms.CharField(widget=forms.Textarea, required=False)

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = 'Имя'
        self.fields['last_name'].label = 'Фамилия'
        self.fields['phone'].label = 'Контактный телефон'
        self.fields['phone'].help_text = 'Укажите реальный номер для связи'
        self.fields['buying_type'].label = 'Способ получения'
        self.fields['address'].label = 'Адрес доставка'
        self.fields['address'].help_text = 'Обязательно укажите город'
        self.fields['comments'].label = 'Комментарий к заказу'
        self.fields['date'].label = 'Дата доставки'
        self.fields['date'].help_text = 'Доставка осущ-ся на след день после оформления заказа'