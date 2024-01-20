from django.contrib import admin

# Register your models here.
from .models import MusicLesson, Question, Student, StudentLesson, PianoClass



class QuestionAdmin(admin.ModelAdmin):
    # Your existing ModelAdmin configuration goes here

    actions = ['clone_selected_objects']

    def clone_selected_objects(self, request, queryset):
        for obj in queryset:
            obj.pk = None  # Set the primary key to None to create a new object
            obj.save()

    clone_selected_objects.short_description = "Clone selected objects"

admin.site.register(MusicLesson)
admin.site.register(Question,QuestionAdmin)
admin.site.register(Student)
admin.site.register(StudentLesson)
admin.site.register(PianoClass)
