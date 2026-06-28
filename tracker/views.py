import json
from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta
from django.views.decorators.csrf import ensure_csrf_cookie
from .models import Task, PomodoroSession

@ensure_csrf_cookie
def timer_page(request):
    # Fetch the 10 most recent sessions
    recent_sessions = PomodoroSession.objects.order_by('-completed_at')[:10]
    # Fetch all tasks
    tasks = Task.objects.order_by('-created_at')
    return render(request, 'tracker/index.html', {
        'sessions': recent_sessions,
        'tasks': tasks
    })

def save_session(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            label = data.get('label', 'General Focus').strip() or 'General Focus'
            session_type = data.get('type', 'WORK')
            duration_minutes = int(data.get('minutes', 25))
            completed = bool(data.get('completed', True))
            
            task = None
            if label:
                task, _ = Task.objects.get_or_create(name=label)
            
            session = PomodoroSession.objects.create(
                task=task,
                task_label=label,
                session_type=session_type,
                duration_minutes=duration_minutes,
                completed_successfully=completed
            )
            return JsonResponse({
                'status': 'saved',
                'session_id': session.id,
                'task_label': session.task_label,
                'completed_at': session.completed_at.strftime('%Y-%m-%d %H:%M:%S')
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'POST requests only'}, status=400)

def task_api(request):
    if request.method == 'GET':
        tasks = list(Task.objects.order_by('-created_at').values('id', 'name'))
        return JsonResponse({'tasks': tasks})
    
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name', '').strip()
            if not name:
                return JsonResponse({'error': 'Task name cannot be empty'}, status=400)
            
            task, created = Task.objects.get_or_create(name=name)
            return JsonResponse({
                'id': task.id,
                'name': task.name,
                'created': created
            }, status=201 if created else 200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
            
    return JsonResponse({'error': 'GET or POST requests only'}, status=405)

def stats_api(request):
    # Calculate stats for dashboard
    now = timezone.now()
    seven_days_ago = now - timedelta(days=7)
    
    # 1. Total stats (all time or active)
    total_minutes = PomodoroSession.objects.filter(
        completed_successfully=True, 
        session_type='WORK'
    ).aggregate(total=Sum('duration_minutes'))['total'] or 0
    
    total_sessions = PomodoroSession.objects.filter(
        completed_successfully=True,
        session_type='WORK'
    ).count()

    # 2. Time per task (pie chart)
    task_stats = PomodoroSession.objects.filter(
        completed_successfully=True,
        session_type='WORK'
    ).values('task_label').annotate(total_minutes=Sum('duration_minutes')).order_by('-total_minutes')[:5]
    
    task_labels = [item['task_label'] for item in task_stats]
    task_values = [item['total_minutes'] for item in task_stats]

    # 3. Daily completed sessions for the last 7 days (bar chart)
    daily_sessions = []
    daily_labels = []
    
    for i in range(6, -1, -1):
        day = now - timedelta(days=i)
        day_start = day.replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = day.replace(hour=23, minute=59, second=59, microsecond=999999)
        
        count = PomodoroSession.objects.filter(
            completed_successfully=True,
            session_type='WORK',
            completed_at__range=(day_start, day_end)
        ).count()
        
        daily_labels.append(day.strftime('%a (%b %d)'))
        daily_sessions.append(count)

    # 4. Session types breakdown (donut chart)
    breakdown = PomodoroSession.objects.filter(completed_successfully=True).values('session_type').annotate(count=Count('id'))
    breakdown_dict = {'WORK': 0, 'SHORT_BREAK': 0, 'LONG_BREAK': 0}
    for item in breakdown:
        breakdown_dict[item['session_type']] = item['count']
        
    return JsonResponse({
        'total_focus_minutes': total_minutes,
        'total_completed_sessions': total_sessions,
        'task_distribution': {
            'labels': task_labels,
            'values': task_values
        },
        'daily_progress': {
            'labels': daily_labels,
            'values': daily_sessions
        },
        'session_breakdown': breakdown_dict
    })
