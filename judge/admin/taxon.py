from django.contrib import admin
from django.forms import ModelForm, ModelMultipleChoiceField
from django.utils.translation import ugettext_lazy as _

from mptt.admin import DraggableMPTTAdmin

from judge.models import Problem, ProblemSource
from judge.widgets import HeavySelect2MultipleWidget


class ProblemGroupForm(ModelForm):
    problems = ModelMultipleChoiceField(
        label=_('Included problems'),
        queryset=Problem.objects.all(),
        required=False,
        help_text=_('These problems are included in this group of problems'),
        widget=HeavySelect2MultipleWidget(data_view='problem_select2'))


class ProblemGroupAdmin(admin.ModelAdmin):
    fields = ('name', 'full_name', 'problems')
    form = ProblemGroupForm

    def save_model(self, request, obj, form, change):
        super(ProblemGroupAdmin, self).save_model(request, obj, form, change)
        obj.problem_set = form.cleaned_data['problems']
        obj.save()

    def get_form(self, request, obj=None, **kwargs):
        self.form.base_fields['problems'].initial = [o.pk for o in obj.problem_set.all()] if obj else []
        return super(ProblemGroupAdmin, self).get_form(request, obj, **kwargs)


class ProblemTypeForm(ModelForm):
    problems = ModelMultipleChoiceField(
        label=_('Included problems'),
        queryset=Problem.objects.all(),
        required=False,
        help_text=_('These problems are included in this type of problems'),
        widget=HeavySelect2MultipleWidget(data_view='problem_select2'))


class ProblemTypeAdmin(admin.ModelAdmin):
    fields = ('name', 'full_name', 'problems')
    form = ProblemTypeForm

    def save_model(self, request, obj, form, change):
        super(ProblemTypeAdmin, self).save_model(request, obj, form, change)
        obj.problem_set = form.cleaned_data['problems']
        obj.save()

    def get_form(self, request, obj=None, **kwargs):
        self.form.base_fields['problems'].initial = [o.pk for o in obj.problem_set.all()] if obj else []
        return super(ProblemTypeAdmin, self).get_form(request, obj, **kwargs)


class ProblemSourceAdmin(DraggableMPTTAdmin):
    list_display = DraggableMPTTAdmin.list_display + ('key', 'name')
    fields = ('name', 'order', 'parent')
    list_editable = ()  # Bug in SortableModelAdmin: 500 without list_editable being set
    mptt_level_indent = 20
    sortable = 'order'

    def __init__(self, *args, **kwargs):
        super(ProblemSourceAdmin, self).__init__(*args, **kwargs)
        self.__save_model_calls = 0

    def save_model(self, request, obj, form, change):
        self.__save_model_calls += 1
        return super(ProblemSourceAdmin, self).save_model(request, obj, form, change)

    def changelist_view(self, request, extra_context=None):
        self.__save_model_calls = 0
        with ProblemSource.objects.disable_mptt_updates():
            result = super(ProblemSourceAdmin, self).changelist_view(request, extra_context)
        if self.__save_model_calls:
            with LockModel(write=(ProblemSource,)):
                ProblemSource.objects.rebuild()
        return result

