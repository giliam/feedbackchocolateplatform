from enum import Enum

from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User


class Reactions(Enum):
    """
    Contains the possible reactions
    """

    UNDEFINED = 0
    CONTINUE = 1
    EXPAND = 2
    NEUTRAL = 3


class GroupType(Enum):
    """
    Different type for the groups of ideas
    """

    FIXATION = 0
    EXPANSION = 1


class Idea(models.Model):
    """
    The basic idea to evaluate.

    :param value: the content of the idea
    :type value: str
    """

    value = models.CharField(max_length=50)

    def __str__(self):
        return "Idea %s" % self.value

    class Meta:
        verbose_name = "Idea"
        verbose_name_plural = "Ideas"


class IdeasGroup(models.Model):
    """
    A group of ideas (gathered to be easier to manipulate)
    
    :param name: the name of the group
    :type name: str
    :param description: the description of the group
    :type description: str
    :param ideas: the ideas of this group
    :type ideas: ManyToMany relation
    """

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
    """
    Checks that the expansion rate is between 0 and 1 (included)
    
    :param value: the expansion rate to check
    :type value: float
    :raises ValidationError: when the expansion rate is invalid
    """
    if value < 0 or value > 1:
        raise ValidationError(
            "%(value)s is not between 0 and 1", params={"value": value}
        )


class Experiment(models.Model):
    """
    A group of ideas (gathered to be easier to manipulate)
    
    :param name: the name of the group
    :type name: str
    :param description: the description of the group
    :type description: str
    :param experiment_groups: the groups used in this experiment
    :type experiment_groups: ManyToMany relation
    :param password: a password protecting the experiment (unused yet)
    :type password: str
    :param running: whether this experiment is running or not
    :type running: boolean
    :param limit_ideas_number: limits the number of ideas proposed to the user 
                                (if -1, no limitation is applied)
    :type limit_ideas_number: int field, default -1
    :param starting_expansion_rate: the starting expansion rate of the experiment
    :type starting_expansion_rate: float field between 0 and 1 (included)
    """

    name = models.CharField(max_length=150, default="experiment")
    description = models.TextField(default="")
    experiment_groups = models.ManyToManyField(IdeasGroup, through="ExperimentGroups")
    password = models.CharField(max_length=150, null=True, blank=True)
    running = models.BooleanField()
    limit_ideas_number = models.IntegerField(default=-1)
    starting_expansion_rate = models.FloatField(
        default=0.2, validators=[validate_expansion_rate]
    )

    def __str__(self):
        return "Experiment #%s : %s" % (self.id, self.name)

    class Meta:
        verbose_name = "Experiment"
        verbose_name_plural = "Experiments"


class ExperimentGroups(models.Model):
    """
    A group selected for an experiment
    
    :param experiment: the experiment considered
    :type experiment: Experiment ForeignKey
    :param group: the group of ideas concerned
    :type group: IdeasGroup ForeignKey
    :param group_type_here: the type of the group in this experiment
    :type group_type_here: GroupType
    """

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
        unique_together = ("experiment", "group")


class Result(models.Model):
    """
    The result of a user on an experiment
    
    :param user: the user considered
    :type user: Django User ForeignKey
    :param experiment: the experiment considered
    :type experiment: Experiment ForeignKey
    :param expansion_rate: the expansion rate 
    :type expansion_rate: float
    :param reactions_ideas: the reactions of the user on the ideas submitted
    :type reactions_ideas: Idea ManyToMany
    :param finished: whether the user has finished or not
    :type finished: boolean
    """

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
        """
        Applies the algorithm to the expansion rate based on user's reaction and
        on whether expansion did or did not occurr.
        
        :param did_expand: did or did not expand
        :type did_expand: boolean
        :param reaction: the reaction of the user
        :type reaction: Reactions
        :return: the expansion rate
        :rtype: float between 0 and 1 (included)
        """
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
    """
    Makes the link between a user result on an experiment and an idea seen
    
    :param idea: the idea considered
    :type idea: Idea ForeignKey
    :param result: the result concerned
    :type result: Result ForeignKey
    :param order: the order in which the user has seen this idea
    :type order: positive integer
    :param did_expand: whether the algorithm did expand on this idea
    :type did_expand: boolean
    :param expansion_rate: the expansion rate after the reaction of the user on this idea
    :type expansion_rate: float
    :param reaction: the user's reaction
    :type reaction: Reactions
    """

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
