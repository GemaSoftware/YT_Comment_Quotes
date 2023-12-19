import os
import re
import google.oauth2.credentials
from googleapiclient.discovery import build
import csv

API_KEY = 'REDACTED'
VIDEO_ID = 'REDACTED'

def get_authenticated_service():
    api_service_name = 'youtube'
    api_version = 'v3'

    if API_KEY:
        return build(api_service_name, api_version, developerKey=API_KEY)

def extract_quotes(text):
    quote_pattern = re.compile(r'"([^"]*)"')
    matches = quote_pattern.findall(text)
    return matches

def write_to_csv(quotes, csv_filename='quotes1.csv'):
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Quote'])
        csv_writer.writerows([[quote] for quote in quotes])

def get_video_comments(service, **kwargs):
    comments = []
    nextPageToken = None

    while True:
        results = service.commentThreads().list(**kwargs, pageToken=nextPageToken).execute()

        for item in results['items']:
            comment_text = item['snippet']['topLevelComment']['snippet']['textDisplay']
            
            if '"' in comment_text:
                quotes = extract_quotes(comment_text)
                comments.extend(quotes)

        nextPageToken = results.get('nextPageToken')

        if not nextPageToken:
            break

    return comments

def main():
    youtube = get_authenticated_service()

    comments = get_video_comments(
        youtube,
        part='snippet',
        videoId=VIDEO_ID,
        textFormat='plainText',
        #gets 100 per page
        maxResults=100
    )

    write_to_csv(comments)
    print(f'Quotes written to CSV file bruh')



if __name__ == '__main__':
    main()