import uuid


def create_housekeeping_request(room_number: int, request: str) -> dict:
    """Create a mock housekeeping request."""

    ticket_id = "HK-" + str(uuid.uuid4())[:8].upper()

    return {
        "success": True,
        "ticket_id": ticket_id,
        "room_number": room_number,
        "request": request,
        "status": "CREATED",
        "message": "Housekeeping request created successfully."
    }


def create_maintenance_request(room_number: int, issue: str) -> dict:
    """Create a mock maintenance request."""

    ticket_id = "MT-" + str(uuid.uuid4())[:8].upper()

    return {
        "success": True,
        "ticket_id": ticket_id,
        "room_number": room_number,
        "issue": issue,
        "status": "CREATED",
        "message": "Maintenance request created successfully."
    }


def contact_front_desk(room_number: int, reason: str) -> dict:
    """Create a mock request for front-desk assistance."""

    ticket_id = "FD-" + str(uuid.uuid4())[:8].upper()

    return {
        "success": True,
        "ticket_id": ticket_id,
        "room_number": room_number,
        "reason": reason,
        "status": "CREATED",
        "message": "Front desk has received the request."
    }
