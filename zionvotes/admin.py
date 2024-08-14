from django.contrib import admin

from zionvotes import models


class RaceInline(admin.StackedInline):
    model = models.Race
    extra = 4
    fields = ['title']


class PollAdmin(admin.ModelAdmin):
    class Meta:
        model = models.Poll
        fields = [
            'title',
            'description',
            'maximum_selections',
            'open',
            'closes_at',
        ]

    list_display = [
        'title', 'open', 'closes_at', 'slug',
    ]

    inlines = [RaceInline]


admin.site.register(models.Poll, PollAdmin)


class PollOptionAdmin(admin.ModelAdmin):
    class Meta:
        model = models.Choice
        fields = [
            'name',
            'slug',
            'poll',
        ]

    list_display = [
        'name',
        'slug',
        'poll_title',
    ]

    def poll_title(self, obj):
        return f"{obj.poll.title} ({obj.poll.slug})"


admin.site.register(models.Choice, PollOptionAdmin)
