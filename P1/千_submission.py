import json
import os
import sys
import graderUtil

# a dict stores the final result
task_result = {
    "ini_cost": -1,
    "best_cost": -1,
    "locations": []
} 

#######################################################################
# read task file content
task_file = sys.argv[1]  #從命令列中獲取輸入的參數，並將第一個參數賦值給變數 task_file
task_content = graderUtil.load_task_file(task_file)
if task_content:
    print(task_content)
# BEGIN_YOUR_CODEs
def distance(point1, point2):
    return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])
def calculate_cost1(restroom):
        cost=sum(distance(restroom, playground) for playground in playgrounds)
        return cost
def calculate_cost2(playgrounds, restrooms):
        total_cost = 0
        for playground in playgrounds:
            min_distance = float('inf')
            for restroom in restrooms:
                new_distance = distance(playground, restroom)
                if new_distance < min_distance:
                    min_distance = new_distance
            total_cost += min_distance
        return total_cost

algorithm_type = int(task_content[0])
restroom_no=int(task_content[3].split('|')[0])
park_size= tuple(map(int,task_content[1].split(',')))
playgrounds = [tuple(map(int, loc.split(','))) for loc in task_content[2].split('|')[1:]]


# _0_0
if algorithm_type==0 and restroom_no==1:
    
# 計算playgrounds到restroom的cost
    restroom = tuple(map(int, task_content[3].split('|')[1].split(',')))
    
    current_location = restroom
    initial_cost = calculate_cost1(restroom)
    best_cost = calculate_cost1(restroom)
    best_location = restroom
    new_cost=0

    while True:
        improved=False

        for dx,dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            
            new_location=(best_location[0]+dx,best_location[1]+dy)
            #確認新位置合法性
            if new_location[0]>=0 and new_location[1]>=0 and new_location not in playgrounds:
                new_cost=calculate_cost1(new_location)
                if best_cost>new_cost:
                    best_cost=new_cost
                    best_location=new_location
                    improved=True
        if improved==False:
            break        
        current_location=best_location
    task_result["ini_cost"] = initial_cost
    task_result["best_cost"] = best_cost
    task_result["locations"] = [best_location]

# _1_0
if algorithm_type==0 and restroom_no==2:
    restrooms = [tuple(map(int, loc.split(','))) for loc in task_content[3].split('|')[1:]]
   
    current_location = restrooms[:]
    initial_cost = calculate_cost2(playgrounds, restrooms)
    best_cost = calculate_cost2(playgrounds, restrooms)
    best_location = restrooms[:]
    new_cost=0

    while True:
        improved = False
        for i in range(len(restrooms)):
            for dx, dy in [(0, -1),(1, 0), (0, 1), (-1, 0)]:
                new_location = (restrooms[i][0] + dx, restrooms[i][1] + dy)
                if new_location not in playgrounds:
                    new_restrooms = restrooms[:i] + [new_location] + restrooms[i+1:]
                    new_cost = calculate_cost2(playgrounds, new_restrooms)
                    if new_cost < best_cost:
                        best_cost = new_cost
                        best_location = new_restrooms[:]
                        improved = True
        if improved==False:
            break        
        current_location=best_location[:]
    task_result["ini_cost"] = initial_cost
    task_result["best_cost"] = best_cost
    task_result["locations"] = [list(loc) for loc in best_location]

# random restart hill climbing
if algorithm_type==1:
    
    # 把公園所有座標列出
    park_locations=[]
    best_location =[]
    for i in range(park_size[0]):
        for j in range(park_size[1]):
            park_locations.append((i,j))
    
    # 廁所能在的位置:限制廁所只能生成在不是playground的座標上
    restroom_locations=list(loc for loc in park_locations if loc not in playgrounds)
    #print('restroom_locations',restroom_locations)
    # 先將best cost設成無窮大
    best_cost = float('inf')
    # restart 次數
    
    # 判斷題目有沒有給restart次數
    if len(task_content) == 4:
         # 如果沒給restart次數,自己設成15次
         restarts=15
    else: # 有給就用題目的
         restarts = int(task_content[4])
    import random
    for _ in range(restarts):
        # 隨機生成廁所的位置
        random_restroom=random.sample(restroom_locations,restroom_no)
        #print('random_restroom',random_restroom)
        # 目前廁所位置=隨機生成的廁所位置
        initial_location = random_restroom[:]
        candidate_location= random_restroom[:]
        candidate_cost=calculate_cost2(playgrounds,initial_location)
        
        for i in range(len(random_restroom)):
            directions=[(1, 0), (-1, 0), (0, 1), (0, -1)]
            for direction in directions:
                 
            #for dx,dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                new_restroom=(random_restroom[i][0]+direction[0],random_restroom[i][1]+direction[1])
                #print('new_restroom',new_restroom)
                # 判斷廁所的上下左右的位置不能跟playground相同,也不能超出park範圍,
                # 也不能跟另一個廁所同位置
                if new_restroom[0]>=0 and new_restroom[0]<park_size[0] and new_restroom[1]>=0 and new_restroom[1]<park_size[1]and new_restroom not in playgrounds and new_restroom not in candidate_location:
                    new_restroom_neighbor = candidate_location[:i] + [new_restroom] + candidate_location[i+1:]
                    new_cost = calculate_cost2(playgrounds, new_restroom_neighbor)
                    
                    if new_cost<candidate_cost:
                        candidate_cost=new_cost
                        #print('candidate_cost',candidate_cost)
                        candidate_location=new_restroom_neighbor
                        #print('candidate_location',candidate_location)
        if candidate_cost<best_cost:
            best_cost=candidate_cost
            #print('best_cost',best_cost)
            best_location=candidate_location
            #print('best_location',best_location)
    task_result["best_cost"] = best_cost
    task_result["locations"] = best_location


# END_YOUR_CODE
#######################################################################

# output your final result
print(json.dumps(task_result))

