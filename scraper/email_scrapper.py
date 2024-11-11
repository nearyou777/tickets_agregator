from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import json
import google.generativeai as genai
import os
import typing_extensions
import base64
from google.oauth2.credentials import Credentials
import os
from google.auth.transport.requests import Request
from typing import List
from time import sleep
from dotenv import load_dotenv
from shared.models import Tickets, Session
from images_scrapper import google_image_search, save_image
import uuid
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
CREDENTIALS_FILE = 'shared/credentials.json'
TOKEN_FILE = 'shared/token.json'
SENDERS = ['hello@ashleygetsaround.com']

load_dotenv()

class Recipe(typing_extensions.TypedDict):
    ticket_data: str
    
def configure_gemini() -> genai.GenerativeModel:
    """
    Set up gemini model
    """
    key = str(os.getenv('GOOGLE_API_KEY'))
    genai.configure(api_key=key)
    model = genai.GenerativeModel("gemini-1.5-pro-latest")
    return model

def generate_gemini_content(model: genai.GenerativeModel, prompt: str) -> List[Recipe]:

    return model.generate_content(
        prompt,
        generation_config=genai.GenerationConfig(
            response_mime_type="application/json", response_schema=list[Recipe]
        ),
    )


def get_credentials():
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=5000)
            with open(TOKEN_FILE, 'w') as token:
                token.write(creds.to_json())
    
    return build('gmail', 'v1', credentials=creds)


def get_email_content(service, message_id: str) -> str:
    """
    Message content
    """
    message = service.users().messages().get(userId='me', id=message_id, format='full').execute()
    for part in message.get('payload', {}).get('parts', []):
        if part['mimeType'] == 'text/plain':
            data = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
            return data
    return None


def get_messages(service, sender_email) -> List[dict]:
    """
    List of the last messages
    """
    query = f"from:{sender_email}" if sender_email else ""
    results = service.users().messages().list(userId='me', q=query, maxResults=10).execute()
    return results.get('messages', [])


# Helper Function to Create Prompt
def create_prompt(content: str) -> str:
    return f'''
Please extract information from this message in JSON format with the following fields. If any field lacks data, use the default values described.

Fields:
- ID : set this column as null
- ValidMessage: Set to True if the message contains travel information; otherwise, False.
- Title: Title of the trip (e.g., 'Whitefish, Montana\n(All fares round-trip, * nonstop)').
- Type: Type of deal, 'Cash' or 'Point'.
- Cabin: Cabin type (e.g., 'Economy').
- Price: Trip price (with $ symbol); if not found, set to 0.
- OriginalPrice: Original price (with $ symbol); if missing, set to the same as Price.
- Dates: Travel dates (e.g., 'Nov 2024 - Aug 2025').
- Book: Link to book the trip; if none, set to `null`.
- DepartureCities: List of possible departure cities; if unavailable, provide airport codes instead.
- DepartureAirports: Comma-separated airport codes (e.g., 'IAH, SFO').
- BookGuide: Short guide on booking the trip.
- Summary: Summary of the deal. A brief conclusion about deal, why user should by it (e.g., 'Head to Europe or North Africa next year with this Flying Blue sale! Best availability from January through April. Book for as low as 25k points R/T with a transfer bonus (details below). 



Nonstop to Amsterdam & Paris with connecting flights available throughout Europe and North Africa for the same price. These fares include a carry-on and checked bag. Advanced seat assignment starts at ~$30 or choose a seat for free at check-in.



Book with Air France/KLM Flying Blue

Flying Blue is charging 30k miles roundtrip from these cities, which is 25% off the usual rates. Transfer points from Amex Membership Rewards, Bilt, Capital One, Chase, Citi, or Wells Fargo (usually instant).



Take advantage of a 20% transfer bonus from Amex to book from 25k Amex MR points round trip!').
- PictureName : just famous city attraction or a city name or  (if trip to europe just a random city in europe)

Message content: 
{content}
'''

def extract_and_process_emails(service, model, tickets: List[str]):
    data = []
    for sender_email in SENDERS:
        messages = get_messages(service, sender_email)
        for message in messages:
            if f"Email-{message['id']}" in tickets:
                continue
            content = get_email_content(service, message['id'])
            if content:
                results = generate_gemini_content(model, create_prompt(content))
                if results:
                    results = results.text
                try:
                    outer_data = json.loads(results)[0]
                except:
                    continue

                try:
                    ticket_data = json.loads(outer_data['ticket_data'])
                except:
                    ticket_data = outer_data

                try:
                    if ticket_data['ValidMessage']:
                        ticket_data['ID'] = f"Email-{message['id']}"
                        ticket_data['DepartureCities'] = '\n'.join(ticket_data['DepartureCities'])
                        del ticket_data['ValidMessage']
                        ticket_data['PictureName'] = google_image_search(query=ticket_data['PictureName'])
                        picture_name = ticket_data['PictureName'].split('/')[-1]
                        if len(picture_name) > 100:
                            image_format = picture_name.split('.')[-1]
                            picture_name = f"{str(uuid.uuid4())}.{image_format}"
                        if not ticket_data['Cabin']: 
                            ticket_data['Cabin'] = 'Currently Unkown'
                        ticket_data['PictureName'] = save_image(picture_name, ticket_data['PictureName'])
                        if not ticket_data['Book']: ticket_data['Book']= 'https://www.google.com/travel/flights'
                        data.append(ticket_data)
                except:
                    continue
    return data


def add_email():
    service = get_credentials()
    model = configure_gemini()
    with Session() as session:
        tickets = [
            str(row.ID) for row in session.query(Tickets).filter(Tickets.ID.like(r"%Email%")).all()
        ]
        session.commit()
    data = extract_and_process_emails(service,model,tickets)
    return data

if __name__ == '__main__':
    add_email()