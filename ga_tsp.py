
import math
import random
import statistics
import matplotlib.pyplot as plt
import streamlit as st

def make_towns(N):
    towns=[]
    for n in range(0,N):
        x=random.random()*1000.0
        y=random.random()*1000.0
        towns.append( (x,y) )

    return towns

def get_towns_distances(towns):
    town_distances={}

    for i in range(0,len(towns)):
        for j in range(0,len(towns)):
            xdiff=towns[i][0]-towns[j][0]
            ydiff=towns[i][1]-towns[j][1]
            this_dist=math.sqrt( (xdiff**2) + (ydiff**2) )
            town_distances[ (i,j) ] =this_dist

    return town_distances

def make_one(N):
    s=[]
    r=list(range(1,N))
    for i in range(0,N-1):
        i=random.randint(0,len(r)-1)
        v=r.pop(i)
        s.append(v)

    return s

def initialization(N,num_pop):
    this_pop=[]
    for i in range(0,num_pop):
        this_pop.append(make_one(N))

    return this_pop

def get_fitness(s,towns_distances):
    fit=0

    this_dist=towns_distances[ (0,s[0]) ]
    fit+=this_dist

    for k in range(1,len(s)):
        this_dist=towns_distances[ (s[k-1],s[k]) ]
        fit+=this_dist
        
    return fit

def get_pop_fitness(population,towns_distances):
    pop_fitness=[]
    for s in population:
        pop_fitness.append(get_fitness(s,towns_distances))
    return pop_fitness

def selection(population,pop_fitness):
    
    i1=random.randint(0,len(population)-1)
    i2=random.randint(0,len(population)-1)
    while i2==i1:
        i2=random.randint(0,len(population)-1)    
    if pop_fitness[i1]<=pop_fitness[i2]:
        i=i1
    else:
        i=i2

    i3=random.randint(0,len(population)-1)
    while i3==i:
        i3=random.randint(0,len(population)-1) 
    i4=random.randint(0,len(population)-1)
    while i4==i or i4==i3:
        i4=random.randint(0,len(population)-1) 
    if pop_fitness[i3]<=pop_fitness[i4]:
        j=i3
    else:
        j=i4

    return population[i],population[j]

def one_ordered_crossover(sA,sB,ip1,ip2):
    new_chars=sB[ip1:ip2+1]
    if ip2+1<len(sA):
        for i in range(ip2+1,len(sA)):
            if not sA[i] in new_chars:
                new_chars.append(sA[i])

    ilimit=min(ip2+1,len(sA))
    for i in range(0,ilimit):
        if not sA[i] in new_chars:
            new_chars.append(sA[i])
        
    second_part=new_chars[:len(sA)-ip1]
    first_part=new_chars[len(sA)-ip1:]
    
    sN=first_part+second_part

    return sN

def crossover(s1,s2):
    ip1=random.randint(0,len(s1)-1)
    ip2=ip1
    while ip2==ip1:
        ip2=random.randint(0,len(s1)-1)
    if ip2<ip1:
        ip_temp=ip2
        ip2=ip1
        ip1=ip_temp
    
    new_s1=one_ordered_crossover(s1,s2,ip1,ip2)
    new_s2=one_ordered_crossover(s2,s1,ip1,ip2)

    return new_s1,new_s2

def get_next_generation(pop,pop_fitness,num_not_elite):
    next_gen=[]
    while len(next_gen)<num_not_elite:
        s1,s2=selection(pop,pop_fitness)
        new_s1,new_s2=crossover(s1,s2)
        next_gen.append(new_s1)
        next_gen.append(new_s2)

    return next_gen

def mutation(population,mutate_prob):
    for i in range(0,len(population)):
        p=random.random()
        if p<=mutate_prob:
            ip1=random.randint(0,len(population[i])-1)
            ip2=ip1
            while ip2==ip1:
                ip2=random.randint(0,len(population[i])-1)
            
            ip_temp=population[i][ip1]
            population[i][ip1]=population[i][ip2]
            population[i][ip2]=ip_temp

    return population

def get_min_path(pop_fitness,population):
    this_min_fitness=min(pop_fitness)
    this_min_path=[]
    for j in range(0,len(pop_fitness) ):
        if pop_fitness[j]==this_min_fitness:
            this_min_path=population[j]
            break    

    return this_min_fitness,this_min_path

def add_elite(population,pop_fitness,num_elite,next_generation):
    tlist=[]
    for i in range(0,len(population)):
        tlist.append( (pop_fitness[i],population[i]) )
    tlist.sort()

    new_pop=[t[1] for t in tlist[:num_elite] ]
    new_pop.extend(next_generation)
    
    return new_pop

def one_run(N,num_pop,num_iter,elitism,mutate_prob,towns,towns_distances):

    population=initialization(N,num_pop)
    pop_fitness=get_pop_fitness(population,towns_distances)

    min_fitness=min(pop_fitness)
    min_fitness,min_path=get_min_path(pop_fitness,population)
    this_mean_fitness=statistics.mean(pop_fitness)
    this_max_fitness=max(pop_fitness)
        
    num_elite=int(elitism*float(num_pop))
    num_not_elite=num_pop-num_elite

    count=0
    step_fitness_list=[(min_fitness,this_mean_fitness,this_max_fitness,min_fitness)]
    final_path=[]
    for i in range(0,num_iter):
        count+=1
        next_generation=get_next_generation(population,pop_fitness,num_not_elite)
        next_generation=mutation(next_generation,mutate_prob)
        next_generation=add_elite(population,pop_fitness,num_elite,next_generation)
        
        pop_fitness=get_pop_fitness(next_generation,towns_distances)
        this_min_fitness,this_min_path=get_min_path(pop_fitness,next_generation)
        this_mean_fitness=statistics.mean(pop_fitness)
        this_max_fitness=max(pop_fitness)
        if this_min_fitness<min_fitness:
            min_fitness=this_min_fitness
            min_path=this_min_path
            
        step_fitness_list.append((this_min_fitness,this_mean_fitness,this_max_fitness,min_fitness) )
        population=next_generation[:]

        if min_fitness==0:
            break

    min_path.insert(0,0)    #start the path at zero
        
    return count,min_fitness,step_fitness_list,min_path

random.seed()    
N=5
num_pop=100
num_iter=500
elitism=0.1
mutate_prob=0.05
    
st.session_state['count']=0
st.session_state['min_fitness']=0
st.session_state['step_fitness_list']=[]
st.session_state['final_path']=[]

if 'towns' not in st.session_state:
    st.session_state['towns']=[]

st.title('GA TSP')
N=st.number_input('N Number of towns', min_value=5, max_value=500, value=N)    
num_pop=st.number_input('Size of population', min_value=5, max_value=10000, value=num_pop)
num_iter=st.number_input('Maximum number of iterations', min_value=2, max_value=100000, value=num_iter)
elitism=st.number_input('Elitism', min_value=0.0, max_value=1.0, value=elitism,step=0.01)
mutate_prob=st.number_input('Mutation probability', min_value=0.0, max_value=1.0, value=mutate_prob,step=0.01)

col1, col2 = st.columns([0.2,0.8])

with col1:
    if st.button('Make towns'):
        st.session_state['towns']=make_towns(N)
        st.session_state['towns_distances']=get_towns_distances(st.session_state['towns'])

with col2:
    if st.session_state['towns']!=[] and N==len(st.session_state['towns']):
        if st.button('Run'):
            st.session_state['count'],st.session_state['min_fitness'],st.session_state['step_fitness_list'],st.session_state['final_path']=one_run(N,num_pop,num_iter,elitism,mutate_prob,st.session_state['towns'],st.session_state['towns_distances'])

col1a,col2a=st.columns(2)
with col1a:
    if st.session_state['towns']!=[]:
        x0=[st.session_state['towns'][0][0]]
        y0=[st.session_state['towns'][0][1]]
        
        x=[t[0] for t in st.session_state['towns'] ]
        y=[t[1] for t in st.session_state['towns'] ]
        fig = plt.figure()
        ax = fig.add_subplot(1,1,1)
        ax.scatter(x,y)
        ax.scatter(x0,y0,color='tab:red')
        
        st.pyplot(fig)
with col2a:
    if st.session_state['final_path']!=[]:
        px=[st.session_state['towns'][p][0] for p in st.session_state['final_path'] ]
        py=[st.session_state['towns'][p][1] for p in st.session_state['final_path'] ]

        x=[t[0] for t in st.session_state['towns'] ]
        y=[t[1] for t in st.session_state['towns'] ]
        fig = plt.figure()
        ax = fig.add_subplot(1,1,1)
        ax.scatter(x,y)
        ax.plot(px,py)
        st.pyplot(fig)  

if st.session_state['final_path']!=[]:
    st.text('count='+str(st.session_state['count']))
    st.text('minimum fitness='+str(st.session_state['min_fitness']))

    x=list(range(0,len(st.session_state['step_fitness_list']) ) )
    y_this_min=[f[0] for f in st.session_state['step_fitness_list']]
    y_this_mean=[f[1] for f in st.session_state['step_fitness_list']]
    y_this_max=[f[2] for f in st.session_state['step_fitness_list']]
    y_min=[f[3] for f in st.session_state['step_fitness_list']]
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax.plot(x, y_this_min)
    ax.plot(x, y_this_mean)
    ax.plot(x, y_this_max)
    ax.plot(x, y_min)
    ax.set_ylim(ymin=0)
    ax.legend(['min','avg','max','min so far'] ) 
    st.pyplot(fig)

