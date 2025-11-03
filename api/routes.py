from fastapi import APIRouter, Query

from controller.application_controller import ApplicationController
from controller.scholarship_controller import ScholarshipController
from core.models import ApplicationCreate, TaskCreate

router = APIRouter()

@router.get("/")
def get_all_scholarships(limit: int = 100):
    """
    Retrieve a list of all available scholarships.
    The model should summarize or present scholarship options clearly to the user.
    Limit the result to 100 items per request to avoid information overload.
    """
    return ScholarshipController.get_all_scholarships(limit)

@router.get("/search")
def search_scholarship(query: str = Query(..., description="Search query text")):
    """
    Search for scholarships that best match the user's input query using Elasticsearch.
    The model should interpret the query semantically (not just keyword-based) and return the most relevant results.
    After presenting results, the model can ask the user if they are interested in applying for one of the suggested scholarships.
    """
    return ScholarshipController.search_scholarship(query, k=10)

@router.post("/applications")
async def create_application(application_data: ApplicationCreate):
    """
    Create a new scholarship application record.
    The model should guide the user through filling required information for applying to a scholarship.
    If any fields are missing or unclear, the model should proactively ask for clarification.
    """
    return await ApplicationController.create_application(application_data)

@router.get("/applications")
async def list_applications():
    """
    Retrieve all scholarship applications submitted by the user.
    The model can summarize each application's current status, deadlines, and progress.
    """
    return await ApplicationController.list_applications()

@router.get("/applications/{application_id}")
async def get_application_by_id(application_id: str):
    """
    Retrieve detailed information for a specific scholarship application identified by its ID.
    The model can highlight key details such as deadlines, required documents, or next steps.
    """
    return await ApplicationController.get_application_by_id(application_id)

@router.post("/tasks")
async def create_task(task_data: TaskCreate):
    """
    Create a new task in the user's scholarship application roadmap.
    The model should help the user define a structured plan, including start and end dates.
    Encourage the user to choose realistic deadlines for better time management.
    """
    return await ApplicationController.create_task(task_data)

@router.get("/tasks/{task_id}")
async def get_task_by_id(task_id: str):
    """
    Retrieve details and progress for a specific task in the user's scholarship roadmap.
    The model can provide suggestions or reminders to help the user complete their tasks on time.
    """
    return await ApplicationController.get_task_by_id(task_id)