# ...
playgrounds = [(0, 0), (2, 0), (2, 2), (3, 2)]
restroom_position = [(0, 2)]
for move in [(0, 1), (0, -1), (1, 0), (-1, 0)]:  # 上下左右移動
    new_position = [restroom_position[0] + move[0], restroom_position[1] + move[1]]
                
    if 0 <= new_position[0] < park_size[0] and 0 <= new_position[1] < park_size[1] and new_position not in playgrounds:  
        new_cost = total_cost_to_restroom(playgrounds, new_position)  # 計算新位置到廁所的成本
        print(new_position)
        # if new_cost < best_cost:
        #     best_cost = new_cost  # 更新最佳成本
        #     best_position = new_position  # 更新最佳位置
        #     improved = True  # 表示有改進
        #     restrooms.append(new_position)  # 將新位置加入廁所列表

# ...
