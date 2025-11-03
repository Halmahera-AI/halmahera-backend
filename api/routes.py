from fastapi import APIRouter, Query

from controller.application_controller import ApplicationController
from controller.scholarship_controller import ScholarshipController
from core.models import ApplicationCreate, TaskCreate

router = APIRouter()

@router.get("/")
def get_all_scholarships(limit: int = 100):
    """
    Retrieve a list of all available scholarships.
    The model should present scholarship options clearly and concisely.
    Limit the result to 100 items per request to avoid information overload.
    """
    return ScholarshipController.get_all_scholarships(limit)

@router.get("/search")
def search_scholarship(query: str = Query(..., description="Search query text")):
    """
    Search for scholarships that best match the user's input query using semantic search.

    CRITICAL FLOW CONTROL:
    - ONLY return the most relevant scholarships that match the user's query precisely
    - DO NOT include scholarships from unrelated countries or fields
    - After presenting results, ask the user if they want to apply for any specific scholarship
    - DO NOT proceed to any other steps until user selects a scholarship

    The model must:
    - Filter results strictly based on query semantics (e.g., "Sweden" should only show Swedish scholarships)
    - Present results in clear bullet points with: name, deadline, eligibility, country
    - Wait for user to explicitly choose a scholarship before suggesting next steps
    - Only mention application process AFTER user selects a specific scholarship
    """
    return ScholarshipController.search_scholarship(query, k=10)

@router.post("/applications")
async def create_application(application_data: ApplicationCreate):
    """
    Create a new scholarship application record for the user's selected scholarship.

    STRICT FLOW SEQUENCE:
    1. Guide user through filling ALL required fields for the chosen scholarship
    2. Proactively ask for clarification if information is missing
    3. After successful creation, CONFIRM successful registration
    4. Provide brief summary: scholarship name, deadlines, next steps
    5. Ask user if they want to create a personalized preparation plan (task roadmap)

    CRITICAL RULES:
    - DO NOT call create_task endpoint from here
    - DO NOT suggest creating tasks until AFTER application is confirmed
    - ONLY ask about task roadmap creation after confirming application success
    - Wait for user's explicit agreement before proceeding to task creation

    This continues the flow: search_scholarship → [user selects] → create_application
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
    Create a new task roadmap for the user's scholarship application process.

    STRICT FLOW REQUIREMENTS:
    - This endpoint should ONLY be called AFTER:
      1. User has successfully created an application AND
      2. LLM has confirmed the application was registered AND  
      3. LLM has asked if user wants a preparation plan AND
      4. User has explicitly agreed to create a task roadmap

    Steps:
    1. Help define specific tasks with start and end dates based on scholarship deadline
    2. Suggest realistic deadlines organized to optimize preparation
    3. Encourage user to confirm or adjust each task
    4. Summarize the full task roadmap once created

    The model must:
    - Ensure user understands this is a separate step from application creation
    - Guide step-by-step in creating each task
    - Confirm user agreement before finalizing roadmap
    """
    return await ApplicationController.create_task(task_data)

@router.get("/tasks/{task_id}")
async def get_task_by_id(task_id: str):
    """
    Retrieve details and progress for a specific task in the user's scholarship roadmap.
    The model can provide suggestions or reminders to help the user complete their tasks on time.
    """
    return await ApplicationController.get_task_by_id(task_id)