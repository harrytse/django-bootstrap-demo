#coding=utf-8
from django import forms

clienttypes = [('all','全部'),('gaode','高德'),('dianping','大众点评')]
postypes = [('gpoi','gpoi'),('shoppoi','shoppoi'),('mpoi','mpoi')]
sorttypes = [('dpscore','默认排序'),('dist','最近优先'),('shoppower','最高评分')]

class DefaultForm(forms.Form):
    keyword = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'value': '','style': 'width:400px;'}))
    clienttype = forms.ChoiceField(choices=clienttypes, required=False, widget=forms.Select(attrs={'style': 'width:200px'}))
    sorttype = forms.ChoiceField(choices=sorttypes, required=False, widget=forms.Select(attrs={'style': 'width:200px'}))
    postype = forms.ChoiceField(choices=postypes, required=False, widget=forms.Select(attrs={'style': 'width:200px'}))
    distance = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'value': '','style': 'width:400px;'}))
    lng = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'value': '','style': 'width:400px;'}))
    lat = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'value': '','style': 'width:400px;'}))
    
class SearchForm(forms.Form):
    query = forms.CharField(widget=forms.Textarea(attrs={'value': '','style': 'width:500px;'}))
    lng = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'value': '','style': 'width:400px;'}))
    lat = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'value': '','style': 'width:400px;'}))
    geoLatLng = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'value': '','style': 'width:400px;'}))
    distLatLng = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'value': '','style': 'width:400px;'}))


