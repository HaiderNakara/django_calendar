from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import redirect
import os.path
from datetime import datetime
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# add your credentials.json file
file = os.path.join(os.path.dirname(__file__), 'credentials.json')
print(file)
CLIENT_SECRETS_FILE = file
SCOPES = ['https://www.googleapis.com/auth/calendar']


@api_view(['GET'])
def GoogleCalendarInitView(request):
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES)
    flow.redirect_uri = 'http://localhost:8000/rest/v1/calendar/redirect/'
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true')
    request.session['state'] = state
    return redirect(authorization_url)


@api_view(['GET'])
def GoogleCalendarRedirectView(request):
    state = request.session.get('state')
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)
    flow.redirect_uri = 'http://localhost:8000/rest/v1/calendar/redirect/'
    authorization_response = request.get_full_path()
    flow.fetch_token(authorization_response=authorization_response)
    credentials = flow.credentials
    try:
        service = build('calendar', 'v3', credentials=credentials)
        now = datetime.utcnow().isoformat() + 'Z'
        events_result = service.events().list(calendarId='primary', timeMin=now,
                                              singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])
        if not events:
            return Response({'Message': 'No upcoming events found.'})
        else:
            events_list = []
            for event in events:
                event_dict = {
                    'id': event['id'],
                    'name': event['summary'],
                    'start': event['start'],
                    'end': event['end']
                }
                events_list.append(event_dict)
            return Response(events_list)
    except HttpError as error:
        print(error)
        return Response({error})
