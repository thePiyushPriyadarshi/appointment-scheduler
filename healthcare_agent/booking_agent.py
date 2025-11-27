from agents import Agent, function_tool
from pydantic import BaseModel
import httpx
from agents import set_tracing_disabled

set_tracing_disabled(True)
from openai import AsyncOpenAI
from agents import set_default_openai_client
from agents import set_default_openai_api

http_client = httpx.AsyncClient(verify=False)
custom_client = AsyncOpenAI(api_key="YOUR_API_KEY",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/", http_client=http_client)
set_default_openai_client(custom_client)
set_default_openai_api("chat_completions")

class AppointmentDetails(BaseModel):
    name : str
    mobile_number: str
    description: str
    preferred_date: str
    preferred_time: str
    provider: str
    appointment_type: str
    disease: str


@function_tool
def get_current_datetime_tool() -> str:
    """
    Provides the current date and time.
    Returns:
        str: Current date and time in ISO format.
    """
    from datetime import datetime
    current_datetime = datetime.now().isoformat()
    return current_datetime


@function_tool
def appointment_scheduler_tool(appointment : AppointmentDetails) -> str:
    """
    Schedules a healthcare appointment based on user preferences.
    Args:
        appointment (AppointmentDetails): Details required to schedule the appointment.
    Returns:
        str: Confirmation message with appointment details.
    """
    # Simulate scheduling logic
    confirmation_message = (
        f"Appointment scheduled with {appointment.provider} on {appointment.preferred_date} at {appointment.preferred_time} "
        f"for a {appointment.appointment_type}."
    )
    print("appointment details:", appointment)
    return confirmation_message

booking_agent = Agent(
    name="Booking Agent",
    model="gemini-2.5-flash",
    handoff_description="Specialist agent for booking healthcare appointments.",
    instructions=f"You are a booking agent that helps users to schedule healthcare appointments. Gather necessary details such that present in {AppointmentDetails} class, all fields are required. Confirm the details with the user before finalizing the booking. If the user provides incomplete information, ask for the missing details. Once all details are collected, Verify all the details with user and after confirmation use the appointment scheduling tool to book the appointment.",
    tools=[appointment_scheduler_tool,get_current_datetime_tool],
)
