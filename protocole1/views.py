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
    """
    The homepage view: presents the experiments available (i.e. running) to the 
    user. If the user has already participated, a mention will appear to mention so.
    The results of an experiment are available through a link for each experiment.
    """
    experiments_available = models.Experiment.objects.filter(running=True)
    results = models.Result.objects.filter(user=request.user)

    # Groups the result by experiment
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


def sort_by_grouptype(groups):
    """
    Sorts the groups between the two group types.
    
    :param groups: the groups to sorts
    :type groups: QuerySet
    :return: a dict with groups gathered by group type (one entry for fixation 
            groups, another one for expansion groups).
    :rtype: dict
    """
    group_fix = groups.filter(group_type_here=models.GroupType.FIXATION.value)
    ideas_fix = [idea for group in group_fix.all() for idea in group.group.ideas.all()]
    group_exp = groups.filter(group_type_here=models.GroupType.EXPANSION.value)
    ideas_exp = [idea for group in group_exp.all() for idea in group.group.ideas.all()]
    return {models.GroupType.FIXATION: ideas_fix, models.GroupType.EXPANSION: ideas_exp}


@login_required
def results_experiment(request, experiment_id):
    """
    Displays the results of a selected experiment.
    
    :param experiment_id: the experiment selected id
    :type experiment_id: int
    """
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

    # Groups the reactions by user result
    reactions_ideas_result = {}
    for reaction in reactions_ideas.all():
        reactions_ideas_result[reaction.result.id] = reactions_ideas_result.get(
            reaction.result.id, []
        ) + [reaction]
    # Sorts the groups by group type
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
    """
    Selects the next idea to display/test.
    
    :param ideas: the ideas available
    :type ideas: list
    :return: a randomly selected idea
    :rtype: Idea
    """
    return random.choice(ideas)


def get_next_step(experiment_ideas, expansion_rate=0.2):
    """
    Apply the algorithm: gets a random value and compare it to the expansion rate
    to know whether we expanded or not. If expanded, picks a random idea in
    the expansion groups. Otherwise, picks a random idea in fixation groups.
    
    :param experiment_ideas: the ideas of the experiment
    :type experiment_ideas: Idea list
    :param expansion_rate: the expansion rate to apply, defaults to 0.2
    :type expansion_rate: float, optional
    :return: the idea and whether we expanded or not
    :rtype: tuple of Idea and boolean
    """
    will_expand = random.random()
    # if the random element is less than expansion rate => expand
    if will_expand <= expansion_rate:
        expansion = True
        idea = get_next_idea(experiment_ideas[models.GroupType.EXPANSION])
    # otherwise, picks an idea in fixation group
    else:
        expansion = False
        idea = get_next_idea(experiment_ideas[models.GroupType.FIXATION])
    return idea, expansion


def remove_already_used_ideas(groups, reactions_ideas):
    """
    Removes the already used ideas from the available ideas for next step.
    
    :param groups: the groups available for next step
    :type groups: dict of ideas separated among two elements (fixation and expansion)
    :param reactions_ideas: the ideas already used by other reactions
    :type reactions_ideas: QuerySet
    :return: the dictionary filtered
    :rtype: dict of Idea
    """
    ideas_already_used = [reaction.idea for reaction in reactions_ideas.all()]
    for idea in ideas_already_used:
        # removes idea from fixation or expansion group when it has already been used
        if idea in groups[models.GroupType.FIXATION]:
            groups[models.GroupType.FIXATION].remove(idea)
        if idea in groups[models.GroupType.EXPANSION]:
            groups[models.GroupType.EXPANSION].remove(idea)
    return groups


def create_next_idea(groups, result):
    """
    Creates the next reaction for an user.
    
    :param groups: the groups available
    :type groups: dict
    :param result: the result concerned
    :type result: Result
    :return: the idea used next and whether we expanded
    :rtype: tuple of Idea and boolean
    """
    # Gets the next idea to use
    next_idea, did_expand = get_next_step(groups, result.expansion_rate)
    # Computes the step we are at in the experiment
    new_order = len(result.reactions_ideas.all())

    # Creates the new object to store the user's reaction to the idea
    # picked previously
    next_result = models.ResultOnIdea(
        idea=next_idea,
        result=result,
        order=new_order,
        did_expand=did_expand,
        reaction=models.Reactions.UNDEFINED.value,
    )
    next_result.save()

    return next_idea, did_expand


@login_required
def participate_experiment(request, experiment_id):
    """
    Make it possible to participate to an experiment through the multiple steps:

        * first create a Result object for this user and picks an idea for him 
            to evaluate if it's the first time he tries this experiment;
        * if the user already has a result object corresponding, uses this object 
            and then:
            - if the last idea seen by the user has no reaction (ie. UNDEFINED)
                and the user didn't post anything, then display the idea and the
                two links;
            - if the last idea seen by the user has no reaction (ie. UNDEFINED)
                and the user did post a reaction through GET reaction parameter,
                stores the reaction and update the expansion rate of the current
                experiment. Then redirects to the page of the experiment in order
                to avoid reacting unwillingly by refreshing the page;
            - if the last idea seen by the user has a reaction (ie. not UNDEFINED)
                - in the case a user just answered and was redirected or the user
                left the page after reacting and comes back later - checks that
                there are still ideas remaining and if so, picks the next idea 
                to display. Otherwise, finishes the user's experiment and 
                redirects to the homepage.

    :param experiment_id: the experiment considered id
    :type experiment_id: int
    """
    experiment = get_object_or_404(models.Experiment, Q(id=experiment_id, running=True))
    experiment_groups = models.ExperimentGroups.objects.prefetch_related(
        "group", "group__ideas"
    ).filter(experiment=experiment)
    result = models.Result.objects.filter(experiment=experiment, user=request.user)
    groups = sort_by_grouptype(experiment_groups.all())

    # If the user is already answering to this experiment, a result must exist
    # link to his account
    if result.count() > 0:
        result = result[0]
        # if the result is finished, redirect to the homepage
        if result.finished:
            return redirect(reverse("protocole1.homepage"))

        # otherwise, checks for the ideas proposed
        reactions_ideas = models.ResultOnIdea.objects.filter(result=result).all()

        # if there is at least one idea proposed
        if len(reactions_ideas) > 0:
            # Takes the last idea proposed
            last_result = reactions_ideas[len(reactions_ideas) - 1]
            # If the last idea proposed has already had a reaction from the user,
            # picks the next idea
            if last_result.reaction != models.Reactions.UNDEFINED.value:
                # Checks that there are ideas remaining in both EXPANSION
                # and FIXATION groups
                # OR that we exceeded the number of ideas to test per user
                groups = remove_already_used_ideas(groups, reactions_ideas)
                if (
                    len(groups[models.GroupType.EXPANSION]) == 0
                    or len(groups[models.GroupType.FIXATION]) == 0
                ) or (
                    experiment.limit_ideas_number > 0
                    and len(reactions_ideas) >= experiment.limit_ideas_number
                ):
                    # If no idea remain,
                    result.finished = True
                    result.save()
                    return redirect(reverse("protocole1.homepage"))

                # Picks the next idea
                next_idea, did_expand = create_next_idea(groups, result)

            # Case where the user has not reacted to the last idea proposed
            # BUT has sent a reaction in GET parameters
            elif "reaction" in request.GET:
                reaction = int(request.GET["reaction"])
                # If the reaction is valid (not UNDEFINED)
                if reaction >= 1:
                    reaction = models.Reactions(reaction)
                    # Updates the expansion rate
                    result.update_expansion_rate(last_result.did_expand, reaction)
                    result.save()
                    # Updates the last idea seen to register the reaction
                    # and the new expansion rate computed
                    last_result.reaction = reaction.value
                    last_result.expansion_rate = result.expansion_rate
                    last_result.save()
                    # Redirects to avoid registering the reaction twice
                    return redirect(
                        reverse(
                            "protocole1.participate_experiment", args=[experiment.id]
                        )
                    )
                # Else keeps the same idea so the user can react rightfully
                else:
                    next_idea = last_result.idea
            # Else displays the idea so the user can react
            else:
                next_idea = last_result.idea
    else:
        # Creates a result for this user on this experiment with default expansion rate
        result = models.Result(
            user=request.user,
            experiment=experiment,
            expansion_rate=experiment.starting_expansion_rate,
        )
        result.save()

        # Picks the first idea
        next_idea, did_expand = create_next_idea(groups, result)

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
    """
    View to log in the user
    """
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
                return redirect("protocole1.homepage")
            else:  # sinon une erreur sera affichée
                error = True
    else:
        if request.user.is_authenticated:
            return redirect("protocole1.homepage")
        form = forms.ConnectionForm()
    return render(
        request,
        "users_login.html",
        {"form": form, "user": request.user, "error": error},
    )


@login_required
def log_out(request):
    """
    View to log out the user.
    """
    logout(request)
    return redirect(reverse(log_in))
