import json
import os
#import pandas
#import sys

task_dir = "./task"
py_command = "python3"
py_code = "submission.py"

def load_task_file(filename):
    file_in = os.path.join(task_dir,filename)
    contents = []
    try:
        with open(file_in,'r') as f:
            contents = f.readlines()
            contents = [line.strip() for line in contents]
            return contents
    except EnvironmentError:
        print("No such file: " + filename)

def load_answer_file(filename):
    file_in = os.path.join(task_dir,filename)
    answers = dict()
    with open(file_in) as f:
        tmp = f.readlines()
        tmp = [line.strip() for line in tmp]
        for x in tmp:
            x = x.split("|")
            answers[x[0]] = x[1]
    return answers

def manhattan_dist(p,r):
    return abs(p.x - r.x) + abs(p.y - r.y) 

def check_format(i_t, j_t, result):
    is_pass = True
    result = json.loads(result)
    if j_t == 0:
        if int(result['ini_cost']) <= 0:
            is_pass = False
            #print("error 1")
    
    if int(result['best_cost']) <= 0:
        if_pass = False
        #print("error 2")
    
    if not result['locations']:
        is_pass = False
        #print("error 3")
    else:
        is_pass = all([isinstance(x, list) for x in result['locations']])
        if not is_pass:
            #print("error 4")
            return is_pass
        if i_t == 0:
            if len(result['locations']) != 1:
                is_pass = False
                #print("error 5")
        elif i_t <= 2:
            if len(result['locations']) != 2 :
                is_pass = False
                #print("error 6")         
    return is_pass

def check_locations(filename, r_list, best_cost):
    park = Park(load_task_file(filename))
    #print(r_list)
    for r in r_list:
        #print(r)
        if park.is_conflict(r):
            print("\tRestrooms overlap playgrounds")
            return False
    park.add_restrooms(r_list)
    cost = park.cost()
    #print("Current ...")
    #print(cost)
    #print("Best ...")
    #print(best_cost)
    if best_cost != cost:
        print("\tThe cost of the restroom arrangement is wrong!")
        return False
    return True


def verify_result(filename, answers, i_t, j_t, result, score):
    is_pass = True
    answers = json.loads(answers)
    best_cost = int(result['best_cost'])
    if j_t == 0:
        if int(answers["ini_cost"]) != int(result["ini_cost"]):
            is_pass = False
            print("\tThe initial cost is incorrect!")
        else:
            score = score + 5
    if int(answers["best_cost"]) < best_cost:
            is_pass = False
            print("\tThe best cost is not correct or could be improved!")
    elif int(answers["best_cost"]) == best_cost: 
        if (i_t == 0) & (j_t == 0):
            score = score + 10
        elif (i_t == 1) & (j_t == 1):
            score = score + 20 # for 1-1
        elif i_t >= 2:
            score = score + 20 # for 2/3
        else:
            score = score + 10 # for 0-0/0-1/1-0
    else:
        if not check_locations(filename, result["locations"], best_cost):
            is_pass = False
            #print("\tThe locations of the restrooms are not correct!")
        else:
            if (i_t == 1) & (j_t == 1):
                score = score + 20 # for 1-1
            elif i_t >= 2:
                score = score + 20 # for 2/3
            else:
                print("!!! Other minimal cost!!!")
                score = score + 10 # for 0-0/0-1/1-0

    return is_pass, score

class Playground:

    def __init__(self, p):
        tmp = p.split(",")
        self.x = int(tmp[0])
        self.y = int(tmp[1])
    
    def min_dist(self, r_list):
        return min([manhattan_dist(self,r) for r in r_list])
    


class Restroom:
    
    def __init__(self, r):
        tmp = r
        #print(type(tmp))
        #print(tmp)
        if type(tmp) is str:
        #if isinstance(type(tmp), str):
            tmp = tmp.split(",")
            #print(tmp)    
        self.x = int(tmp[0])
        self.y = int(tmp[1])


class Park:
    playgrounds = []
    restrooms = []
    def __init__(self, park_info):
        size_info = park_info[1].split(",")
        self.num_rows = int(size_info[0])
        self.num_cols = int(size_info[1])

        tmp = park_info[2].split("|")
        self.num_playgrounds = tmp[0]
        self.playgrounds = [Playground(p) for p in tmp[1:]]

        tmp = park_info[3].split("|")
        self.num_restrooms = tmp[0]
        if len(tmp) > 1:
            self.restrooms = [Restroom(r) for r in tmp[1:]]
    
    def is_conflict(slef, r):
        is_in = False
        #print(r)
        for p in slef.playgrounds:
            if (r[0] == p.x) & (r[1] == p.y):
                is_in = True
                break
        return is_in

    def add_restrooms(self, r_list):
        if r_list:
            self.restrooms = [Restroom(r) for r in r_list]
    
    def cost(self):
        cost = 0
        for p in self.playgrounds:
            if self.restrooms:
                cost = cost + Playground.min_dist(p, self.restrooms)
            #print(cost)
        return cost

#park_info = load_task_file("task_0_1")
#park = Park(park_info)
#print(park.cost())