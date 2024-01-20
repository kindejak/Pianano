from django.shortcuts import render
from .forms import StudentForm

from django.views import View

# Create your views here.


# create a student view
class createStudentForm(View):
    context ={}

    def get(self, request):
        form = StudentForm()
        self.context['form'] = form
        #self.context['detail'] = StudentForm.objects.all()
        return render(request, 'create_student.html', self.context)

    def post(self, request):
        form = StudentForm(request.POST or None)
        if form.is_valid():
            form.save()
        self.context['form'] = form
        return render(request, 'create_student.html', self.context)
