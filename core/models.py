import hashlib

from django.conf import settings
from django.utils import timezone
from django.db import models
from django.core.exceptions import FieldError
from django.db.models.fields.related import ManyToManyField

from model_utils import FieldTracker


class DeletedManager(models.Manager):
	def get_queryset(self):
		return super(DeletedManager, self).get_queryset().exclude(is_deleted=True)

class BaseMeta():
	ordering = ['id']

class AbstractFieldTracker(FieldTracker):
    def finalize_class(self, sender, name, **kwargs):
        self.name = name
        self.attname = '_%s' % name
        if not hasattr(sender, name):
            super(AbstractFieldTracker, self).finalize_class(sender, **kwargs)

class SuperModel(models.Model):
	created_date = models.DateTimeField()
	updated_date = models.DateTimeField()
	composite_id = models.CharField(max_length=255)
	is_deleted = models.NullBooleanField()

	objects = DeletedManager()

	def __init__(self, *args, **kwargs):
		AbstractFieldTracker().finalize_class(self.__class__, 'tracker')
		# e.g. self.tracker.previous('< fieldname >')
		super(SuperModel, self).__init__(*args, **kwargs)
	
	def save(self, *args, **kwargs):
		curr_time = timezone.now()
		if not self.id:
			self.created_date = curr_time
			self.composite_id = hashlib.sha256(str(self._meta.db_table) + str(curr_time)).hexdigest()
		self.updated_date = curr_time
		super(SuperModel, self).save(*args, **kwargs)

	def delete(self, *args, **kwargs):
		self.is_deleted = True
		super(SuperModel, self).save(*args, **kwargs)

	def to_dict(self):
		opts = self._meta
		data = {}
		for f in opts.concrete_fields + opts.many_to_many:
			if isinstance(f, ManyToManyField):
				if self.pk is None:
					data[f.name] = []
				else:
					data[f.name] = list(f.value_from_object(self).values_list('pk', flat=True))
			else:
				data[f.name] = f.value_from_object(self)
		return data

	@classmethod
	def get_fields(cls):
		return {str(field.column): str(field.get_internal_type())\
					for field in cls._meta.fields}

	class Meta(BaseMeta):
		abstract = True
