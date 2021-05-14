import os
os.environ['PROJ_LIB'] = r'C:\Users\jeetj\Miniconda3\pkgs\proj4-5.2.0-ha925a31_1\Library\share'
import random as rand
import itertools
from copy import deepcopy


from mapcolor import colormap
import time


full = []
backtracks = 0
class State:
    def __init__(self,name,domain,status="not visited"):
        self.name=name
        self.neighbours=None
        self.color_name=None
        self.status=status
        self.domain=domain
        self.singleton=False
    
    def set_neighbours(self,neighbours):
        self.neighbours=neighbours
    def get_neighbours(self):
        return self.neighbours
    def set_color(self,color_name):
        self.color_name=color_name
    def set_parent(self,parent):
        self.parent=parent
    def set_domain(self,domain):
        self.domain=domain
    def get_domain(self):
        return self.domain
    def is_singleton(self):
        if self.singleton:
            return self.singleton
        return False
    
        
def available_states(state_objects):
    not_visited_states=[]
    for state in state_objects:
        if state.status=="not visited":
            not_visited_states.append(state)
    return not_visited_states
def available_colors(state,domain):
    #print(domain)
    available_domain=domain.copy()
    for neighbour in state.neighbours:
        color = neighbour.color_name
        #print("name",neighbour.name)
        #print("color",color)
        
        if color!=None and (color in available_domain) :
            available_domain.remove(color)
    return available_domain
def change_domain(state,color):
    for neighbour in state.neighbour:
        if (neighbour.status=="not visited") and (color in neighbour.domain):
            (neighbour.domain).remove(color)
            
def single_domain_states(state_objects):
    #single_domain=[]
    for state in state_objects:
        if state.singleton==False and len(state.get_domain())==1:
            #print(len(state.domain))
            #print(state.domain)
            #print("hey",state.name)
            state.singleton=True
            color = state.domain[0]
            print("single_state_domain",state.domain)
            return state,color
    return None,None
def singleton_propagtion(state_objects):
    print("Insingleton Propogation ............++++++++++++")
    singleton_states={}
    while True:
        
        state,color = single_domain_states(state_objects)
        #print("state123",state)
        if state==None:
            return singleton_states,"sucess"
        else:
            print("singleton_state",state.name)
            print("domain",state.domain)
            singleton_states[state]=color
            for neighbour in state.neighbours:
                if neighbour.status=="not visited" and color in neighbour.domain:
                    print("neighbour : "+neighbour.name)
                    print("domain_neighbour : ",neighbour.domain)
                    if len(neighbour.domain)==1:
                        print("name",neighbour.name)
                        print(neighbour.domain)
                        return singleton_states,"unsucessful"
                    (neighbour.domain).remove(color)
                    print("after domain_neighbour : ",neighbour.domain)
                        
        
        
    
                    
    

def color_arranging(domain,state_domain):
    #print("in color_arranging")
    dom=deepcopy(domain)
    dom2=deepcopy(dom)
    state_dom=deepcopy(state_domain)
    #print("length",(state_dom))
    #print(dom)
    for color in dom:
        count=0
        #print("color : "+color)
        for state_color in state_dom:
            
            if color!=state_color:
                #print("state_color",state_color)
                count+=1
        #print("count",count)
        if count==len(state_dom):
            #print("in count")
            dom2.remove(color)
            #print("dom",dom2)
    #print("dom",dom2)
    return dom2
                
    
def update_colors(state,color):
    print("in update_colors .......... ")
    #print("length",len(state.neighbours))
    #print("color_name",color)
    #print("in updated colors")capitalize
    #print("state.name : "+state.name)
    updated_states=[]
    for neighbour in state.neighbours:
        #print(neighbour.name,neighbour.status)
        #print(neighbour.domain)
        if neighbour.status=="not visited" and color in neighbour.domain:
            #print("name",neighbour.name)
            (neighbour.domain).remove(color)
            #print("after removing  "+color,neighbour.name,neighbour.domain)
            updated_states.append(neighbour)
    #print("length",len(updated_states))
    return updated_states
def reset(state,domain,color,updated_states):
    #print("color)
    print("in reset method .............")
    pos = domain.index(color)
    #print("pos",pos)
    #print("color_name",color)
    #print("length of updated_states for : "+state.name,len(updated_states))
    for neighbour in state.neighbours:
        if neighbour.status=="not visited" and (neighbour in updated_states):
            (neighbour.domain).insert(pos,color)
            dom = color_arranging(domain,neighbour.domain)
            neighbour.domain=deepcopy(dom)
            #print("color after inserting",neighbour.name,neighbour.domain)
def singleton_reset(singleton_states,domain,colour):
    #print(singleton_states)
    print("in singleton_reset method.............")
    for state,color in singleton_states.items():
        #print("single : "+state.name)
        #print("color",singleton_states[state])
        #print("domain123",state.domain)
        #print("color_name",color)
        pos = domain.index(color)
        #print("pos",pos)
        for neighbour in state.neighbours:
            #print("neighbour_name : "+neighbour.name)
            #print("is_singleton",neighbour.is_singleton())
            if neighbour.status=="not visited" and (neighbour.is_singleton()):
                #print("neighbour_name2 : "+neighbour.name)
                (neighbour.domain).insert(pos,color)
                dom = color_arranging(domain,neighbour.domain)
                neighbour.domain=dom
        state.singleton=False
       
            
        

            
            
            
            
        
            

                           
            

"""def csp(state_objects,domain):
    un_assigned_states=available_states(state_objects)
    #print(len(un_assigned_states))
    if len(un_assigned_states)==40:
        return state_objects
    state = rand.choice(un_assigned_states)
    #state=un_assigned_states[0]
    print("state : "+state.name)
    for color in domain:
        if color_validation(state,color):
            state.status="visited"
            state.color_name=color
            result=csp(state_objects,domain)
            if result!="un sucessful":
                return result
    state.status="not visited"
    state.color_name=None
    return "un sucessful"
    """
def csp(state_objects,domain,states_and_colors):
        global backtracks 
        #print("domain:",domain)
            
        
        if len(states_and_colors)==len(state_objects):
            return states_and_colors
        
        un_assigned_states=available_states(state_objects)
        #print("remaining_states",len(un_assigned_states))
        #state=rand.choice(un_assigned_states)
        
        state=un_assigned_states[0]
        print(state.name)
        available_domain=deepcopy(state.domain)
        #print("available_domain",available_domain)
        
        
        #state=un_assigned_states[0]
        iter1 = 0
        for color in available_domain:
            iter1+=1 
            state.status="visited"
            state.color_name=color
            states_and_colors[state.name]=color
            #full.append(states_and_colors)
            #if iter1%100==0:
            #colormap(states_and_colors)

            updated_states=update_colors(state,color)
            print("total updated states",len(updated_states))
            singleton_states,status=singleton_propagtion(state_objects)
            print(len(singleton_states),status)
            
            if status!="unsucessful":
                result=csp(state_objects,domain,states_and_colors)
            else:
                result=status
            if result!="unsucessful":
                return result
            del states_and_colors[state.name]
            state.color_name=None
            state.status="not visited"
            #print("color name",color)
            '''print(state.name)
            state.status="visited"
            state.color_name=color
            print('color_name',color)
            states_and_colors[state.name]=color
            updated_states = update_colors(state,color)
            print(len(updated_states))
            print(states_and_colors)
            singleton_states,status=singleton_propagtion(state_objects)
            #for single in singleton_states:
                #print("Single_name",single.name)
            print("status",status,"length",len(singleton_states))
            #print(states_and_colors)
            #print("singleton_states:",singleton_states)
            if status!="unsucessful":
                print("about to recurse")
                result=csp(state_objects,domain,states_and_colors)
                print("result",result)
            else:
                print("return  ",status)
                result=status
            #print("color",state.color_name)

            #print(state.name,state.status)
            
            print(result,state.name)
            print("updated states by : "+state.name,len(updated_states))
            if result!="unsucessful":
                return result
            del states_and_colors[state.name]
            reset(state,domain,state.color_name,updated_states)
            #singleton_reset(singleton_states,domain,state.color_name)
            
            state.color_name=None
            state.status="not visited"
            #print(states_and_colors)'''
            
        #print("no colors")
        
        #print(state.name,state.status)
        #state.color_name=None
        backtracks+=1
        return "unsucessful"
        
            
    
                
            
            
            
            


def to_objects(states,domain):
    state_objs = []
    dom=deepcopy(domain)
    for state in states:
        state_obj=State(state,dom)
        state_objs.append(state_obj)
        dom=deepcopy(dom)
    return state_objs
        
        
def main():
    states=['wa','nt','q','nsw','v','sa']
    restriction_graph={
        'wa':['nt','sa'],
        'nt':['wa','q','sa'],
        'sa':['wa','q','nsw','nt','v'],
        'q':['nt','sa','nsw'],
        'nsw':['q','v','sa'],
        'v':['sa','nsw']
        }
    # states= ['New Hampshire', 'Oklahoma', 'Tennessee', 'Illinois', 'New Mexico', 'Kentucky', 'West Virginia', 'Maryland', 'Maine', 'Wisconsin', 'Missouri', 'Minnesota', 'Montana', 'Massachusetts', 'South Carolina', 'North Dakota', 'Pennsylvania', 'Arizona', 'South Dakota', 'Ohio', 'Oregon', 'Alabama', 'Indiana', 'Rhode Island', 'Virginia', 'Idaho', 'Nevada', 'Nebraska', 'New York', 'Utah', 'Michigan', 'Kansas', 'Florida', 'Connecticut', 'Iowa', 'Wyoming', 'Louisiana', 'California', 'Vermont', 'Texas', 'Georgia', 'New Jersey', 'North Carolina', 'Washington', 'Delaware', 'Colorado', 'Mississippi', 'Arkansas']
    # restriction_graph ={
    #         'Alabama':['Florida', 'Georgia', 'Mississippi', 'Tennessee'],
    #         'Arizona':['California', 'Colorado', 'Nevada', 'New Mexico', 'Utah'],
    #         'Arkansas' :['Louisiana', 'Mississippi', 'Missouri', 'Oklahoma', 'Tennessee', 'Texas'],
    #         'California':['Arizona', 'Nevada', 'Oregon'],
    #         'Colorado':['Arizona', 'Kansas', 'Nebraska', 'New Mexico', 'Oklahoma', 'Utah', 'Wyoming'],
    #         'Connecticut':['Massachusetts', 'New York', 'Rhode Island'],
    #         'Delaware':['Maryland', 'New Jersey', 'Pennsylvania'],
    #         'Florida':['Alabama', 'Georgia'],
    #         'Georgia':['Alabama', 'Florida', 'North Carolina', 'South Carolina', 'Tennessee'],
    #         'Idaho':['Montana', 'Nevada', 'Oregon', 'Utah', 'Washington', 'Wyoming'],
    #         'Illinois':['Indiana','Iowa', 'Michigan', 'Kentucky', 'Missouri', 'Wisconsin'],
    #         'Indiana':['Illinois', 'Kentucky', 'Michigan', 'Ohio'],
    #         'Iowa': ['Illinois', 'Minnesota', 'Missouri', 'Nebraska', 'South Dakota', 'Wisconsin'],
    #         'Kansas' :['Colorado', 'Missouri', 'Nebraska', 'Oklahoma'],
    #         'Kentucky':['Illinois', 'Indiana', 'Missouri', 'Ohio', 'Tennessee', 'Virginia', 'West Virginia'],
    #         'Louisiana':['Arkansas', 'Mississippi', 'Texas'],
    #         'Maine':["New Hampshire"],
    #         "Maryland":['Delaware','Pennsylvania','Virginia', 'West Virginia'],
    #         'Massachusetts':['Connecticut', 'New Hampshire', 'New York', 'Rhode Island', 'Vermont'],
    #         'Michigan':['Illinois', 'Indiana', 'Minnesota', 'Ohio', 'Wisconsin'],
    #         'Minnesota':['Iowa', 'Michigan', 'North Dakota', 'South Dakota', 'Wisconsin'],
    #         'Mississippi':['Alabama', 'Arkansas', 'Louisiana', 'Tennessee'],
    #         'Missouri':['Arkansas', 'Illinois', 'Iowa', 'Kansas', 'Kentucky', 'Nebraska', 'Oklahoma', 'Tennessee'],
    #         'Montana':['Idaho', 'North Dakota', 'South Dakota', 'Wyoming'],
    #         'Nebraska' :['Colorado', 'Iowa', 'Kansas', 'Missouri', 'South Dakota', 'Wyoming'],
    #         'Nevada':['Arizona', 'California', 'Idaho', 'Oregon', 'Utah'],
    #         'New Hampshire': ['Maine', 'Massachusetts', 'Vermont'],
    #         'New Jersey':["Delaware", "New York", "Pennsylvania"],
    #         'New Mexico':['Arizona', 'Colorado', 'Oklahoma', 'Texas', 'Utah'],
    #         'New York':['Connecticut', 'Massachusetts', 'New Jersey', 'Pennsylvania', 'Rhode Island', 'Vermont'],
    #         'North Carolina':['Georgia', 'South Carolina', 'Tennessee', 'Virginia'],
    #         'North Dakota':['Minnesota', 'Montana', 'South Dakota'],
    #         'Ohio':['Indiana', 'Kentucky', 'Michigan', 'Pennsylvania', 'West Virginia'],
    #         'Oklahoma' :['Arkansas', 'Colorado', 'Kansas', 'Missouri', 'New Mexico', 'Texas'],
    #         'Oregon':["California", 'Idaho', 'Nevada', "Washington"],
    #         'Pennsylvania':['Delaware', 'Maryland', 'New Jersey', 'New York', 'Ohio', 'West Virginia'],
    #         'Rhode Island':['Connecticut', 'Massachusetts', 'New York'],
    #         'South Carolina':['Georgia', 'North Carolina'],
    #         'South Dakota':['Iowa', 'Minnesota', 'Montana', 'Nebraska', 'North Dakota', 'Wyoming'],
    #         'Tennessee':['Alabama', 'Arkansas', 'Georgia', 'Kentucky', 'Mississippi', 'Missouri', 'North Carolina', 'Virginia'],
    #         'Texas':['Arkansas', 'Louisiana', 'New Mexico', 'Oklahoma'],
    #         'Utah':['Arizona', 'Colorado', 'Idaho', 'Nevada', 'New Mexico', 'Wyoming'],
    #         'Vermont':['Massachusetts', 'New Hampshire', 'New York'],
    #         'Virginia':['Kentucky', 'Maryland', 'North Carolina', 'Tennessee', 'West Virginia'],
    #         'Washington':['Idaho', 'Oregon'],
    #         'West Virginia':['Kentucky', 'Maryland', 'Ohio', 'Pennsylvania', 'Virginia'],
    #         'Wisconsin':['Illinois', 'Iowa', 'Michigan', 'Minnesota'],
    #         'Wyoming':['Colorado', 'Idaho', 'Montana', 'Nebraska', 'South Dakota', 'Utah'],
    #         'Hawaii':[],
    #         'Alaska':[]
    #         }
    
    
    
    '''states=['AB', 'BC', 'MB', 'NB', 'NL', 'NS', 'NT', 'NU', 'ON', 'PE',
                 'QC', 'SK', 'YT']
    restriction_graph={
            'AB':['BC','NT','SK'],
            'BC':['NT','YT','AB'],
            'MB':['NU','ON','SK'],
            'NB':['NS','QC'],
            'NL':['QC'],
            'NT':['NU','SK','BC','AB','YT'],
            'NU':['MB','NT'],
            'ON':['QC','MB'],
            'YT':['NT','BC'],
            'SK':['AB','NT','MB'],
            'QC':['ON','NL','NB'],
            'NS':['NB'],
            'PE':[]
            }'''
    

    domain=["blue","green","red","orange"]
    state_objects = to_objects(states,domain)
    for state in state_objects:
        print(state.domain)
    #state_objects.append(State('A',["red"]))
    #state_objects.append(State('g',["red"]))
    #print("states",(single_domain_states(state_objects))[0].name)
    
    
    states_and_colors={}
    for state in state_objects:
        key = state.name
        values=restriction_graph[key]
        neighbours=[]
        for value in values:
            obj=[obj_form for obj_form in state_objects if obj_form.name==value ]
            neighbours.append(obj[0])
            
        state.set_neighbours(neighbours)
    #print(color_arranging(domain,["orange","red"]))
    
        
    
    st=csp(state_objects,domain,states_and_colors)
    #print(state_objects[33].name,state_objects[33].domain)
    #print(singleton_propagtion(state_objects,"red"))
    print(st)
    #for i in range(0,len(full),6000):
    #    print(full[i])
    #    colormap(full[i])


    #time.sleep(10)
    """for state in state_objects:
        print(state.name," " ,state.domain)"""


    #print(color_validation(stat,"blue"))
    '''for state in state_objects:
        print(state.domain)'''
    """
    for key in restriction_graph.keys():
        states = (restriction_graph[key])
        #color=st[key]
        for state in states:
            if st[state]==color:
                print(key,state,color)
            else:
                print("false")
    """

start_time = time.time()
main()
end_time = time.time()

print("Time of execution = " + str(end_time- start_time) + " seconds")
print("Number of Backtracks= " + str(backtracks))
        
'''st1 = {'Oregon': 'blue', 'Delaware': 'blue', 'Arkansas': 'blue', 'Michigan': 'blue', 'Kentucky': 'blue',
 'North Dakota': 'blue', 'Wyoming': 'blue', 'Texas': 'green', 'Alabama': 'blue', 'Kansas': 'blue', 
 'Missouri': 'green', 'Arizona': 'blue', 'Vermont': 'blue', 'South Carolina': 'blue', 'Rhode Island': 'blue',
 'Washington': 'green', 'South Dakota': 'green', 'Mississippi': 'green', 'Idaho': 'red', 'California': 'red', 
 'Montana': 'orange', 'Maryland': 'green', 'Maine': 'blue', 'New York': 'green', 'Utah': 'orange', 'Indiana': 'red', 
 'North Carolina': 'green', 'Louisiana': 'red', 'West Virginia': 'red', 'Nebraska': 'red', 'Tennessee': 'red', 
 'Minnesota': 'red', 'Iowa': 'blue', 'New Mexico': 'red', 'Massachusetts': 'red', 
 'Oklahoma': 'orange', 'Ohio': 'green', 'Connecticut': 'orange', 'Florida': 'green', 'Wisconsin': 'green',
 'Illinois': 'orange', 'Colorado': 'green', 'Pennsylvania': 'orange', 'New Jersey': 'red', 'Nevada': 'green', 
 'Georgia': 'orange', 'New Hampshire': 'green', 'Virginia': 'orange'}'''
k = {'Kansas': 'blue', 'New Hampshire': 'blue', 'Idaho': 'blue', 'Louisiana': 'blue', 'New Jersey': 'blue',
 'Arkansas': 'green', 'Kentucky': 'blue', 'Maine': 'green', 'Minnesota': 'blue',
 'Missouri': 'red', 'West Virginia': 'green', 'North Carolina': 'blue', 'Massachusetts': 'green',
 'Michigan': 'green', 'Indiana': 'red', 'Illinois': 'orange', 'Virginia': 'red', 'Oklahoma': 'orange',
 'Montana': 'orange', 'North Dakota': 'green', 'Texas': 'red', 'Colorado': 'red', 'South Carolina': 'green',
 'Maryland': 'blue', 'California': 'blue', 'New York': 'orange', 'Florida': 'blue', 'Vermont': 'red',
 'Utah': 'orange', 'Georgia': 'red', 'Oregon': 'green', 'Wisconsin': 'red', 'Rhode Island': 'blue',
 'Nebraska': 'orange', 'New Mexico': 'blue', 'Mississippi': 'red', 'Alabama': 'green', 'Nevada': 'red', 
 'Tennessee': 'orange', 'Iowa': 'green', 'South Dakota': 'red', 'Ohio': 'orange', 'Pennsylvania': 'red',
 'Washington': 'red', 'Wyoming': 'green', 'Arizona': 'green', 'Delaware': 'green', 'Connecticut': 'red'}
k={'Ohio': 'blue', 'Hawaii': 'blue', 'Vermont': 'blue', 'Maine': 'blue', 'Tennessee': 'blue', 
'Oklahoma': 'blue', 'Colorado': 'green', 'Alabama': 'green', 'Oregon': 'blue',
 'Minnesota': 'blue', 'New Mexico': 'red', 'Mississippi': 'red', 'Kansas': 'red',
 'New Hampshire': 'green', 'Louisiana': 'blue', 'Rhode Island': 'blue', 'Montana': 'blue',
 'Wisconsin': 'green', 'Michigan': 'red', 'Arkansas': 'green', 'Maryland': 'blue',
 'Missouri': 'orange', 'Massachusetts': 'red', 'North Dakota': 'green', 'Nevada': 'green',
 'South Dakota': 'orange', 'Illinois': 'blue', 'Washington': 'green', 'Virginia': 'green',
 'Indiana': 'green', 'Alaska': 'blue', 'Connecticut': 'green', 'North Carolina': 'red',
 'New York': 'orange', 'New Jersey': 'blue', 'Iowa': 'red', 'Kentucky': 'red',
 'South Carolina': 'blue', 'West Virginia': 'orange', 'Idaho': 'orange',
 'Florida': 'blue', 'Delaware': 'green', 'Nebraska': 'blue', 'Arizona': 'orange', 
'Wyoming': 'red', 'California': 'red', 'Utah': 'blue', 'Texas': 'orange', 'Pennsylvania': 'red',
 'Georgia': 'orange'}
print(list(k.keys()))








    
    

    
    

    
    
        
    
