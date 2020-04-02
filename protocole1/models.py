from enum import Enum

from django.db import models
from django.contrib.auth.models import User


class Reactions(Enum):
    CONTINUE = 0
    EXPAND = 1
    STOP = 2


class GroupeType(Enum):
    FIXATION = 0
    EXPANSION = 1


class Idea(models.Model):
    value = models.CharField(max_length=50)


class IdeasGroup(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(default="")
    ideas = models.ManyToManyField(Idea, related_name="groups")


class Experiment(models.Model):
    groups = models.ManyToManyField(IdeasGroup, through="ExperimentGroups")
    password = models.CharField(max_length=150)
    running = models.BooleanField()


class ExperimentGroups(models.Model):
    experience = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    groupe = models.ForeignKey(IdeasGroup, on_delete=models.CASCADE)
    type_groupe_dans_experience = models.CharField(
        max_length=5,
        choices=[(groupe_type, groupe_type.value) for groupe_type in GroupeType],
    )


class Result(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="results"
    )
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    expansion_rate = models.IntegerField()
    reactions_ideas = models.ManyToManyField(Idea, through="ResultOnIdea")


class ResultOnIdea(models.Model):
    idea = models.ForeignKey(Idea, on_delete=models.SET_NULL, null=True)
    result = models.ForeignKey(Result, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()
    reaction = models.CharField(
        max_length=5, choices=[(reaction, reaction.value) for reaction in Reactions]
    )
