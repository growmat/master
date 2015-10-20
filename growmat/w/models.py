from django.db import models
from django.forms import ModelForm
from django.views.generic import ListView
from django.views.generic import DetailView
from django.core.urlresolvers import reverse




# Create your models here.
class Instrument(models.Model):
	
	NT = 1<<0
	IV = 1<<1
	W  = 1<<2
	A  = 1<<3
	
	INSTRUMENT_TYPE = (
					(0, 'SYSTEM'),
					(10, 'OUTPUT'),
     				(20, 'THERMOMETER'),
         			(30, 'HUMIDITYMETER'),
    			    (40, 'DISTANCEMETER'),
    				(50, 'PHMETER'),    				
	)
	
	INSTRUMENT_INDEX = (
					(0, '0'),
     				(1, '1'),
         			(2, '2'),
    			    (3, '3'),
    				(4, '4'),
    				(5, '5'),
     				(6, '6'),
         			(7, '7'),
    			    (8, '8'),
    				(9, '9'),
	)
	
	address = models.IntegerField(default=0)
	type = models.IntegerField(choices=INSTRUMENT_TYPE, default=0)
	index = models.IntegerField(choices=INSTRUMENT_INDEX, default=0)
	name = models.CharField(default='NEW',  max_length=256)
	value = models.FloatField(default=0, null=True, blank=True)
	status = models.IntegerField(default=0, null=True, blank=True) 
	datetime = models.DateTimeField(null=True, blank=True) 
	
	#def get_absolute_url(self):
	#	return reverse('list', kwargs={'pk': self.pk})
	def get_fields(self):
		return [(field.name, field.value_to_string(self)) for field in Instrument._meta.fields]
	
class InstrumentForm(ModelForm):
    class Meta:
        model = Instrument
        fields = ['address', 'type', 'index', 'name', 'value', 'status', 'datetime']


class InstrumentList(ListView):
	model = Instrument
		#queryset = Instrument.objects.all()
		#fields = ['address', 'type', 'index', 'name', 'value', 'status', 'datetime']		
#class Choice(models.Model):
#    question = models.ForeignKey(Question)
#    choice_text = models.CharField(max_length=200)
#    votes = models.IntegerField(default=0)


class Period(models.Model):
	name = models.CharField(default='NEW',  max_length=256)
	time_from = models.TimeField()
	time_to = models.TimeField()
	description = models.CharField(null=True, blank=True,  max_length=256) 
	
	

class PeriodForm(ModelForm):
    class Meta:
        model = Period
        fields = ['name', 'time_from', 'time_to', 'description']	
        


class Rule(models.Model):	

	
	ATTRIBUTE_TYPE = (
					('VALUE', 'VALUE'),
     				('STATUS', 'STATUS'),
         			('NT', 'NT'),
    			    ('IV', 'IV'),
    			    ('W', 'WARNING'),
    			    ('A', 'ALARM'),
	)
	
	OPERATION_TYPE = (
					('<', '<'),
     				('=', '='),
         			('>', '>'),
    			    ('!=', '!='),
    			    ('&', 'AND'),
    			    ('|', 'OR'),
	)
	
	ACTION_TYPE = (
					('=', '='),
					('&', 'AND'),
					('|', 'OR'),
	)
	

	period = models.ForeignKey(Period)
	input = models.ForeignKey(Instrument, related_name='input_instrument')
	input_attribute = models.CharField(choices=ATTRIBUTE_TYPE, default=0, max_length=6)
	operation = models.CharField(choices=OPERATION_TYPE, default=0, max_length=2)
	input_parameter = models.FloatField(default=0, blank=True)
	output = models.ForeignKey(Instrument, related_name='output_instrument')
	output_attribute = models.CharField(choices=ATTRIBUTE_TYPE, default=0, max_length=6)
	action = models.CharField(choices=ACTION_TYPE, default=0, max_length=3)
	output_parameter = models.FloatField(default=0, blank=True)
	description = models.CharField(null=True, blank=True,  max_length=256) 
	result = models.BooleanField(default=False, blank=True) 
	result0 = models.BooleanField(default=False, blank=True) 
	datetime = models.DateTimeField(null=True, blank=True) 

class RuleForm(ModelForm):
    class Meta:
        model = Rule
        fields = ['period', 'input', 'input_attribute', 'operation', 'input_parameter', 'output', 'output_attribute', 'action', 'output_parameter', 'description', 'result', 'result0', 'datetime']
        
    def __init__(self, *args, **kwargs):
        super(RuleForm, self).__init__(*args, **kwargs)
        self.fields['input'].queryset = Instrument.objects.all()
        self.fields['input'].label_from_instance = lambda obj: "%s" % (obj.name)
        self.fields['output'].queryset = Instrument.objects.all()
        self.fields['output'].label_from_instance = lambda obj: "%s" % (obj.name)
        
        self.fields['period'].queryset = Period.objects.all()
        self.fields['period'].label_from_instance = lambda obj: "%s" % (obj.name)
        
        
class Archive(models.Model):	
	instrument = models.ForeignKey(Instrument)
	value = models.FloatField(default=0, null=True, blank=True)
	status = models.IntegerField(default=0, null=True, blank=True)
	datetime = models.DateTimeField(null=True, blank=True) 
	

	
	
	 

	