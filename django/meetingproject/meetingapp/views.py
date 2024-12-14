from datetime import datetime,timedelta
from django.shortcuts import render,redirect, get_object_or_404
from .models import Event, Task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib import messages
from django.http import HttpResponse

def meeting(request):
    return render(request,'meeting.html')

#create new meeting
#saves the information from the form in the meeting.html
def meetingsave(request):
    if request.method == "POST":
        topic = request.POST.get('topic')
        organiser = request.POST.get('organiser')
        partner = request.POST.get('partner')
        partner_logo = request.POST.get('partner_logo')
        event_type = request.POST.get('type')
        participants = request.POST.get('participants')
        location = request.POST.get('location')
        date = request.POST.get('date')
        
        try:
            formatted_date = datetime.strptime(date, "%Y-%m-%d").date()  # Parse string to date object
        except ValueError:
            return render(request, 'meeting.html', {"error": "Invalid date format. Please use YYYY-MM-DD."})

        starttime = request.POST.get('starttime') 
        endtime = request.POST.get('endtime')     
        try:
            formatted_start_time = datetime.strptime(starttime, "%H:%M").time()
            formatted_end_time = datetime.strptime(endtime, "%H:%M").time()
        except ValueError:
            return render(request, 'meeting.html', {"error": "Invalid time format. Use HH:MM."}) 
        link=request.POST.get('link')
        agenda = request.POST.getlist('agenda[]')

        filtered_agenda = [agenda.strip() for agenda in agenda if agenda.strip()]

        planned_duration = calculate_time_duration(formatted_start_time, formatted_end_time)

        # Save to the database
        event = Event(
            topic=topic,
            organiser=organiser,
            partner=partner,
            partner_logo=partner_logo,
            event_type=event_type,
            participants=participants,
            location=location,
            date=formatted_date,
            starttime=formatted_start_time,
            endtime=formatted_end_time,
            duration=planned_duration,
            link=link,
            agenda=filtered_agenda,
        )
        event.save()
           
    meetings=Event.objects.all()
    return render(request, 'meeting_list.html',{'meetings':meetings}) 

#sends the meeting invitation using sending.html
def meetingsend(request,id):
    try:
        event=Event.objects.get(id=id)
    except Event.DoesNotExist:
        return(render(request,'meeting.html',{"error":"event not found"}))
    context = {
        'topic': event.topic,
        'organiser': event.organiser,
        'partner':event.partner,
        'partner_logo':event.partner_logo,
        'type': event.event_type,
        'location': event.location,
        'date': event.date,
        'starttime': event.starttime,
        'endtime': event.endtime,
        'duration':event.duration,
        'link':event.link,
        'agenda': event.agenda,
    }

    # Render the HTML content
    html_content = render_to_string('sending.html', context)

    # Create email message
    subject = "Meeting Invitation"
    from_email = "mr.vengeance303@gmail.com"
    to_email = ["sarveshs160405@gmail.com"]

    email = EmailMultiAlternatives(subject, "", from_email, to_email)
    email.attach_alternative(html_content, "text/html")
    try:
        email.send()
    except Exception as e:
        return render(request, 'meeting.html', {"error": f"Error sending email: {str(e)}"})
    return redirect('meeting_list')


#first window that is opened after running which contains all the meeting info 
def meeting_list(request):
    meetings = Event.objects.all()
    return render(request, 'meeting_list.html', {'meetings': meetings})

#renders the template where remark(task) is added
def after_meeting(request, id):
    meeting = Event.objects.get(id=id)
    return render(request, 'add_remark.html', {'meeting': meeting})


#points_discussed part of the m-o-m
#remarks, actual_start_time  and actual_end_time are provided in the form
def points_discussed(request, id):
    if request.method == 'POST':
        meeting = get_object_or_404(Event, id=id)

        meeting.actual_starttime  = request.POST.get('actual_starttime')
        meeting.actual_endtime = request.POST.get('actual_endtime')
        remarks = request.POST.getlist('remark[]')
        try:
            formatted_actual_start_time = datetime.strptime(meeting.actual_starttime, "%H:%M").time()
            formatted_actual_end_time = datetime.strptime(meeting.actual_endtime, "%H:%M").time()
        except ValueError:
            return render(request, 'meeting.html', {"error": "Invalid time format. Use HH:MM."}) 
        
        meeting.actual_duration = calculate_time_duration(formatted_actual_start_time, formatted_actual_end_time)

        filtered_remarks = [remark.strip() for remark in remarks if remark.strip()] 
        meeting.remark = filtered_remarks  
        meeting.save()

        return redirect('meeting_list')


#points_agreed part of the m-o-m
#tasks(remarks) are assigned with priority,assigned date and final date 
def points_agreed(request, id):
    meeting = get_object_or_404(Event, id=id)
    
    if request.method == 'POST':
        # Retrieve form data
        person = request.POST.get('person')
        priority = request.POST.get('priority')
        assigned_date = request.POST.get('assigned_date')
        final_date = request.POST.get('final_date')
        remark = request.POST.get('remark')

        try:
            # Convert string date to datetime object
            assigned_date = datetime.strptime(assigned_date, "%Y-%m-%d").date()
            final_date = datetime.strptime(final_date, "%Y-%m-%d").date()
        except ValueError:
            return HttpResponse("Invalid date format. Please use YYYY-MM-DD.", status=400)

        # Save the task to the Task model (assumed model for task assignments)
        task = Task(
            person=person,
            remark=remark,
            priority=priority,
            assigned_date=assigned_date,
            final_date=final_date,
            meeting=meeting  # Link this task to the meeting
        )
        task.save()

        # Reload the page without redirecting
        return render(request, 'assign_tasks.html', {
            'meeting': meeting,
            'remarks': meeting.remark, 
            'assigned_remarks': [task.remark for task in meeting.tasks.all()]
        })
    
    else:
        # Get remarks for the specific meeting
        remarks = meeting.remark
        assigned_remarks = [task.remark for task in meeting.tasks.all()]
        
        return render(request, 'assign_tasks.html', {
            'meeting': meeting,
            'remarks': remarks,
            'assigned_remarks': assigned_remarks
        })

#deletes the mail from the meeting_list
def delete_meeting(request, id):

    meeting = get_object_or_404(Event, id=id)
    meeting.delete()
    messages.success(request, 'Meeting deleted successfully!')
    return redirect('meeting_list')

#diplayes the m-o-m content by clicking the row
def minutes_of_meeting(request, id):
    meeting = get_object_or_404(Event, id=id)
    tasks = Task.objects.filter(meeting=meeting)  # Get all tasks related to the meeting

    return render(request, 'minutes_of_meeting.html', {'meeting': meeting, 'tasks': tasks})


#calculation of duration with the provided start_time and end_time 
#or if actual_start_time and actual_end_time are provided it takes the later for the calculation
def calculate_time_duration(start_time, end_time):
    """
    Calculate the duration between two times, accounting for cross-midnight scenarios.
    """
    start_datetime = datetime.combine(datetime.min, start_time)
    end_datetime = datetime.combine(datetime.min, end_time)
    if end_datetime < start_datetime:
        end_datetime += timedelta(days=1)
    return end_datetime - start_datetime

#sending mom mail
def send_mom(request, id):

    meeting = get_object_or_404(Event, id=id)
    # Fetch associated tasks from the task table
    tasks = Task.objects.filter(meeting=meeting)
    context = {
        'meeting': {
            'topic': meeting.topic,
            'organiser': meeting.organiser,
            'partner':meeting.partner,
            'event_type': meeting.event_type,
            'participants': meeting.participants,
            'location': meeting.location,
            'date': meeting.date,
            'starttime': meeting.starttime,
            'endtime': meeting.endtime,
            'actual_starttime': meeting.actual_starttime,
            'actual_endtime': meeting.actual_endtime,
            'duration': meeting.duration,
            'actual_duration': meeting.actual_duration,
            'agenda': meeting.agenda,
            'remark': meeting.remark,
            'link': meeting.link,
        },
        'tasks': tasks
    }
    
    # Render the HTML content
    html_content = render_to_string('sending_mom.html', context)
    
    subject = f"Minutes of the Meeting - {meeting.topic}"
    from_email = "mr.vengeance303@gmail.com"
    to_email = ["sarveshs160405@gmail.com"]  # Replace with actual recipient emails
    
    email = EmailMultiAlternatives(subject, "", from_email, to_email)
    email.attach_alternative(html_content, "text/html")

    try:
        email.send()
        return redirect('meeting_list')
    except Exception as e:
        return HttpResponse(f"Failed to send email: {str(e)}")

#https://meet.google.com/vcj-iacy-faa
#g-meet link for your reference 