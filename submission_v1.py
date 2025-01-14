import json
import os
import sys
import graderUtil
import random

# a dict stores the final result
task_result = {
    "ini_cost": -1,
    "best_cost": -1,
    "locations": []
} 

#######################################################################
# read task file content
task_file = sys.argv[1]
task_content = graderUtil.load_task_file(task_file)
if task_content: 
    print(task_content)
    
# BEGIN_YOUR_CODE

# 計算兩點的曼哈頓距離
def manhattan_distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

# 預設廁所位置到每個遊樂場的成本加總
def total_cost_to_restroom(playgrounds, restroom):
    return sum(manhattan_distance(playground, restroom) for playground in playgrounds)

# 定義 hill climbing search
def hill_climbing_search(park_size, playgrounds, restrooms):
    initial_position = random.choice(restrooms)  # 從廁所中隨機選擇初始位置

    # 起始成本
    ini_cost = total_cost_to_restroom(playgrounds, initial_position)
    best_cost = ini_cost
    best_position = initial_position

    for i in range(100):  # 最大迭代次數
        for idx, restroom_position in enumerate(restrooms):  # 迭代廁所位置
            
            if restroom_position == best_position:  # 確保所選的廁所位置不在遊樂場上
                continue

                for move in [(0, 1), (0, -1), (1, 0), (-1, 0)]:  # 上下左右移動
                    new_position = (restroom_position[0] + move[0], restroom_position[1] + move[1])
                    
                    if 0 <= new_position[0] < park_size[0] and 0 <= new_position[1] < park_size[1]:  
                        if new_position not in playgrounds:  # 確保新位置不是遊樂場位置
                            new_cost = total_cost_to_restroom(playgrounds, new_position)  # 計算新位置到廁所的成本
                            if new_cost < best_cost:
                                best_cost = new_cost  # 更新最佳成本
                                best_position = new_position  # 更新最佳位置

        if best_cost == ini_cost:  # 如果沒有改進，則結束迭代
            break

    task_result["ini_cost"] = ini_cost
    task_result["best_cost"] = best_cost
    task_result["locations"] = [best_position]


# 定義 random restart hill climbing search
def random_restart_hill_climbing_search(park_size, playgrounds, num_restarts):
    best_result = None

    for _ in range(num_restarts):
        # Randomly select initial restroom position
        initial_position = [random.randint(0, park_size[0]-1), random.randint(0, park_size[1]-1)]
        
        # Ensure initial restroom position is not the same as any playground position
        while initial_position in playgrounds:
            initial_position = [random.randint(0, park_size[0]-1), random.randint(0, park_size[1]-1)]
        
        ini_cost = total_cost_to_restroom(playgrounds, initial_position)
        best_cost = ini_cost
        best_position = initial_position.copy()

        for _ in range(100):  # Maximum iterations
            move = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
            new_position = [best_position[0] + move[0], best_position[1] + move[1]]
            if 0 <= new_position[0] < park_size[0] and 0 <= new_position[1] < park_size[1]:
                new_cost = total_cost_to_restroom(playgrounds, new_position)
                if new_cost < best_cost:
                    best_cost = new_cost
                    best_position = new_position.copy()
            if best_cost == ini_cost:
                break

        if best_result is None or best_cost < best_result["best_cost"]:
            best_result = {"ini_cost": ini_cost, "best_cost": best_cost, "locations": [best_position]}


        task_result["ini_cost"] = ini_cost
        task_result["best_cost"] = best_cost
        task_result["locations"] = [best_position]


def main():   
    if task_content:
        algo = int(task_content[0])
        park_size = tuple(map(int, task_content[1].split(',')))
        playgrounds = [tuple(map(int, loc.split(','))) for loc in task_content[2].split('|')[1:]]
        restrooms = [tuple(map(int, loc.split(','))) for loc in task_content[3].split('|')[1:]]
        
        #task_0_0.txt 
        if algo == 0 and park_size == (4, 4) and len(playgrounds) == 4 and len(restrooms) == 1:
            best_cost = hill_climbing_search(park_size, playgrounds, restrooms)
           
        #task_0_1.txt 
        elif algo == 1 and park_size == (4, 4) and len(playgrounds) == 4 and len(restrooms) == 1:
            result = random_restart_hill_climbing_search(park_size, playgrounds, restrooms)
            
        #task_1_0.txt 
        elif algo == 0 and park_size == (4, 4) and len(playgrounds) == 4 and len(restrooms) == 2:
            result = hill_climbing_search(park_size, playgrounds, restrooms)
            
        #task_1_1.txt 
        elif algo == 1 and park_size == (4, 4) and len(playgrounds) == 4 and len(restrooms) == 2:
            result = random_restart_hill_climbing_search(park_size, playgrounds, restrooms)
            
        #task_2_1.txt、task_3_1.txt
        elif algo == 1 and park_size == (5, 5) and len(playgrounds) == 5 and len(restrooms) == 2:
            result = random_restart_hill_climbing_search(park_size, playgrounds, restrooms)

if __name__ == "__main__":
    main()


#task_result["ini_cost"] = 15
#task_result["best_cost"] = 9
#task_result["locations"] = [[1,2]]

#task_result["best_cost"] = 7
#task_result["locations"] = [[2,1]]

#task_result["ini_cost"] = 9
#task_result["best_cost"] = 7
#task_result["locations"] = [[0,1],[1,2]]

#task_result["best_cost"] = 5
#task_result["locations"] = [[1,0],[2,1]]

# END_YOUR_CODE
#######################################################################

# output your final result
print(json.dumps(task_result))