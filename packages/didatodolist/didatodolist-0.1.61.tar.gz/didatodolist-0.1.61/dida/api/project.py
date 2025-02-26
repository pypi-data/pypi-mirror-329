"""
项目相关API
"""
from typing import List, Optional, Dict, Any
from .base import BaseAPI

class ProjectAPI(BaseAPI):
    """项目相关的API实现"""
    
    def get_projects(self, name: Optional[str] = None, color: Optional[str] = None,
                    group_id: Optional[str] = None, include_tasks: bool = True) -> List[Dict[str, Any]]:
        """
        获取项目列表，支持多种筛选条件
        
        Args:
            name: 项目名称筛选
            color: 项目颜色筛选
            group_id: 项目组ID筛选
            include_tasks: 是否包含任务列表
            
        Returns:
            List[Dict[str, Any]]: 项目列表
        """
        response = self._get("/api/v2/batch/check/0")
        projects_data = response.get('projectProfiles', [])
        tasks_data = response.get('syncTaskBean', {}).get('update', [])
        
        # 处理项目数据
        result = []
        for project in projects_data:
            match = True
            
            # 应用筛选条件
            if name and project.get('name') != name:
                match = False
            if color and project.get('color') != color:
                match = False
            if group_id and project.get('groupId') != group_id:
                match = False
            
            if match:
                project_data = project.copy()
                
                # 添加任务列表（如果需要）
                if include_tasks:
                    project_tasks = [
                        task for task in tasks_data
                        if task.get('projectId') == project['id']
                    ]
                    project_data['tasks'] = project_tasks
                    
                result.append(project_data)
                
        return result

    def create_project(self, name: str, color: Optional[str] = None,
                      group_id: Optional[str] = None, view_mode: str = "list",
                      is_inbox: bool = False) -> Dict[str, Any]:
        """
        创建新项目
        
        Args:
            name: 项目名称
            color: 项目颜色
            group_id: 项目组ID
            view_mode: 视图模式，默认为list
            is_inbox: 是否为收集箱
            
        Returns:
            Dict[str, Any]: 创建的项目数据
        """
        project_data = {
            "name": name,
            "color": color,
            "groupId": group_id,
            "viewMode": view_mode,
            "inAll": True,
            "sortOrder": 0,
            "sortType": "sortOrder",
            "isInbox": is_inbox
        }
        
        # 移除None值的字段
        project_data = {k: v for k, v in project_data.items() if v is not None}
        
        response = self._post("/api/v2/project", data=project_data)
        return response

    def get_project(self, project_id: str) -> Optional[Dict[str, Any]]:
        """
        获取单个项目的详细信息
        
        Args:
            project_id: 项目ID
            
        Returns:
            Optional[Dict[str, Any]]: 项目数据，如果项目不存在则返回None
        """
        try:
            response = self._get(f"/api/v2/project/{project_id}")
            return response
        except Exception:
            return None

    def update_project(self, project_id: str, name: Optional[str] = None,
                      color: Optional[str] = None, group_id: Optional[str] = None,
                      view_mode: Optional[str] = None) -> Dict[str, Any]:
        """
        更新项目信息
        
        Args:
            project_id: 项目ID
            name: 新的项目名称
            color: 新的项目颜色
            group_id: 新的项目组ID
            view_mode: 新的视图模式
            
        Returns:
            Dict[str, Any]: 更新结果
        """
        # 获取当前项目信息
        current_project = self.get_project(project_id)
        if not current_project:
            return {
                "success": False,
                "info": f"未找到ID为 '{project_id}' 的项目",
                "data": None
            }
        
        # 构建更新数据
        update_data = current_project.copy()
        
        if name is not None:
            update_data['name'] = name
        if color is not None:
            update_data['color'] = color
        if group_id is not None:
            update_data['groupId'] = group_id
        if view_mode is not None:
            update_data['viewMode'] = view_mode
        
        try:
            response = self._post(f"/api/v2/project/{project_id}", data=update_data)
            return {
                "success": True,
                "info": "项目更新成功",
                "data": response
            }
        except Exception as e:
            return {
                "success": False,
                "info": f"更新项目失败: {str(e)}",
                "data": None
            }

    def delete_project(self, project_id: str) -> Dict[str, Any]:
        """
        删除项目
        
        Args:
            project_id: 项目ID
            
        Returns:
            Dict[str, Any]: 删除操作的结果
        """
        try:
            # 获取项目信息用于返回
            project = self.get_project(project_id)
            if not project:
                return {
                    "success": False,
                    "info": f"未找到ID为 '{project_id}' 的项目",
                    "data": None
                }
            
            # 发送删除请求
            self._delete(f"/api/v2/project/{project_id}")
            
            return {
                "success": True,
                "info": f"成功删除项目 '{project.get('name', project_id)}'",
                "data": project
            }
        except Exception as e:
            return {
                "success": False,
                "info": f"删除项目失败: {str(e)}",
                "data": None
            }

    def get_project_tasks(self, project_id: str) -> List[Dict[str, Any]]:
        """
        获取项目下的所有任务
        
        Args:
            project_id: 项目ID
            
        Returns:
            List[Dict[str, Any]]: 任务列表
        """
        response = self._get("/api/v2/batch/check/0")
        tasks_data = response.get('syncTaskBean', {}).get('update', [])
        return [
            task for task in tasks_data
            if task.get('projectId') == project_id
        ] 