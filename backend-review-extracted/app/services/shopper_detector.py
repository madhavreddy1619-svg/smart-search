def detect_shopper_type(cleaned_query: str, goal: str | None):
    query = cleaned_query.lower()

    if "classroom" in query or "students" in query or "school" in query:
        return "teacher_or_parent"

    if "new hire" in query or "break room" in query or "conference room" in query:
        return "office_manager"

    if "home office" in query or "work from home" in query or "wfh" in query:
        return "remote_worker"

    if "party" in query or "event" in query:
        return "general_consumer"

    if goal in ["new hire desk setup", "break room", "conference room setup"]:
        return "office_manager"

    return "unknown"