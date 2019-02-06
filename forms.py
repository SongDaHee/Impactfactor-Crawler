from django import forms
#from .models import 

class PostForm(forms.Form):
    #class Meta:
        #field=('name1','name2',)
    pName=forms.CharField(initial='None',label='pName',max_length=100,required=False)
    ckbox1=forms.BooleanField(label='chkbox1',required=False)
    
    sName=forms.CharField(initial='None',label='sName',max_length=200,required=False)
    ckbox2=forms.BooleanField(label='chkbox2',required=False)