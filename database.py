from supabase import create_client
import os
from dotenv import load_dotenv
from typing import Optional, List, Dict

# Load environment variables
load_dotenv()

# Initialize Supabase client
supabase = create_client(
    os.getenv("SUPABASE_URL", ""),
    os.getenv("SUPABASE_KEY", "")
)

class Database:
    @staticmethod
    async def create_task(task_data: Dict) -> Dict:
        """Create a new task in the database."""
        try:
            response = supabase.table('tasks').insert(task_data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error creating task: {e}")
            return None

    @staticmethod
    async def get_tasks() -> List[Dict]:
        """Get all tasks from the database."""
        try:
            response = supabase.table('tasks').select("*").order('created_at', desc=True).execute()
            return response.data
        except Exception as e:
            print(f"Error getting tasks: {e}")
            return []

    @staticmethod
    async def get_task(task_id: str) -> Optional[Dict]:
        """Get a specific task by ID."""
        try:
            response = supabase.table('tasks').select("*").eq('id', task_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error getting task {task_id}: {e}")
            return None

    @staticmethod
    async def update_task_status(task_id: str, status: str) -> Optional[Dict]:
        """Update the status of a task."""
        try:
            response = supabase.table('tasks').update({"status": status}).eq('id', task_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error updating task {task_id}: {e}")
            return None

    @staticmethod
    async def delete_task(task_id: str) -> bool:
        """Delete a task by ID."""
        try:
            response = supabase.table('tasks').delete().eq('id', task_id).execute()
            return bool(response.data)
        except Exception as e:
            print(f"Error deleting task {task_id}: {e}")
            return False
