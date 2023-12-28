from django import forms  
from smsapp.models import AudioFile, records, group, broadcastmessagecat, broadcastmessagedis,broadcastmessageall, grade


class RecordsForm(forms.ModelForm):
	class Meta:
		model = records
		exclude = ['status','group']
		
		widgets = {
            'EmpNumber': forms.TextInput (attrs={'class': 'form-control', 'placeholder':'Enter employment number'}),
            'Title': forms.Select (attrs={'class': 'form-control'}),
            'FirstName': forms.TextInput (attrs={'class': 'form-control', 'placeholder':'First Name'}),
            'LastName': forms.TextInput (attrs={'class': 'form-control', 'placeholder':'Last Name'}),
            'OtherName': forms.TextInput (attrs={'class': 'form-control', 'placeholder':'Other Name'}),
            'Gender': forms.Select (attrs={'class': 'form-control'}),
            'DOB': forms.TextInput (attrs={'type':'date', 'class': 'form-control'}),
            'MaritalStatus': forms.Select (attrs={'class': 'form-control'}),
            'Religion': forms.Select (attrs={'class': 'form-control'}),
            'OfficialEmail': forms.EmailInput (attrs={'type':'email', 'class': 'form-control', 'placeholder':'Eg: joe@email.com'}),
            'PersonalEmail': forms.EmailInput (attrs={'class': 'form-control', 'placeholder':'Eg: joe@email.com'}),
            'Mobile': forms.TextInput (attrs={'class': 'form-control', 'placeholder':'10 digits number', 'title':'Must be 10 digits only', 'pattern':'\d{10}'}),
            'Mobile1': forms.TextInput (attrs={'class': 'form-control', 'placeholder':'10 digits number'}),
            'FirstAppDate': forms.TextInput (attrs={'type':'date', 'class': 'form-control'}),
            'AssumptionDutyDate': forms.TextInput (attrs={'type':'date', 'class': 'form-control'}),
            'category': forms.Select (attrs={'class': 'form-control'}),
            'grade': forms.Select (attrs={'class': 'form-control'}),
            'bmc': forms.Select (attrs={'class': 'form-control'}),
            'unit': forms.Select (attrs={'class': 'form-control'}),
            
           # 'group': forms.Select (attrs={'class': 'form-control'}),
            
        }
        
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['grade'].queryset = grade.objects.none()
        
		if 'category' in self.data:
			try:
				category_id = int(self.data.get('category'))
				self.fields['grade'].queryset = grade.objects.filter(category_id=category_id).order_by('grade')
			except (ValueError, TypeError):
				pass  # invalid input from the client; ignore and fallback to empty City queryset
		elif self.instance.pk:
			self.fields['grade'].queryset = self.instance.category.grade_set.order_by('grade')

        
        
class BroadcastmessagecatForm(forms.ModelForm):
	class Meta:
		model = broadcastmessagecat
		fields = '__all__'
		
		widgets = {
			'theme': forms.Select (attrs={'class': 'form-control'}),
			'Content': forms.Textarea (attrs={'class': 'form-control', "rows":5, 'placeholder':'Enter the content of your message here'}),
			'category':forms.Select (attrs={'class': 'form-control'}),
            #'Group': forms.Select (attrs={'class': 'form-control'}),
        
            
        }

class BroadcastmessageallForm(forms.ModelForm):
	class Meta:
		model = broadcastmessageall
		fields = '__all__'
		
		widgets = {
			'Subject': forms.TextInput (attrs={'class': 'form-control', 'placeholder':'Eg: Pin Renewal'}),
			'Content': forms.Textarea (attrs={'class': 'form-control', "rows":5, 'placeholder':'Enter the content of your message here'}),
			#'category':forms.SelectMultiple (attrs={'class': 'form-control'}),
            #'Group': forms.Select (attrs={'class': 'form-control'}),
        
            
        }
        
class BroadcastmessagedisForm(forms.ModelForm):
	class Meta:
		model = broadcastmessagedis
		fields = '__all__'
		
		widgets = {
			'Subject': forms.TextInput (attrs={'class': 'form-control', 'placeholder':'Eg: Pin Renewal'}),
			'Content': forms.Textarea (attrs={'class': 'form-control', "rows":5, 'placeholder':'Enter the content of your message here'}),
			'district':forms.Select (attrs={'class': 'form-control'}),
            #'Group': forms.Select (attrs={'class': 'form-control'}),
        
            
        }

class GroupForm(forms.ModelForm):
	class Meta:
		model = group
		fields = '__all__'
		
		widgets = {
            'groupName': forms.TextInput (attrs={'class': 'form-control'}),
        
        }

class AudioFileForm(forms.ModelForm):
    class Meta:
        model = AudioFile
        #fields = ('file',)
        fields = '__all__'
        
