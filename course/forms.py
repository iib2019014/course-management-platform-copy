from django import forms

from .models import (
    Feedback,
    RATING,
    REMARK,

    AssignmentSubmission,
)


class AssignmentSubmissionForm(forms.Form) :
    answer_file = forms.FileField(required=True)

class PracticalSubmissionForm(forms.Form) :
    file = forms.FileField(required=True)

class FeedbackForm(forms.ModelForm) :
    how_would_you_rate_the_course = forms.IntegerField(widget=forms.RadioSelect(choices=RATING))
    # course_content_was = forms.CharField(widget=forms.RadioSelect(choices=REMARK))
    # explanations_by_instructor_were = forms.CharField(widget=forms.RadioSelect(choices=REMARK))
    # availability_of_extra_help_when_needed_was = forms.CharField(widget=forms.RadioSelect(choices=REMARK))
    # grading_techniques_were = forms.CharField(widget=forms.RadioSelect(choices=REMARK))
    # the_amount_of_effort_you_put_into_this_course_was = forms.CharField(widget=forms.RadioSelect(choices=REMARK))
    class Meta :
        model = Feedback
        fields = (
            'how_would_you_rate_the_course',
            # 'course_content_was',
            # 'explanations_by_instructor_were',
            # 'availability_of_extra_help_when_needed_was',
            # 'grading_techniques_were',
            # 'the_amount_of_effort_you_put_into_this_course_was',
            'review'
        )