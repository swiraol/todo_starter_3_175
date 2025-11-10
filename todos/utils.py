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

def delete_todo_by_id(todo_id, lst):
    lst['todos'] = [todo for todo in lst['todos'] if todo_id != todo['id']]
    return None

def complete_all_todos(todos):
    for todo in todos:
        todo['completed'] = True 
    return None

def todos_remaining(lst):
    return sum((1 for todo in lst['todos'] if not todo['completed']))

def is_list_completed(lst):
    return todos_remaining(lst) == 0 and len(lst['todos']) > 0

def is_todo_completed(todo):
    return todo['completed']
            
def sort_items(items, select_completed):
    sorted_items = sorted(items, key=lambda item: item['title'].lower())

    incomplete_items = [item for item in sorted_items if not select_completed(item)]
    complete_items = [item for item in sorted_items if select_completed(item)]

    return incomplete_items + complete_items

def remove_list_by_id(all_lists, list_id):
    new_lists = [lst for lst in all_lists if list_id != lst['id']]

    return new_lists