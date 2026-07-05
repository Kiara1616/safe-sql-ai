BLOCKED = ["DROP", "DELETE", "UPDATE", "INSERT", "ALTER"]

def is_safe_sql(query: str) -> bool:
    q = query.strip().upper()
    if ";" in q[:-1]:
        return False
    if not q.startswith("SELECT"):
        return False
    return not any(word in q for word in BLOCKED)
