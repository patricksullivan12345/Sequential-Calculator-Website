from django.shortcuts import render, redirect
from .models import projects, fiber, sequentials
from .forms import projectsForm, fiberForm, sequentialsForm
from django.contrib.auth.decorators import login_required

@login_required(login_url="login")
def list_projects(request):

    profile = request.user.profile
    names = projects.objects.filter(owner=profile.id)

    return render(request, 'seq/projects.html', {'names':names})

@login_required(login_url="login")
def createProject(request):

    profile = request.user.profile

    project_form = projectsForm()

    if request.method == 'POST':
        project_form = projectsForm(request.POST)
        if project_form.is_valid():
            project = project_form.save(commit=False)
            project.owner = profile
            project.save()
    
            return redirect('projects')

    proj_content = {'form':project_form}

    return render(request, "seq/project_form.html",proj_content)

@login_required(login_url="login")
def createFiber(request, pk):

    project_foriegn_key = projects.objects.get(id=pk)
    autofill = {'project_relationship':project_foriegn_key.id}

    fiber_form = fiberForm(autofill, use_required_attribute=False)

    if request.method == 'POST':
        fiber_form = fiberForm(request.POST)
        if fiber_form.is_valid():
            fiber_form.save()
            return redirect('project', pk=project_foriegn_key.id)

    fiber_content = {'fiber_form':fiber_form, 'relationship':project_foriegn_key}

    return render(request, "seq/fiber_form.html",fiber_content)

@login_required(login_url="login")
def redirectSeq(request, pk):

    fib_query =  fiber.objects.filter(project_relationship = pk)
    seq_query = sequentials.objects.select_related('fiber_relationship').filter(fiber_relationship__in=fib_query) 

    seq_content = {'fiber_query':fib_query,'seq_query':seq_query}

    return render(request, "seq/seq_redirect.html",seq_content)

@login_required(login_url="login")
def createSeq(request, pk):

    seq_query = fiber.objects.get(id=pk)

    autofill = {'fiber_relationship': seq_query,'project_relationship':seq_query.project_relationship}

    seq_form = sequentialsForm(autofill)

    if request.method == 'POST':
        seq_form = sequentialsForm(request.POST)
        if seq_form.is_valid():
            seq_form.save()
            return redirect('project', pk=seq_query.project_relationship_id)

    seq_content = {'sequentials_form':seq_form}

    return render(request, "seq/seq_form.html",seq_content)

@login_required(login_url="login")
def updateProject(request, pk):

    profile = request.user.profile

    project = profile.projects_set.get(id=pk)
    project_form = projectsForm(instance=project)

    if request.method == 'POST':
        project_form = projectsForm(request.POST, instance=project)
        if project_form.is_valid():
            project_form.save()
            return redirect('projects')

    proj_content = {'form':project_form}

    return render(request, "seq/project_form.html",proj_content)

@login_required(login_url="login")
def updateFiber(request, pk):

    fiber_select = fiber.objects.get(id=pk)

    fiber_edit_form = fiberForm(instance=fiber_select, use_required_attribute=False)

    if request.method == 'POST':
        fiber_edit_form = fiberForm(request.POST, instance=fiber_select)
        if fiber_edit_form.is_valid():
            fiber_edit_form.save()
            return redirect('project', pk=fiber_select.project_relationship_id)

    proj_content = {'form':fiber_edit_form}

    return render(request, "seq/project_form.html",proj_content)

@login_required(login_url="login")
def updateSeq(request, pk):

    seq_select = sequentials.objects.get(id=pk)
    
    seq_edit_form = sequentialsForm(instance=seq_select)

    if request.method == 'POST':
        seq_edit_form = sequentialsForm(request.POST, instance=seq_select, use_required_attribute=False)
        if seq_edit_form.is_valid():
            seq_edit_form.save()
            return redirect('project',pk=seq_select.project_relationship_id) 

    proj_content = {'sequentials_form':seq_edit_form}

    return render(request, "seq/seq_form.html",proj_content)

@login_required(login_url="login")
def deleteProject(request, pk):

    profile = request.user.profile

    project = profile.projects_set.get(id=pk)

    if request.method == 'POST':
        project.delete()
        return redirect('projects')

    proj_content = {'object':project}

    return render(request, "seq/delete_obj.html",proj_content)

@login_required(login_url="login")
def deleteFiber(request, pk):

    fiber_delete = fiber.objects.get(id=pk)

    if request.method == 'POST':
        fiber_delete.delete()
        return redirect('project', pk=fiber_delete.project_relationship_id)

    proj_content = {'object':fiber_delete}

    return render(request, "seq/delete_obj.html",proj_content)

@login_required(login_url="login")
def deleteSeq(request, pk):

    seq_delete = sequentials.objects.get(id=pk)

    if request.method == 'POST':
        seq_delete.delete()
        return redirect('project', pk=seq_delete.project_relationship_id) 

    proj_content = {'object':seq_delete}

    return render(request, "seq/delete_obj.html",proj_content)