"""
TaskAPIV2 使用示例

本模块展示了如何使用 TaskAPIV2 的各种功能来查询和过滤任务
"""

from datetime import datetime, timedelta
import pytz
from dida import DidaClient

def main():
    # 初始化客户端
    # 注意：需要替换为您的实际凭证
    client = DidaClient(username="your_username", password="your_password")
    
    # 示例1：获取今天的任务
    print("\n=== 今天的任务 ===")
    today_tasks = client.tasksv2.get_tasks(mode="today")
    for task in today_tasks:
        print(f"- {task['title']} (到期时间: {task.get('dueDate', '无')})")

    # 示例2：获取高优先级任务
    print("\n=== 高优先级任务 ===")
    high_priority_tasks = client.tasksv2.get_tasks(priority=5)
    for task in high_priority_tasks:
        print(f"- {task['title']} (优先级: 高)")

    # 示例3：按项目名称筛选任务
    print("\n=== 工作项目的任务 ===")
    work_tasks = client.tasksv2.get_tasks(project_name="工作")
    for task in work_tasks:
        print(f"- {task['title']} (项目: {task['projectName']})")

    # 示例4：使用关键词搜索任务
    print("\n=== 包含'会议'的任务 ===")
    meeting_tasks = client.tasksv2.get_tasks(keyword="会议")
    for task in meeting_tasks:
        print(f"- {task['title']}")

    # 示例5：获取最近7天的任务
    print("\n=== 最近7天的任务 ===")
    recent_tasks = client.tasksv2.get_tasks(mode="recent_7_days")
    for task in recent_tasks:
        print(f"- {task['title']} (日期: {task.get('dueDate', '无')})")

    # 示例6：按标签筛选任务
    print("\n=== 带有特定标签的任务 ===")
    tagged_tasks = client.tasksv2.get_tasks(tag_names=["重要", "紧急"])
    for task in tagged_tasks:
        print(f"- {task['title']} (标签: {[tag['name'] for tag in task.get('tagDetails', [])]})")

    # 示例7：获取特定时间范围内创建的任务
    print("\n=== 最近24小时内创建的任务 ===")
    now = datetime.now(pytz.timezone('Asia/Shanghai'))
    yesterday = now - timedelta(days=1)
    recent_created_tasks = client.tasksv2.get_tasks(
        created_after=yesterday,
        created_before=now
    )
    for task in recent_created_tasks:
        print(f"- {task['title']} (创建时间: {task['createdTime']})")

    # 示例8：组合查询 - 高优先级且今天到期的工作任务
    print("\n=== 高优先级且今天到期的工作任务 ===")
    combined_tasks = client.tasksv2.get_tasks(
        mode="today",
        priority=5,
        project_name="工作"
    )
    for task in combined_tasks:
        print(f"- {task['title']} (项目: {task['projectName']}, 优先级: 高)")

if __name__ == "__main__":
    main() 