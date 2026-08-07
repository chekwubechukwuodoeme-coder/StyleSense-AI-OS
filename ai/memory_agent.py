from database.memory import get_memory

USER_ID = 1


def build_memory():

    memory = get_memory(USER_ID)

    if not memory:
        return ""

    sections = []

    sections.append("# USER PROFILE")

    for key, value in memory.items():

        sections.append(f"- {key}: {value}")

    return "\n".join(sections)