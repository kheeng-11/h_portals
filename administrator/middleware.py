from django.shortcuts import redirect

class CombinedSessionCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path

        global_allowed = ['/static/', '/media/']

        admin_allowed = ['/administrator/login/', '/administrator/logout/']
        teacher_allowed = ['/teacher/login/', '/teacher/logout/']
        student_allowed = ['/student/login/', '/student/logout/']
        parent_allowed = ['/parent/login/', '/parent/logout/']

        if any(path.startswith(p) for p in global_allowed):
            return self.get_response(request)

        if path.startswith('/administrator/'):
            if not request.session.get('admin_id') and not any(path.startswith(p) for p in admin_allowed):
                return redirect('administrator:login')

        elif path.startswith('/teacher/'):
            if not request.session.get('teacher_id') and not any(path.startswith(p) for p in teacher_allowed):
                return redirect('teacher:login')

        elif path.startswith('/student/'):
            if not request.session.get('student_id') and not any(path.startswith(p) for p in student_allowed):
                return redirect('student:login')

        elif path.startswith('/parent/'):
            if not request.session.get('parent_id') and not any(path.startswith(p) for p in parent_allowed):
                return redirect('parent:login')

        return self.get_response(request)
