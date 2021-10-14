from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse
from .models import projects, fiber, sequentials, tags
from .forms import projectsForm, fiberForm, sequentialsForm
from collections import defaultdict
import numpy as np

def list_projects(request):

    names = projects.objects.all()

    return render(request, 'seq/projects.html', {'names':names})

def relationship_queries(request, pk): #Projects kwargs must match!

    projectObj = projects.objects.get(id=pk)
    fib_query = fiber.objects.filter(project_relationship=str(projectObj.id))
    seq_query = sequentials.objects.filter(fiber_relationship__in=fib_query).order_by('fiber_relationship') 
    all_seqs =  seq_query.values_list('fiber_relationship','in_seq','out_seq').order_by('fiber_relationship')

    slack_list = []

    def slack_function(slack_list,all_seqs):

        for seq in all_seqs:

            slack_list.append(str(abs(seq[1]-seq[2])))
        
        return slack_list

    slack =  slack_function(slack_list,all_seqs)

    w2w_list = []

    def w2w_function(w2w_list,all_seqs):
        
        for i in range(len(all_seqs)):

            if i == 0:

                w2w_list.append(0)

            elif str(all_seqs[i-1][0]) != str(all_seqs[i][0]):

                w2w_list.append(0)

            elif str(all_seqs[i-1][0]) == str(all_seqs[i][0]):

                w2w_list.append(abs(all_seqs[i-1][2] - all_seqs[i][1]))
            
        return w2w_list

    w2w = w2w_function(w2w_list,all_seqs)

    measured_list = []

    index_list = []

    np_list = []

    def ml_function(measured_list,all_seqs,index_list,np_list):

        for i in range(len(all_seqs)):

            if i == 0:

                index_list.append([all_seqs[i][1],all_seqs[i][2]])

            elif  str(all_seqs[i-1][0]) != str(all_seqs[i][0]):

                index_list.append([all_seqs[i][1],all_seqs[i][2]])

            elif  str(all_seqs[i-1][0]) == str(all_seqs[i][0]):

                index_list.append([all_seqs[i][1],all_seqs[i][2],124532234232])

        for i in range(len(index_list)):

            if i == 0:

                pass

            elif len(index_list[i]) == 3:

                index_list[i-1].append(index_list[i][0])
                index_list[i-1].append(index_list[i][1])

        for remove_list in index_list:

            if len(remove_list) != 3:

                np_list.append(np.array(remove_list))

        for i in range(len(np_list)):

            sorted_distance = np.sort(np_list[i])

            measured_length = sorted_distance[len(sorted_distance)-1] - sorted_distance[0]

            measured_list.append("Fiber " + str(i+1) + " measured length = " + str(measured_length))

        return measured_list

    measured_list = ml_function(measured_list,all_seqs,index_list,np_list)

    return render(request, 'seq/project.html', {'projectObj': projectObj, 
                                                'fib_query': fib_query, 
                                                'seq_query':seq_query,
                                                'slack':slack,
                                                'w2w':w2w,
                                                'measured_list':measured_list,
                                               })

def createProject(request):

    project_form = projectsForm()

    if request.method == 'POST':
        project_form = projectsForm(request.POST)
        if project_form.is_valid():
            project_form.save()
            return redirect('projects')

    proj_content = {'form':project_form}

    return render(request, "seq/project_form.html",proj_content)

def createFiber(request, pk):

    project_foriegn_key = projects.objects.get(id=pk)
    autofill = {'project_relationship':project_foriegn_key.id}

    fiber_form = fiberForm(autofill)

    if request.method == 'POST':
        fiber_form = fiberForm(request.POST)
        if fiber_form.is_valid():
            fiber_form.save()
            return redirect('projects')

    fiber_content = {'fiber_form':fiber_form, 'relationship':project_foriegn_key}

    return render(request, "seq/fiber_form.html",fiber_content)

def redirectSeq(request, pk):

    fib_query =  fiber.objects.filter(project_relationship = pk)
    seq_query = sequentials.objects.select_related('fiber_relationship').filter(fiber_relationship__in=fib_query) 

    seq_content = {'fiber_query':fib_query,'seq_query':seq_query}

    return render(request, "seq/seq_redirect.html",seq_content)

def createSeq(request, pk):

    seq_query = fiber.objects.get(id=pk)

    autofill = {'fiber_relationship': seq_query}

    seq_form = sequentialsForm(autofill)

    if request.method == 'POST':
        seq_form = sequentialsForm(request.POST)
        if seq_form.is_valid():
            seq_form.save()
            return redirect('projects')  

    seq_content = {'sequentials_form':seq_form}

    return render(request, "seq/seq_form.html",seq_content)

def updateProject(request, pk):

    project = projects.objects.get(id=pk)
    project_form = projectsForm(instance=project)

    if request.method == 'POST':
        project_form = projectsForm(request.POST, instance=project)
        if project_form.is_valid():
            project_form.save()
            return redirect('projects')

    proj_content = {'form':project_form}

    return render(request, "seq/project_form.html",proj_content)

def updateFiber(request, pk):

    fiber_select = fiber.objects.get(id=pk)

    fiber_edit_form = fiberForm(instance=fiber_select)

    if request.method == 'POST':
        fiber_edit_form = fiberForm(request.POST, instance=fiber_select)
        if fiber_edit_form.is_valid():
            fiber_edit_form.save()
            return redirect('projects')

    proj_content = {'form':fiber_edit_form}

    return render(request, "seq/project_form.html",proj_content)

def updateSeq(request, pk):

    seq_select = sequentials.objects.get(id=pk)

    seq_edit_form = sequentialsForm(instance=seq_select)

    if request.method == 'POST':
        seq_edit_form = sequentialsForm(request.POST, instance=seq_select)
        if seq_edit_form.is_valid():
            seq_edit_form.save()
            return redirect('projects')  

    proj_content = {'sequentials_form':seq_edit_form}

    return render(request, "seq/seq_form.html",proj_content)

def deleteProject(request, pk):

    project = projects.objects.get(id=pk)

    if request.method == 'POST':
        project.delete()
        return redirect('projects')

    proj_content = {'object':project}

    return render(request, "seq/delete_obj.html",proj_content)

def deleteFiber(request, pk):

    fiber_delete = fiber.objects.get(id=pk)

    if request.method == 'POST':
        fiber_delete.delete()
        return redirect('projects')

    proj_content = {'object':fiber_delete}

    return render(request, "seq/delete_obj.html",proj_content)

def deleteSeq(request, pk):

    seq_delete = sequentials.objects.get(id=pk)

    if request.method == 'POST':
        seq_delete.delete()
        return redirect('projects')

    proj_content = {'object':seq_delete}

    return render(request, "seq/delete_obj.html",proj_content)
