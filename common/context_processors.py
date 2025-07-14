from core.permissions import checkUserPermission

def menu_permissions(request):
    if not request.user.is_authenticated:
        return {}
    
    return {
        'can_view_categories': request.user.is_superuser or checkUserPermission(request, 'can_view', '/backend/category'),
        'can_add_categories': request.user.is_superuser or checkUserPermission(request, 'can_add', '/backend/category'),
        'can_view_tags': request.user.is_superuser or checkUserPermission(request, 'can_view', '/backend/tags'),
        'can_add_tags': request.user.is_superuser or checkUserPermission(request, 'can_add', '/backend/tags'),
        'can_view_posts': request.user.is_superuser or checkUserPermission(request, 'can_view', '/backend/post'),
    }
