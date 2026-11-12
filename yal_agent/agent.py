
from .classifier import classify
from .schemas import AgentRequest, Intent
from .tools import (
    create_housekeeping_request,
    create_maintenance_request,
    contact_front_desk,
)


def handle_guest_request(
    guest_message: str,
    room_number: int | None = None
) -> dict:

    # 1. Validate the guest's request
    request = AgentRequest(
        guest_message=guest_message,
        room_number=room_number
    )

    # 2. Understand the guest's intent using Day 1 classifier
    classification = classify(request.guest_message)

    # 3. Check whether classification failed
    if classification["error"]:
        return {
            "success": False,
            "action_taken": False,
            "response": (
                "I'm sorry, I couldn't process your request. "
                "Please try again."
            )
        }

    result = classification["result"]

    # 4. Handle emergencies before all other decisions
    if result["intent"] == Intent.EMERGENCY.value:
        return {
            "success": True,
            "action_taken": False,
            "response": (
                "This may be an emergency. Please move away "
                "from the danger and do not touch the affected "
                "equipment. Alert the front desk immediately. "
                "If there is fire or immediate danger, contact "
                "local emergency services. I have not dispatched "
                "emergency assistance."
            )
        }

    # 5. Ask for clarification if required
    if result["needs_clarification"]:
        return {
            "success": False,
            "action_taken": False,
            "response": result["clarification_question"]
        }

    intent = result["intent"]

    # 6. Select the correct tool

    if intent == Intent.HOUSEKEEPING.value:

        if request.room_number is None:
            return {
                "success": False,
                "action_taken": False,
                "response": "Could you please share your room number?"
            }

        tool_result = create_housekeeping_request(
            request.room_number,
            request.guest_message
        )

    elif intent == Intent.MAINTENANCE.value:

        if request.room_number is None:
            return {
                "success": False,
                "action_taken": False,
                "response": "Could you please share your room number?"
            }

        tool_result = create_maintenance_request(
            request.room_number,
            request.guest_message
        )

    elif intent == Intent.COMPLAINT.value:

        if request.room_number is None:
            return {
                "success": False,
                "action_taken": False,
                "response": "Could you please share your room number?"
            }

        tool_result = contact_front_desk(
            request.room_number,
            request.guest_message
        )

    # 7. Handle information questions without creating a ticket
    elif intent == Intent.INFORMATION.value:
        return {
            "success": True,
            "action_taken": False,
            "response": (
                "I don't have verified hotel information available "
                "right now. Please contact the front desk for assistance."
            )
        }

    # 8. Handle unsupported or unrecognised requests
    else:
        return {
            "success": False,
            "action_taken": False,
            "response": (
                "I'm not sure how to handle that request. "
                "Could you please provide more details?"
            )
        }

    # 9. Check the actual tool result before confirming
    if not tool_result.get("success"):
        return {
            "success": False,
            "action_taken": False,
            "response": (
                "I'm sorry, your request could not be created. "
                "Please contact the front desk."
            )
        }

    # 10. Confirm only after successful tool execution
    return {
        "success": True,
        "action_taken": True,
        "ticket_id": tool_result["ticket_id"],
        "response": (
            f"Your request has been created successfully. "
            f"Your ticket number is {tool_result['ticket_id']}."
        )
    }