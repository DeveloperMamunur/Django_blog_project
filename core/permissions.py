from accounts.models import UserPermission

def checkUserPermission(request, accessType, menuUrl):
    try:
        user_permissions = {
            'can_view': 'can_view',
            'can_add': 'can_add',
            'can_edit': 'can_edit',
            'can_delete': 'can_delete',
        }
        if request.user.is_superuser:
            return True
        else:
            check_user_permission = UserPermission.objects.filter(
                user_id=request.user.id, is_active=True, **{user_permissions[accessType]: True},
                menu__menu_url=menuUrl
            ).first()
            if check_user_permission:
                return True
            else:
                return False
    except:
        return False
