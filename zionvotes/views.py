from random import shuffle

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from django.views.generic.detail import SingleObjectTemplateResponseMixin, SingleObjectMixin
from django.urls import reverse
from django.shortcuts import get_object_or_404, Http404, HttpResponse
# from django.utils.safestring import mark_safe
from django.utils.html import escape, mark_safe

from zionvotes.forms import RaceForm, PollForm
# from django.views

from zionvotes.models import Race, Choice, Poll, Vote
from zionvotes.count import CSSDCounter, counter_for_race


class PollVoteView(SingleObjectTemplateResponseMixin, SingleObjectMixin, FormView):
    model = Poll
    form_class = PollForm
    template_name = 'zionvotes/poll_form.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(open=True)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['poll'] = self.object
        return kwargs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['poll'] = self.object
        # random_options = list(self.object.choice_set.all())
        # shuffle(random_options)
        # ctx['random_options'] = random_options
        return ctx

    def form_valid(self, form):

        for race, field in form.poll_fields:
            Vote.objects.create(
                selection=form.cleaned_data[race.slug],
                slug=Vote.get_random_slug(),
                race=race,
                vote_source='webform',
            )

        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse('zionvotes:result', args=[self.object.slug])


class PollResultsView(DetailView):
    model = Poll
    template_name = 'zionvotes/poll_results.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        race_counters = [
            (race, counter_for_race(race))
            for race in self.object.race_set.all()
            if race.counting_method == "cssd"
        ]
        for race, counter in race_counters:
            counter.count(race.vote_set.all())
        context['race_counters'] = race_counters

        return context


def get_poll_queryset(user):
    qs = Poll.objects.all()
    if user.is_superuser:
        return qs
    elif not user.is_anonymous:
        return qs.filter(user=user)
    return Poll.objects.none()


def get_poll_or_404(user, slug):
    return get_object_or_404(get_poll_queryset(user), slug=slug)


def get_race_queryset(user):
    poll_qs = get_poll_queryset(user)
    return Race.objects.filter(poll__in=poll_qs)


def get_poll_or_404(user, slug):
    return get_object_or_404(get_poll_queryset(user), slug=slug)


class PollRacesListView(ListView):
    model = Race
    template_name = 'zionvotes/race_list.html'
    context_object_name = 'races'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(poll__slug=self.kwargs['slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['poll'] = get_poll_or_404(self.request.user, self.kwargs['slug'])
        return context


class PollListView(ListView):
    model = Poll
    template_name = 'zionvotes/poll_list.html'

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_superuser:
            return qs
        elif not self.request.user.is_anonymous:
            return qs.filter(user=self.request.user)

        return self.model.objects.none()


class PollCreateView(CreateView):
    model = Poll
    template_name = 'zionvotes/poll_create.html'
    fields = (
        'title',
        'description',
        'open',
        'closes_at',
    )

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.model(owner=self.request.user, slug=self.model.get_random_slug())
        return kwargs

    def get_success_url(self):
        return reverse('zionvotes:poll:detail', kwargs={'slug': self.object.slug})


class RaceCreateView(CreateView):
    model = Race
    template_name = 'zionvotes/race_create.html'
    form_class = RaceForm

    def dispatch(self, request, *args, **kwargs):
        self.poll = get_poll_or_404(self.request.user, self.kwargs['poll_slug'])
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.model(owner=self.request.user, poll=self.poll, slug=self.model.get_random_slug())
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['poll'] = self.poll
        return context

    def get_success_url(self):
        return reverse('zionvotes:poll:race:details', kwargs={'poll_slug': self.poll.slug, 'slug': self.object.slug})


class RaceDetailView(DetailView):
    model = Race
    template_name = 'zionvotes/race_detail.html'

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_superuser:
            return qs
        elif not self.request.user.is_anonymous:
            return qs.filter(user=self.request.user)

        return self.model.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['choices'] = self.object.choice_set.order_by('name')
        return context


class RaceUpdateView(UpdateView):
    model = Race
    template_name = 'zionvotes/race_update.html'
    form_class = RaceForm

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_superuser:
            return qs
        elif not self.request.user.is_anonymous:
            return qs.filter(user=self.request.user)

        return self.model.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['choices'] = self.object.choice_set.order_by('name')
        return context

    def form_invalid(self, form):
        return super().form_invalid(form)

    def get_success_url(self):
        return self.request.path


class ChoiceCreateView(CreateView):
    model = Choice
    template_name = 'zionvotes/_race_choice_form.html'
    fields = ['name']

    def get_race_object(self):
        return get_object_or_404(get_race_queryset(self.request.user), slug=self.kwargs['race_slug'])

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.model(
            race=self.get_race_object(),
            slug=self.model.get_random_slug(),
        )
        return kwargs

    def get_context_data(self, **kwargs):
        kwargs['create_form'] = True
        return super().get_context_data(**kwargs)

    def get_success_url(self):
        return reverse('zionvotes:poll:race:choice:update', args=(self.kwargs['poll_slug'], self.object.race.slug, self.object.slug))


class ChoiceUpdateView(UpdateView):
    model = Choice
    template_name = 'zionvotes/_race_choice_form.html'
    fields = ['name']

    def get_poll_queryset(self):
        qs = Race.objects.all()
        if self.request.user.is_superuser:
            return qs
        elif not self.request.user.is_anonymous:
            return qs.filter(user=self.request.user)

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(race__poll__in=get_poll_queryset(self.request.user))

    def get_context_data(self, **kwargs):
        if self.kwargs['poll_slug'] and self.object.race.poll.slug != self.kwargs['poll_slug']:
            # If a poll slug is provided it MUST match the poll option
            raise Http404()
        if self.kwargs['race_slug'] and self.object.race.slug != self.kwargs['race_slug']:
            raise Http404()
        kwargs['update_form'] = True
        return super().get_context_data(**kwargs)

    def get_success_url(self):
        return self.request.path


class ChoiceDeleteView(DeleteView):
    model = Choice
    # template_name = 'zionvotes/_polloption_form.html'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        self.object.delete()
        return HttpResponse(mark_safe(f"<div>Removed {escape(self.object.name)}</div>"))

    def form_invalid(self, form):
        return super().form_invalid(form)

    def get_poll_queryset(self):
        qs = Race.objects.all()
        if self.request.user.is_superuser:
            return qs
        elif not self.request.user.is_anonymous:
            return qs.filter(user=self.request.user)

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(race__poll__in=get_poll_queryset(self.request.user))

