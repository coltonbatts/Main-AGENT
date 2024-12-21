from supabase import create_client
import os
from dotenv import load_dotenv
from typing import Optional, List, Dict
from contextlib import contextmanager

# Load environment variables
load_dotenv()

def get_supabase_client():
    """Create a new Supabase client instance."""
    return create_client(
        os.getenv("SUPABASE_URL", ""),
        os.getenv("SUPABASE_KEY", "")
    )

class Database:
    @staticmethod
    def create_task(task_data: Dict) -> Dict:
        """Create a new task in the database."""
        try:
            client = get_supabase_client()
            response = client.table('tasks').insert(task_data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error creating task: {e}")
            return None

    @staticmethod
    def get_tasks() -> List[Dict]:
        """Get all tasks from the database."""
        try:
            client = get_supabase_client()
            response = client.table('tasks').select("*").order('created_at', desc=True).execute()
            return response.data
        except Exception as e:
            print(f"Error getting tasks: {e}")
            return []

    @staticmethod
    def get_task(task_id: str) -> Optional[Dict]:
        """Get a specific task by ID."""
        try:
            client = get_supabase_client()
            response = client.table('tasks').select("*").eq('id', task_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error getting task {task_id}: {e}")
            return None

    @staticmethod
    def update_task_status(task_id: str, status: str) -> Optional[Dict]:
        """Update the status of a task."""
        try:
            client = get_supabase_client()
            response = client.table('tasks').update({"status": status}).eq('id', task_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error updating task {task_id}: {e}")
            return None

    @staticmethod
    def delete_task(task_id: str) -> bool:
        """Delete a task by ID."""
        try:
            client = get_supabase_client()
            response = client.table('tasks').delete().eq('id', task_id).execute()
            return bool(response.data)
        except Exception as e:
            print(f"Error deleting task {task_id}: {e}")
            return False
