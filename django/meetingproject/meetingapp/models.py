from django.db import models
from django.core.exceptions import ValidationError

class Event(models.Model):
    topic = models.CharField(max_length=200)  # Topic of the event
    organiser = models.CharField(max_length=200)
    partner=models.CharField(max_length=200,default='none')
    partner_logo=models.URLField(blank=True, null=True) # Organiser's name
    event_type = models.CharField(max_length=100)  # Type of the event
    participants = models.CharField(max_length=500) # Participants' details
    location = models.CharField(max_length=300)  # Location of the event
    date = models.DateField(null=True)  # Event date
    starttime = models.TimeField(null=True)
    endtime = models.TimeField(null=True)
    actual_starttime = models.TimeField(null=True)
    actual_endtime = models.TimeField(null=True)
    duration = models.DurationField(null=True)
    actual_duration = models.DurationField(null=True)  # Duration of the event
    agenda = models.JSONField(default=list)
    remark = models.JSONField(default=list)
    link = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.topic} organized by {self.organiser}"

class Task(models.Model):
    person = models.CharField(max_length=255)
    remark = models.TextField()
    priority = models.CharField(max_length=50)
    assigned_date = models.DateField()
    final_date = models.DateField()
    meeting = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='tasks')

    def __str__(self):
        return f"Task for {self.meeting.topic} - {self.person}"


    def clean(self):
        """ Validate that the assigned date is before the final date """
        if self.assigned_date >= self.final_date:
            raise ValidationError("Final date must be after assigned date.")

    def __str__(self):
        return f"Task for {self.person} - {self.remark} (Priority: {self.priority})"
