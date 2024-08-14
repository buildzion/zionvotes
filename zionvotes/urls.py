
from django.urls import path, re_path, include

from zionvotes import views


choice_patterns = [
    re_path(r'new$', views.ChoiceCreateView.as_view(), name='create'),
    re_path(r'(?P<slug>ch-[\w]{12})/delete$', views.ChoiceDeleteView.as_view(), name='delete'),
    re_path(r'(?P<slug>ch-[\w]{12})$', views.ChoiceUpdateView.as_view(), name='update'),
]

race_patterns = [
    path('new', views.RaceCreateView.as_view(), name='create'),
    re_path(r'(?P<slug>r-[\w]{12})/detail$', views.RaceDetailView.as_view(), name='details'),
    re_path(r'(?P<slug>r-[\w]{12})/update$', views.RaceUpdateView.as_view(), name='update'),
    re_path(r'(?P<race_slug>r-[\w]{12})/', include((choice_patterns, 'choice'))),
]

poll_patterns = [
    path('new', views.PollCreateView.as_view(), name='create'),
    re_path(r'(?P<slug>p-[\w]{8})/$', views.PollRacesListView.as_view(), name='detail'),
    re_path(r'(?P<poll_slug>p-[\w]{8})/', include((race_patterns, 'race'))),
]


zv_patterns = [
    path('', views.PollListView.as_view(), name='index'),
    re_path(r'(?P<slug>p-[\w]{8})$', views.PollVoteView.as_view(), name='vote'),
    re_path(r'(?P<slug>p-[\w]{8})/result$', views.PollResultsView.as_view(), name='result'),
    path('polls/', include((poll_patterns, 'poll'))),
]


urlpatterns = [
    path('', include((zv_patterns, 'zionvotes'))),
]
