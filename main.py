from client import *
import numpy as np
from math import *
import random 
import pickle
id = "KM3cGnpd5T86XOe18c8SKilDBqirKnR3156si4V5Zb4SOFO33V"
crossOverProb = 0.3
#mutateProb = np.array([0.3,0.3,0.3,0.3,0.3,0.3,0.3,0.3,0.3,0.3,0.3])
mutateProb = 0.3
populationSize = 100
generations = []
population = []
kl = './day'
nu = 857
kl+=str(nu)
filename = kl+"/output.txt"
infile = open(filename,'rb')
individuals = json.load(infile)
infile.close()
filename = kl+"/valErrors.txt"
infile = open(filename,'rb')
valErrors = json.load(infile)
infile.close()
#print(valErrors)
filename = kl+"/trainErrors.txt"
infile = open(filename,'rb')
trainErrors = json.load(infile)
infile.close()
filename = kl+"/generations.txt"
infile = open(filename,'rb')
generation = json.load(infile)
infile.close()

vis = [[0]*100]*100
vis = np.array(vis)

afterCrossOver = []
afterMutation = []

class individual:

    def __init__(self,*args):
        if len(args)==1:
            self.arr = args[0]
            afterCrossOver.append(self.arr.tolist()) 
            self.mutate()
            afterMutation.append(self.arr.tolist())
            out = get_errors(id,self.arr.tolist())
            self.valError = out[1]
            self.trainError = out[0]    
            self.score = 10*self.valError + self.trainError #+ self.trainError #+self.trainError
        else:
            self.arr = args[0]
            afterCrossOver.append(self.arr.tolist())
            afterMutation.append(self.arr.tolist())
            self.valError = args[1]
            self.trainError = args[2]
            self.score = 10*self.valError + self.trainError #+ self.trainError  #+self.trainError
#-self.arr[i]/10,-self.arr[i]/50,-self.arr[i]/100,self.arr[i]/10,self.arr[i]/50,self.arr[i]/100])[0]
    def mutate(self):
        for i in range(0,11):
            pro = random.uniform(0,1)
            if pro<=mutateProb:
                self.arr[i] += (random.choices([-self.arr[i]/100,self.arr[i]/100])[0])
                if self.arr[i]>10:
                    self.arr[i]=10
                elif self.arr[i]<-10:
                    self.arr[i]=-10

def crossOver(a,b):
    arr = [] 
    pro = a.score/(a.score+b.score)
    for i in range(0,11):
        arr.append(((1.5+pro)*b.arr[i]+(2.5-pro)*a.arr[i])/4)
        # k = random.uniform(0,1)
        # if k<=pro:
        #     arr.append(b.arr[i])
        # else:
        #     arr.append(a.arr[i])
    c = individual(np.array(arr))
    return c

def initiate():
    global populationSize
    global population
    global generations
    for i in range(0,100):
        y = individual(np.array(individuals[i]),valErrors[i],trainErrors[i])
        population.append(y)
    # for i in range(0,100):
    #     x = individual(np.array(individuals[i]))
    #     population.append(x)
    population = sorted(population, key = lambda l:l.score)

def createGen():
    newPopulation = []
    global populationSize
    global population
    global generations

    for j in range(0,90):
        newPopulation.append(population[j])
    # child = crossOver(population[0],population[1])
    # newPopulation.append(child)
    # vis[0][1]=1
    # vis[1][0]=1
    i=0
    while i < 10:
        x = random.randint(0,99)
        y = random.randint(0,99)
        if vis[x][y]==0 or vis[x][y]==1:
            child = crossOver(population[x],population[y])
            newPopulation.append(child)
            i+=1
            vis[x][y]=1
            vis[y][x]=1
    for j in range(0,100): 
        for k in range(0,100):
            vis[j][k]=0
    population = newPopulation
    population = sorted(population, key = lambda l:l.score)
    generations.append(population)

def main():
    global populationSize
    global population
    global generations
    global afterCrossOver
    global afterMutation
    global mutateProb
    for mn in range(0,20):
        st = "./day"
        num = 858+mn
        st+=str(num)
        afterMutation = []
        afterMutation = []
        initiate()
        createGen()
        generation = []
        l = []
        for i in range(0,100):
            l.append(population[i].arr.tolist())
        generation.append(l)
        # for i in range(0,5):
        #     createGen()
        #     l = []
        #     for j in range(0,100):
        #         l.append(population[i].arr.tolist())
        #     generation.append(l)
        individuals = []
        valErrors = []
        trainErrors = []
        for i in range(0,100):
            individuals.append(population[i].arr.tolist())
            valErrors.append(population[i].valError)
            trainErrors.append(population[i].trainError)
        with open(st+'/output.txt','w') as write_file:
            json.dump(individuals, write_file)
        with open(st+'/generations.txt','w') as write_file:
            json.dump(generation, write_file)
        with open(st+'/valErrors.txt','w') as write_file:
            json.dump(valErrors, write_file)
        with open(st+'/trainErrors.txt','w') as write_file:
            json.dump(trainErrors, write_file)
        with open(st+'/afterMutation.txt','w') as write_file:
            json.dump(afterMutation, write_file)
        with open(st+'/afterCrossOver.txt','w') as write_file:
            json.dump(afterCrossOver, write_file)
        mutateProb += 0.05

if __name__ == '__main__': 
    main()
