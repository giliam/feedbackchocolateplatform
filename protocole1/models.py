from enum import Enum

from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User


class Reactions(Enum):
    NEUTRAL = 0
    CONTINUE = 1
    EXPAND = 2
    STOP = 3


class GroupType(Enum):
    FIXATION = 0
    EXPANSION = 1


class Idea(models.Model):
    value = models.CharField(max_length=50)

    def __str__(self):
        return "Idea %s" % self.value

    class Meta:
        verbose_name = "Idea"
        verbose_name_plural = "Ideas"


class IdeasGroup(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(default="")
    ideas = models.ManyToManyField(Idea, related_name="groups")

    def __str__(self):
        return "IdeasGroup %s" % self.name

    class Meta:
        verbose_name = "IdeasGroup"
        verbose_name_plural = "IdeasGroups"
        ordering = ["name"]


def validate_expansion_rate(value):
    if value < 0 or value > 1:
        raise ValidationError(
            "%(value)s is not between 0 and 1", params={"value": value}
        )


class Experiment(models.Model):
    description = models.TextField(default="")
    experiment_groups = models.ManyToManyField(IdeasGroup, through="ExperimentGroups")
    password = models.CharField(max_length=150, null=True, blank=True)
    running = models.BooleanField()
    starting_expansion_rate = models.FloatField(
        default=0.2, validators=[validate_expansion_rate]
    )

    def __str__(self):
        return "Experiment #%s" % (self.id,)

    class Meta:
        verbose_name = "Experiment"
        verbose_name_plural = "Experiments"


class ExperimentGroups(models.Model):
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    group = models.ForeignKey(IdeasGroup, on_delete=models.CASCADE)
    group_type_here = models.PositiveIntegerField(
        choices=[(group_type.value, group_type) for group_type in GroupType]
    )

    def __str__(self):
        return "ExperimentGroups for group %s in experiment %s" % (
            self.group.name,
            self.experiment.id,
        )

    class Meta:
        verbose_name = "ExperimentGroup"
        verbose_name_plural = "ExperimentGroups"
        ordering = ["experiment"]


class Result(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="results"
    )
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    expansion_rate = models.FloatField(
        default=0.2, validators=[validate_expansion_rate]
    )
    reactions_ideas = models.ManyToManyField(Idea, through="ResultOnIdea")
    finished = models.BooleanField(default=False)

    def update_expansion_rate(self, did_expand, reaction):
        if did_expand:
            if reaction == Reactions.CONTINUE:
                if self.expansion_rate < 1:
                    self.expansion_rate += 0.05

            if reaction == Reactions.EXPAND:
                if self.expansion_rate > 0:
                    self.expansion_rate -= 0.05
        else:
            if reaction == Reactions.EXPAND:
                if self.expansion_rate < 1:
                    self.expansion_rate += 0.05

            if reaction == Reactions.CONTINUE:
                if self.expansion_rate > 0:
                    self.expansion_rate -= 0.05
        return min(max(self.expansion_rate, 0), 1)

    def __str__(self):
        return "Result of %s on %s" % (self.user, self.experiment)

    class Meta:
        verbose_name = "Result"
        verbose_name_plural = "Results"
        ordering = ["experiment", "user"]


class ResultOnIdea(models.Model):
    idea = models.ForeignKey(Idea, on_delete=models.SET_NULL, null=True)
    result = models.ForeignKey(Result, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()
    did_expand = models.BooleanField(default=False)
    expansion_rate = models.FloatField(
        default=0.2, validators=[validate_expansion_rate]
    )
    reaction = models.PositiveIntegerField(
        choices=[(reaction.value, reaction) for reaction in Reactions], default=-1
    )

    def __str__(self):
        return "Result #%s on idea %s (%s)" % (self.order, self.idea, self.result)

    class Meta:
        verbose_name = "ResultOnIdea"
        verbose_name_plural = "ResultOnIdeas"
        ordering = ["result", "order", "idea"]
