def error_for_list_title(list_title, todo_lists):
    if any(list_title == lst['title'] for lst in todo_lists):
        return 'The title must be unique.'
    
    if not 1 <= len(list_title) <= 100:
        return 'The title must be between 1 and 100 characters.'
    
    return None

def error_for_todo_title(todo_title):
    if not 1 <= len(todo_title) <= 100:
        return 'The title must be between 1 and 100 characters.'
    
    return None

def find_list_by_id(list_id, lists):
    return next((lst for lst in lists if list_id == lst['id']), None)

def find_todo_by_id(todo_id, todos):
    return next((todo for todo in todos if todo_id == todo['id']), None)
            
