def activity_selection(activities):
    """
    活动选择问题的贪心算法实现
    
    参数:
        activities: 活动列表，每个元素为 (开始时间, 结束时间) 的元组
    
    返回:
        selected_activities: 选中的活动列表
    """
    # 步骤1: 按结束时间对活动进行排序（贪心策略的关键）
    sorted_activities = sorted(activities, key=lambda x: x[1])
    
    # 步骤2: 初始化选中的活动列表
    selected_activities = []
    
    # 步骤3: 选择第一个活动（结束时间最早的）
    if sorted_activities:
        selected_activities.append(sorted_activities[0])
        last_end_time = sorted_activities[0][1]
        
        # 步骤4: 遍历剩余活动，选择不与已选活动重叠的
        for activity in sorted_activities[1:]:
            start_time, end_time = activity
            # 如果当前活动的开始时间 >= 上一个选中活动的结束时间，则选择该活动
            if start_time >= last_end_time:
                selected_activities.append(activity)
                last_end_time = end_time
    
    return selected_activities


# 示例测试
if __name__ == "__main__":
    # 测试用例：活动列表 [(开始时间, 结束时间)]
    activities = [
        (1, 4),   # 活动1
        (3, 5),   # 活动2
        (0, 6),   # 活动3
        (5, 7),   # 活动4
        (3, 8),   # 活动5
        (5, 9),   # 活动6
        (6, 10),  # 活动7
        (8, 11),  # 活动8
        (8, 12),  # 活动9
        (2, 13),  # 活动10
        (12, 14)  # 活动11
    ]
    
    selected = activity_selection(activities)
    
    print("选中的活动:")
    for i, (start, end) in enumerate(selected, 1):
        print(f"活动{i}: 开始时间={start}, 结束时间={end}")
    print(f"总共选中 {len(selected)} 个活动")