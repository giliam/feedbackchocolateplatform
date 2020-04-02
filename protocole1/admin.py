from django.contrib import admin

from protocole1 import models

admin.site.register(models.Idea)
admin.site.register(models.IdeasGroup)
admin.site.register(models.Experiment)
admin.site.register(models.ExperimentGroups)
admin.site.register(models.Result)
admin.site.register(models.ResultOnIdea)
