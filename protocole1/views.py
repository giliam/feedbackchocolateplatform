import random

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, render, redirect, reverse
from django.views.decorators.debug import sensitive_post_parameters

from protocole1 import forms, models


##
# HOMEPAGE
##


@login_required
def homepage(request):
    experiments_available = models.Experiment.objects.filter(running=True)
    results = models.Result.objects.filter(user=request.user)
    results_filtered = {}
    for result in results.all():
        results_filtered[result.experiment.id] = result.finished

    return render(
        request,
        "homepage.html",
        {"experiments_available": experiments_available, "results": results_filtered},
    )


##
# RESULTS
##


@login_required
def results_experiment(request, experiment_id):
    experiment = get_object_or_404(models.Experiment, Q(id=experiment_id, running=True))
    experiment_groups = models.ExperimentGroups.objects.prefetch_related(
        "group", "group__ideas"
    ).filter(experiment=experiment)
    results = models.Result.objects.prefetch_related("user", "reactions_ideas").filter(
        experiment=experiment
    )
    reactions_ideas = models.ResultOnIdea.objects.prefetch_related(
        "result", "result__experiment"
    ).filter(result__experiment=experiment)
    reactions_ideas_result = {}
    for reaction in reactions_ideas.all():
        reactions_ideas_result[reaction.result.id] = reactions_ideas_result.get(
            reaction.result.id, []
        ) + [reaction]
    groups = sort_by_grouptype(experiment_groups.all())

    return render(
        request,
        "results_experiment.html",
        {
            "experiment": experiment,
            "results": results,
            "reactions_ideas_result": reactions_ideas_result,
        },
    )


##
# PARTICIPATION
##


def get_next_idea(ideas):
    return random.choice(ideas)


def get_next_step_feedback(experiment_ideas, expansion_rate=0.2):
    will_expand = random.random()
    if will_expand <= expansion_rate:
        expansion = True
        idea = get_next_idea(experiment_ideas[models.GroupType.EXPANSION])
    else:
        expansion = False
        idea = get_next_idea(experiment_ideas[models.GroupType.FIXATION])
    return idea, expansion


def sort_by_grouptype(groups):
    group_fix = groups.filter(group_type_here=models.GroupType.FIXATION.value)
    ideas_fix = [idea for group in group_fix.all() for idea in group.group.ideas.all()]
    group_exp = groups.filter(group_type_here=models.GroupType.EXPANSION.value)
    ideas_exp = [idea for group in group_exp.all() for idea in group.group.ideas.all()]
    return {models.GroupType.FIXATION: ideas_fix, models.GroupType.EXPANSION: ideas_exp}


def remove_already_used_ideas(groups, reactions_ideas):
    ideas_already_used = [reaction.idea for reaction in reactions_ideas.all()]
    for idea in ideas_already_used:
        if idea in groups[models.GroupType.FIXATION]:
            groups[models.GroupType.FIXATION].remove(idea)
        elif idea in groups[models.GroupType.EXPANSION]:
            groups[models.GroupType.EXPANSION].remove(idea)
    return groups


def create_next_idea(experiment, groups, result):
    next_idea, did_expand = get_next_step_feedback(
        groups, experiment.starting_expansion_rate
    )
    new_order = len(result.reactions_ideas.all())
    next_result = models.ResultOnIdea(
        idea=next_idea,
        result=result,
        order=new_order,
        did_expand=did_expand,
        reaction=models.Reactions.NEUTRAL.value,
    )
    next_result.save()
    return next_idea, did_expand


@login_required
def participate_experiment(request, experiment_id):
    experiment = get_object_or_404(models.Experiment, Q(id=experiment_id, running=True))
    experiment_groups = models.ExperimentGroups.objects.prefetch_related(
        "group", "group__ideas"
    ).filter(experiment=experiment)
    result = models.Result.objects.filter(experiment=experiment, user=request.user)
    groups = sort_by_grouptype(experiment_groups.all())

    if result.count() > 0:
        result = result[0]
        if result.finished:
            return redirect(reverse("protocole1.homepage"))
        reactions_ideas = models.ResultOnIdea.objects.filter(result=result).all()
        if len(reactions_ideas) > 0:
            last_result = reactions_ideas[len(reactions_ideas) - 1]
            if last_result.reaction != models.Reactions.NEUTRAL.value:
                groups = remove_already_used_ideas(groups, reactions_ideas)
                if (
                    len(groups[models.GroupType.EXPANSION]) == 0
                    or len(groups[models.GroupType.FIXATION]) == 0
                ):
                    result.finished = True
                    return redirect(reverse("protocole1.homepage"))
                next_idea, did_expand = create_next_idea(experiment, groups, result)
            elif "reaction" in request.GET:
                reaction = int(request.GET["reaction"])
                if reaction >= 1:
                    reaction = models.Reactions(reaction)
                    result.update_expansion_rate(last_result.did_expand, reaction)
                    result.save()
                    last_result.reaction = reaction.value
                    last_result.expansion_rate = result.expansion_rate
                    last_result.save()
                    return redirect(
                        reverse(
                            "protocole1.participate_experiment", args=[experiment.id]
                        )
                    )
                else:
                    next_idea = last_result.idea
            else:
                next_idea = last_result.idea
    else:
        result = models.Result(
            user=request.user,
            experiment=experiment,
            expansion_rate=experiment.starting_expansion_rate,
        )
        result.save()

        next_idea, did_expand = create_next_idea(experiment, groups, result)

    return render(
        request,
        "participate_experiment.html",
        {
            "experiment": experiment,
            "next_idea": next_idea,
            "reactions": [rea for rea in models.Reactions if rea.value > 0],
        },
    )


##
# USER PAGES
##


@sensitive_post_parameters("password")
def log_in(request):
    error = False
    if request.method == "POST":
        form = forms.ConnectionForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data[
                "username"
            ]  # Nous récupérons le nom d'profile_user
            password = form.cleaned_data["password"]  # … et le mot de passe
            user = authenticate(
                username=username, password=password
            )  # Nous vérifions si les données sont correctes
            if user:  # Si l'objet renvoyé n'est pas None
                login(request, user)  # nous connectons l'profile_user
                return redirect("homepage")
            else:  # sinon une erreur sera affichée
                error = True
    else:
        if request.user.is_authenticated:
            return redirect("homepage")
        form = forms.ConnectionForm()
    return render(
        request,
        "users_login.html",
        {"form": form, "user": request.user, "error": error},
    )


@login_required
def log_out(request):
    logout(request)
    return redirect(reverse(log_in))
