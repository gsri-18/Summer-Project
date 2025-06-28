from django.contrib import admin
from .models import User, Problem, TestCase, Submission
from django.contrib.auth.admin import UserAdmin

@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'difficulty', 'time_limit', 'memory_limit')
    search_fields = ('name', 'code')
    list_filter = ('difficulty',)
    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'code', 'difficulty', 'time_limit', 'memory_limit')
        }),
        ('Description Fields', {
            'fields': (
                'description',
                'input_format',
                'output_format',
                'constraints',
                'sample_input',
                'sample_output'
            )
        }),
    )

# The rest:
admin.site.register(User, UserAdmin)
admin.site.register(TestCase)
admin.site.register(Submission)


from .models import Contest, ContestSubmission
admin.site.register(Contest)
admin.site.register(ContestSubmission)
