
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import UserProfile, Issue





def index(request):
    return render(request, 'index.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                pass  
            else:
                user = None
        except User.DoesNotExist:
            user = None
        
        if user is not None:
            
            login(request, user)
            if user.is_superuser:
                return redirect('admindash')
            else:
                return redirect('user')
        else:
            return HttpResponse("Invalid Credentials")
            
    return render(request, 'login.html')

def signin(request):
    if request.method == 'POST':
        full_name = request.POST.get('fullName')
        email = request.POST.get('email')
        password = request.POST.get('password')
        hostel_block = request.POST.get('hostelBlock')
        is_admin = request.POST.get('isAdmin') == 'on'

        if not User.objects.filter(email=email).exists():

            user = User.objects.create_user(username=email, email=email, password=password)
            user.first_name = full_name
            if is_admin:
                user.is_staff = True
                user.is_superuser = True
            user.save()

            UserProfile.objects.create(user=user, hostel_block=hostel_block)
            return redirect('login')
        else:
            return HttpResponse("Email already exists")

    return render(request, 'signin.html')





@login_required
def user(request):
    """
    Handles requests to the root of the app.
    Returns a simple message.
    """
    status_filter = request.GET.get('status', 'all')
    category_filter = request.GET.get('category', 'all')
    issues = Issue.objects.filter(reported_by=request.user)
    if status_filter != 'all':
        issues = issues.filter(status=status_filter)
    if category_filter != 'all':
        issues = issues.filter(category=category_filter)
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = None
    all_issues = Issue.objects.filter(reported_by=request.user)
    notifications = []
    for issue in all_issues.order_by('-created_at'):
        if issue.status == 'In Progress':
            notifications.append({
                'message': f'Your issue "{issue.title}" is in progress.',
                'type': 'info',
                'issue': issue
            })
        elif issue.status == 'Resolved':
            notifications.append({
                'message': f'Your issue "{issue.title}" has been resolved.',
                'type': 'success',
                'issue': issue
            })
    context = {
        'issues': issues,
        'user_profile': user_profile,
        'selected_status': status_filter,
        'selected_category': category_filter,
        'total_issues': all_issues.count(),
        'pending': all_issues.filter(status='Pending').count(),
        'in_progress': all_issues.filter(status='In Progress').count(),
        'resolved': all_issues.filter(status='Resolved').count(),
        'notifications': notifications,
    }
    return render(request,'user.html', context)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def admindash(request):
    """
    Admin dashboard view showing all issues with management capabilities.
    """
    category_filter = request.GET.get('category', 'all')
    status_filter = request.GET.get('status', 'all')

    issues = Issue.objects.all().order_by('-created_at')

    if category_filter != 'all':
        issues = issues.filter(category=category_filter)
    if status_filter != 'all':
        issues = issues.filter(status=status_filter)

    total_users = User.objects.count()
    total_issues = Issue.objects.count()
    pending_count = Issue.objects.filter(status='Pending').count()
    in_progress_count = Issue.objects.filter(status='In Progress').count()
    resolved_count = Issue.objects.filter(status='Resolved').count()

    context = {
        'issues': issues,
        'total_users': total_users,
        'total_issues': total_issues,
        'pending_count': pending_count,
        'in_progress_count': in_progress_count,
        'resolved_count': resolved_count,
        'selected_category': category_filter,
        'selected_status': status_filter,
    }
    return render(request,'admindash.html', context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def update_issue_status(request, issue_id):
    """
    Update the status of an issue via AJAX POST request.
    """
    if request.method == 'POST':
        new_status = request.POST.get('status')
        try:
            issue = Issue.objects.get(id=issue_id)
            issue.status = new_status
            issue.save()
            return JsonResponse({'success': True, 'status': issue.get_status_display()})
        except Issue.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Issue not found'})
    return JsonResponse({'success': False, 'error': 'Invalid request'})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def delete_issue(request, issue_id):
    """
    Delete an issue via POST request.
    """
    if request.method == 'POST':
        try:
            issue = Issue.objects.get(id=issue_id)
            issue.delete()
            return JsonResponse({'success': True})
        except Issue.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Issue not found'})
    return JsonResponse({'success': False, 'error': 'Invalid request'})

@login_required
def logout_view(request):
    """
    Logout the user and redirect to login page.
    """
    logout(request)
    return redirect('login')

@login_required
@login_required
def report(request):
    """
    Handles requests to the root of the app.
    Returns a simple message.
    """
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        category = request.POST.get('category')
        location = request.POST.get('location')


        Issue.objects.create(
            title=title,
            description=description,
            category=category,
            location=location,
            reported_by=request.user
        )
        return redirect('user')

    return render(request,'report.html')


