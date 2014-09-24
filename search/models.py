from django.db import models

# Create your models here.

class Person(models.Model):
	first_name = models.CharField(max_length=20)
	last_name = models.CharField(max_length=30)
	current_affiliation = models.CharField(max_length=30)
	most_recent_university_studied = models.CharField(max_length=50)
	field_of_study = models.CharField(max_length=25)
	subfield1 = models.CharField(max_length=25)
	subfield2 = models.CharField(max_length=25)
	subfield3 = models.CharField(max_length=25)
	popularity = models.IntegerField(default='0')
	most_recent_modification = models.DateTimeField('most_recent_modification')
	most_recent_modifier = models.CharField(max_length=25)

	def __str__(self):
		return self.first_name+' '+self.last_name