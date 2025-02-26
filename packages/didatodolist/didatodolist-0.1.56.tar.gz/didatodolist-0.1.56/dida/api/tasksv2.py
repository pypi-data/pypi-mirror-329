"""
任务API版本2，支持灵活的任务查询功能
"""

from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import pytz
from .base import BaseAPI

class TaskAPIV2(BaseAPI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._completed_columns = set()  # 存储已完成状态的栏目ID
        self._column_info = {}  # 存储栏目信息

    def _update_column_info(self, projects: List[Dict[str, Any]]) -> None:
        """
        更新栏目信息
        
        Args:
            projects: 项目列表数据
        """
        for project in projects:
            if 'columns' in project:
                for column in project['columns']:
                    self._column_info[column['id']] = column
                    # 根据栏目名称或其他特征判断是否为已完成栏目
                    if '已完成' in column.get('name', ''):
                        self._completed_columns.add(column['id'])

    def get_tasks(self, mode: str = "all", keyword: Optional[str] = None, priority: Optional[int] = None,
                  project_name: Optional[str] = None, tag_names: Optional[List[str]] = None,
                  created_after: Optional[datetime] = None, created_before: Optional[datetime] = None,
                  completed_after: Optional[datetime] = None, completed_before: Optional[datetime] = None,
                  completed: Optional[bool] = None) -> List[Dict[str, Any]]:
        """
        获取任务，支持多种模式和筛选条件
        
        Args:
            mode: 查询模式，支持 "all", "today", "yesterday", "recent_7_days"
            keyword: 关键词筛选（支持模糊搜索，会搜索标题、内容和子任务）
            priority: 优先级筛选 (0-最低, 1-低, 3-中, 5-高)
            project_name: 项目名称筛选
            tag_names: 标签名称列表筛选
            created_after: 创建时间开始筛选
            created_before: 创建时间结束筛选
            completed_after: 完成时间开始筛选
            completed_before: 完成时间结束筛选
            completed: 是否已完成，True表示已完成，False表示未完成，None表示全部
            
        Returns:
            List[Dict[str, Any]]: 符合条件的任务列表
        """
        tasks = self.get_all_tasks()

        # 如果是查询今天的任务，默认只显示未完成的任务
        if mode == "today" and completed is None:
            completed = False

        def match_keyword(task: Dict[str, Any], kw: str) -> bool:
            """递归检查任务及其子任务是否匹配关键词"""
            # 检查当前任务
            if (kw.lower() in task.get('title', '').lower() or 
                kw.lower() in task.get('content', '').lower()):
                return True
            
            # 递归检查子任务
            for child in task.get('children', []):
                if match_keyword(child, kw):
                    return True
            return False

        def filter_tasks(task_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
            """递归过滤任务列表"""
            filtered_tasks = []
            for task in task_list:
                # 首先处理子任务
                children = []
                if task.get('children'):
                    children = filter_tasks(task['children'])

                # 检查当前任务是否匹配所有条件
                task_matches = True

                # 检查完成状态（这个条件最优先，因为它会影响其他时间相关的判断）
                if completed is not None and self._is_task_completed(task) != completed:
                    task_matches = False

                # 只有在任务未完成的情况下，才进行时间相关的判断
                if task_matches:
                    if mode == "today" and not self._is_today(task):
                        task_matches = False
                    elif mode == "yesterday" and not self._is_yesterday(task):
                        task_matches = False
                    elif mode == "recent_7_days" and not self._is_recent_7_days(task):
                        task_matches = False

                # 其他过滤条件
                if task_matches:
                    if keyword and not match_keyword(task, keyword):
                        task_matches = False
                    if priority is not None and task.get('priority') != priority:
                        task_matches = False
                    if project_name and project_name.lower() not in task.get('projectName', '').lower():
                        task_matches = False
                    if tag_names and not any(tag in task.get('tags', []) for tag in tag_names):
                        task_matches = False
                    if created_after and self._parse_date(task.get('createdTime')) < created_after:
                        task_matches = False
                    if created_before and self._parse_date(task.get('createdTime')) > created_before:
                        task_matches = False
                    if completed_after and self._parse_date(task.get('completedTime')) < completed_after:
                        task_matches = False
                    if completed_before and self._parse_date(task.get('completedTime')) > completed_before:
                        task_matches = False

                # 如果当前任务匹配或者有匹配的子任务，则添加到结果中
                if task_matches or children:
                    task_copy = task.copy()
                    task_copy['children'] = children
                    filtered_tasks.append(task_copy)

            return filtered_tasks

        return filter_tasks(tasks)

    def _parse_date(self, date_str: Optional[str]) -> Optional[datetime]:
        """
        统一解析日期字符串为datetime对象
        
        Args:
            date_str: 日期字符串
            
        Returns:
            Optional[datetime]: 解析后的datetime对象，解析失败返回None
        """
        if not date_str:
            return None
            
        try:
            # 尝试ISO格式
            return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.000+0000")
        except ValueError:
            try:
                # 尝试标准格式
                return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                print(f"Warning: Unrecognized date format: {date_str}")
                return None

    def _is_today(self, task: Dict[str, Any]) -> bool:
        """
        判断任务是否是今天的任务
        规则：
        1. 如果任务已完成，则不是今天的任务
        2. 任务的时间范围（startDate到dueDate）与今天有重叠
        3. 对于全天任务，结束时间应该是当天的23:59:59
        4. 时间判断时要考虑时区
        """
        # 如果任务已完成，不应该出现在今天的任务中
        if self._is_task_completed(task):
            return False

        local_tz = pytz.timezone('Asia/Shanghai')
        now = datetime.now(local_tz)
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = today_start + timedelta(days=1)

        # 获取任务的开始和结束时间
        start_date = self._parse_date(task.get('startDate'))
        due_date = self._parse_date(task.get('dueDate'))

        # 如果既没有开始时间也没有结束时间，则不是今天的任务
        if not start_date and not due_date:
            return False

        # 确保时区一致
        if start_date and start_date.tzinfo is None:
            start_date = local_tz.localize(start_date)
        elif start_date:
            start_date = start_date.astimezone(local_tz)

        if due_date and due_date.tzinfo is None:
            due_date = local_tz.localize(due_date)
        elif due_date:
            due_date = due_date.astimezone(local_tz)

        # 对于全天任务，调整结束时间到当天的23:59:59
        if task.get('isAllDay') and due_date:
            due_date = due_date.replace(hour=23, minute=59, second=59)

        # 检查时间范围是否重叠
        if start_date and due_date:
            return start_date < today_end and due_date >= today_start
        elif start_date:
            return start_date < today_end
        else:  # 只有 due_date
            return due_date >= today_start

    def _is_yesterday(self, task: Dict[str, Any]) -> bool:
        """
        判断任务是否是昨天的任务
        规则：
        1. 如果任务已完成，则不是昨天的任务
        2. 任务的时间范围（startDate到dueDate）与昨天有重叠
        3. 对于全天任务，结束时间应该是当天的23:59:59
        4. 时间判断时要考虑时区
        """
        # 如果任务已完成，不应该出现在昨天的任务中
        if self._is_task_completed(task):
            return False

        local_tz = pytz.timezone('Asia/Shanghai')
        now = datetime.now(local_tz)
        yesterday_start = (now - timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        yesterday_end = yesterday_start + timedelta(days=1)

        # 获取任务的开始和结束时间
        start_date = self._parse_date(task.get('startDate'))
        due_date = self._parse_date(task.get('dueDate'))

        # 如果既没有开始时间也没有结束时间，则不是昨天的任务
        if not start_date and not due_date:
            return False

        # 确保时区一致
        if start_date and start_date.tzinfo is None:
            start_date = local_tz.localize(start_date)
        elif start_date:
            start_date = start_date.astimezone(local_tz)

        if due_date and due_date.tzinfo is None:
            due_date = local_tz.localize(due_date)
        elif due_date:
            due_date = due_date.astimezone(local_tz)

        # 对于全天任务，调整结束时间到当天的23:59:59
        if task.get('isAllDay') and due_date:
            due_date = due_date.replace(hour=23, minute=59, second=59)

        # 检查时间范围是否重叠
        if start_date and due_date:
            return start_date < yesterday_end and due_date >= yesterday_start
        elif start_date:
            return start_date < yesterday_end
        else:  # 只有 due_date
            return due_date >= yesterday_start

    def _is_recent_7_days(self, task: Dict[str, Any]) -> bool:
        """
        判断任务是否在最近7天内
        规则：
        1. 如果任务已完成，则不包含在内
        2. 任务的时间范围（startDate到dueDate）与未来7天有重叠
        3. 对于全天任务，结束时间应该是当天的23:59:59
        4. 时间判断时要考虑时区
        """
        # 如果任务已完成，不应该出现在最近7天的任务中
        if self._is_task_completed(task):
            return False

        local_tz = pytz.timezone('Asia/Shanghai')
        now = datetime.now(local_tz)
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        week_end = today_start + timedelta(days=7)

        # 获取任务的开始和结束时间
        start_date = self._parse_date(task.get('startDate'))
        due_date = self._parse_date(task.get('dueDate'))

        # 如果既没有开始时间也没有结束时间，则不在最近7天内
        if not start_date and not due_date:
            return False

        # 确保时区一致
        if start_date and start_date.tzinfo is None:
            start_date = local_tz.localize(start_date)
        elif start_date:
            start_date = start_date.astimezone(local_tz)

        if due_date and due_date.tzinfo is None:
            due_date = local_tz.localize(due_date)
        elif due_date:
            due_date = due_date.astimezone(local_tz)

        # 对于全天任务，调整结束时间到当天的23:59:59
        if task.get('isAllDay') and due_date:
            due_date = due_date.replace(hour=23, minute=59, second=59)

        # 检查时间范围是否重叠
        if start_date and due_date:
            return start_date < week_end and due_date >= today_start
        elif start_date:
            return start_date < week_end
        else:  # 只有 due_date
            return due_date >= today_start

    def _merge_project_info(self, task_data: Dict[str, Any], projects: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        合并项目信息到任务数据中
        
        Args:
            task_data: 任务数据
            projects: 项目列表
            
        Returns:
            Dict[str, Any]: 合并后的任务数据
        """
        if not task_data.get('projectId'):
            return task_data
            
        for project in projects:
            if project['id'] == task_data['projectId']:
                task_data['projectName'] = project['name']
                task_data['projectKind'] = project['kind']
                break
                
        return task_data

    def _merge_tag_info(self, task_data: Dict[str, Any], tags: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        合并标签信息到任务数据中
        
        Args:
            task_data: 任务数据
            tags: 标签列表
            
        Returns:
            Dict[str, Any]: 合并后的任务数据
        """
        if not task_data.get('tags'):
            return task_data
            
        tag_details = []
        for tag_name in task_data['tags']:
            for tag in tags:
                if tag['name'] == tag_name:
                    tag_details.append({
                        'name': tag['name'],
                        'label': tag['label']
                    })
                    break
        
        task_data['tagDetails'] = tag_details
        return task_data

    def _simplify_task_data(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        简化任务数据，只保留必要字段
        
        Args:
            task_data: 原始任务数据
            
        Returns:
            Dict[str, Any]: 简化后的任务数据
        """
        def format_date(date_str: Optional[str], is_due_date: bool = False) -> Optional[str]:
            if not date_str:
                return None
            try:
                local_tz = pytz.timezone('Asia/Shanghai')
                if 'T' in date_str:
                    base_time = date_str.split('.')[0]
                    if date_str.endswith('Z'):
                        dt = datetime.strptime(base_time, "%Y-%m-%dT%H:%M:%S")
                        dt = pytz.UTC.localize(dt)
                    elif '+0000' in date_str:
                        dt = datetime.strptime(base_time, "%Y-%m-%dT%H:%M:%S")
                        dt = pytz.UTC.localize(dt)
                    else:
                        try:
                            dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                        except ValueError:
                            dt = datetime.strptime(base_time, "%Y-%m-%dT%H:%M:%S")
                            dt = local_tz.localize(dt)
                else:
                    dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
                    dt = local_tz.localize(dt)
                
                local_dt = dt.astimezone(local_tz)
                if is_due_date and local_dt.hour == 0 and local_dt.minute == 0 and local_dt.second == 0:
                    local_dt = local_dt + timedelta(days=1)
                
                return local_dt.strftime("%Y-%m-%d %H:%M:%S")
            except Exception:
                return date_str

        children = []
        if task_data.get('items'):
            for item in task_data['items']:
                child_task = self._simplify_task_data(item)
                children.append(child_task)

        essential_fields = {
            'id': task_data.get('id'),
            'title': task_data.get('title'),
            'content': task_data.get('content'),
            'priority': task_data.get('priority'),
            'status': task_data.get('status'),
            'startDate': format_date(task_data.get('startDate'), is_due_date=False),
            'dueDate': format_date(task_data.get('dueDate'), is_due_date=True),
            'projectName': task_data.get('projectName'),
            'projectId': task_data.get('projectId'),
            'projectKind': task_data.get('projectKind'),
            'columnId': task_data.get('columnId'),
            'tagDetails': task_data.get('tagDetails', []),
            'kind': task_data.get('kind'),
            'isAllDay': task_data.get('isAllDay'),
            'reminder': task_data.get('reminder'),
            'repeatFlag': task_data.get('repeatFlag'),
            'items': children,
            'progress': task_data.get('progress', 0),
            'modifiedTime': format_date(task_data.get('modifiedTime')),
            'createdTime': format_date(task_data.get('createdTime')),
            'completedTime': format_date(task_data.get('completedTime')),
            'completedUserId': task_data.get('completedUserId'),
            'isCompleted': task_data.get('isCompleted', False),
            'creator': task_data.get('creator'),
            'timeZone': 'Asia/Shanghai',
            'isFloating': task_data.get('isFloating', False),
            'reminders': task_data.get('reminders', []),
            'exDate': task_data.get('exDate', []),
            'etag': task_data.get('etag'),
            'deleted': task_data.get('deleted', 0),
            'attachments': task_data.get('attachments', []),
            'imgMode': task_data.get('imgMode', 0),
            'sortOrder': task_data.get('sortOrder', 0),
            'parentId': task_data.get('parentId'),
            'children': children
        }
        
        return {k: v for k, v in essential_fields.items() if v is not None}

    def build_task_tree(self, tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        将任务列表转换为树形结构
        
        Args:
            tasks: 任务列表
            
        Returns:
            List[Dict[str, Any]]: 树形结构的任务列表
        """
        task_map = {task['id']: task for task in tasks}
        
        for task in tasks:
            task['children'] = []
        
        root_tasks = []
        for task in tasks:
            parent_id = task.get('parentId')
            if parent_id and parent_id in task_map:
                task_map[parent_id]['children'].append(task)
            else:
                root_tasks.append(task)
        
        return root_tasks

    def _get_completed_tasks_info(self) -> Dict[str, Any]:
        completed_tasks_info = {}
        projects = self._get("/api/v2/batch/check/0").get('projectProfiles', [])
        for project in projects:
            project_id = project['id']
            completed_tasks = self._get(f"/api/v2/project/{project_id}/completed/")
            for task in completed_tasks:
                key = f"{task.get('creator')}_{task.get('title')}"
                task['status'] = 2
                task['isCompleted'] = True
                if not task.get('completedTime'):
                    task['completedTime'] = task.get('modifiedTime')
                if not task.get('completedUserId'):
                    task['completedUserId'] = task.get('creator')
                completed_tasks_info[key] = task
        return completed_tasks_info

    def _is_task_completed(self, task: Dict[str, Any]) -> bool:
        """
        判断任务是否已完成
        
        Args:
            task: 任务数据
            
        Returns:
            bool: 是否已完成
        """
        # 检查任务状态
        if task.get('status') == 2 or task.get('isCompleted', False):
            return True
        
        # 检查是否在已完成栏目中
        if task.get('columnId') in self._completed_columns:
            return True
        
        return False

    def get_all_tasks(self, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        tasks = self._get_all_tasks_flat(filters)
        return self.build_task_tree(tasks)

    def _get_all_tasks_flat(self, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        response = self._get("/api/v2/batch/check/0")
        tasks_data = response.get('syncTaskBean', {}).get('update', [])
        projects = response.get('projectProfiles', [])
        tags = response.get('tags', [])
        self._update_column_info(projects)
        completed_tasks_info = self._get_completed_tasks_info()
        tasks = []
        for task in tasks_data:
            if task.get('kind') == 'TEXT':
                task = self._merge_project_info(task, projects)
                task = self._merge_tag_info(task, tags)
                key = f"{task.get('creator')}_{task.get('title')}"
                if key in completed_tasks_info:
                    completed_task = completed_tasks_info[key]
                    original_fields = {
                        'id': task.get('id'),
                        'projectId': task.get('projectId'),
                        'columnId': task.get('columnId'),
                        'sortOrder': task.get('sortOrder'),
                        'tags': task.get('tags', []),
                        'tagDetails': task.get('tagDetails', [])
                    }
                    task.update(completed_task)
                    task.update(original_fields)
                else:
                    task['isCompleted'] = False
                    if task.get('status') == 2:
                        task['status'] = 0
                simplified_task = self._simplify_task_data(task)
                tasks.append(simplified_task)
        if filters:
            filtered_tasks = []
            for task in tasks:
                if self._apply_filters(task, filters):
                    filtered_tasks.append(task)
            return filtered_tasks
        return tasks 