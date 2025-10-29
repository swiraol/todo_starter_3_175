def error_for_list_title(list_title, todo_lists):
    if any(list_title == lst['title'] for lst in todo_lists):
        return 'The title must be unique.'
    
    if not 1 <= len(list_title) <= 100:
        return 'The title must be between 1 and 100 characters.'
    
    return None