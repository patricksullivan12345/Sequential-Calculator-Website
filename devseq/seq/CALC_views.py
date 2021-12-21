from django.shortcuts import render
from .models import projects, fiber, sequentials
import numpy as np

def relationship_queries(request, pk): #Projects kwargs must match!

    projectObj = projects.objects.get(id=pk)
    fib_query = fiber.objects.filter(project_relationship=str(projectObj.id))
    seq_query = sequentials.objects.filter(fiber_relationship__in=fib_query).order_by('fiber_relationship') 
    all_seqs =  seq_query.values_list('fiber_relationship','in_seq','out_seq').order_by('fiber_relationship')

    def query_organizer():

        seq_dict={}

        for i in range(len(all_seqs)):

            uuid = str(all_seqs[i][0])

            if uuid not in seq_dict.keys():

                seq_dict[uuid] = []

        for i in range(len(all_seqs)):

            uuid = str(all_seqs[i][0])

            if uuid in seq_dict.keys():

                seq_dict[uuid].append(all_seqs[i][1])
                seq_dict[uuid].append(all_seqs[i][2])

        return seq_dict

    seq_dict = query_organizer()

    def master_dictionary(seq_dict):

        slack_list = []
        w2w_list = []
        sum_list = []
        measured_list = []

        if len(seq_dict.values()) != 0:

            for seqs in seq_dict.values():

                if len(seqs) == 2:

                    np_seqs = np.array(seqs)

                    slack = abs(np_seqs[0]-np_seqs[1])

                    slack_list.append(slack)

                    w2w_list.append(0)  

                    measured_list.append('Fiber measured length = ' + str(slack))              

                else: 

                    np_seqs = np.array(seqs)

                    np_w2w = np.delete(np_seqs,0)
                    np_w2w = np.delete(np_w2w,-1)
                    np_w2w_split = np.split(np_w2w,2)
                    w2w_list.append(0)

                    for diff in abs(np_w2w_split[0]-np_w2w_split[1]):
                    
                        w2w_list.append(diff)  
                        sum_list.append(diff)

                    np_split_slack = np.split(np_seqs, len(np_seqs)/2)

                    for i in range(len(np_split_slack)):
                        
                        slack = abs(np_split_slack[i][0]-np_split_slack[i][1])

                        slack_list.append(slack)
                        sum_list.append(slack)      

                    measured_list.append('Fiber measured length = ' + str(np.sum(sum_list)))

                    sum_list = []                                 


            return slack_list,w2w_list,measured_list

        else:

            return '','',''
            

    measured_list = master_dictionary(seq_dict)

    #print(measured_list)

    def html_calcs(measured_list,all_seqs):

        sequential_output = {}

        sequential_output['in'] = []
        sequential_output['out'] = []
        sequential_output['slack'] = []
        sequential_output['w2w'] = []

        for i in range(len(all_seqs)):

            sequential_output['in'].append(all_seqs[i][1])
            sequential_output['out'].append(all_seqs[i][2])
        
        sequential_output['slack'].append(measured_list[0])
        sequential_output['w2w'].append(measured_list[1])

        return sequential_output

    sequential_output =  html_calcs(measured_list,all_seqs)

    context =  {'projectObj': projectObj, 
                'fib_query': fib_query, 
                'calcs':sequential_output,
                'seq_query': seq_query,
                'measured_list':measured_list[2],
                }

    return render(request, 'seq/project.html', context )