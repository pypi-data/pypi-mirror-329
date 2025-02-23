# from pytube import YouTube



# # videoId = video["videoId"]
# #                 videoUrl = video["videoUrl"]
# #                 channelId = video["channelId"]
# #                 channelName = video["videoChannel"]
# #                 videoTitle = video["videoTitle"]
# #                 videoDescription = video["videoDescription"]
# #                 videoThumbnail = video["videoThumbnail"]
# #                 videoPublishDate = video["videoPublishDate"]
# #                 videoViewCount = video["videoViewCount"]
# #                 videoLikeCount = video["videoLikeCount"]
# #                 videoCommentCount = video["videoCommentCount"]
# #                 videoDuration = video["videoDuration"]




# # video_url = "https://www.youtube.com/watch?v=WFcYF_pxLgA"

# # yt = YouTube(video_url)
# # # Get the title of the video
# # videoId = yt.video_id
# # channelId = yt.channel_id
# # channelName = yt.author
# # videoTitle = yt.title
# # videoDescription = yt.description
# # videoThumbnail = yt.thumbnail_url
# # videoPublishDate = yt.publish_date
# # videoViewCount = yt.views
# # videoDuration = yt.length


# # keywords = yt.keywords
# # meta = yt.metadata
# # rating = yt.rating
# # captions= yt.captions
# # vid_info = yt.vid_info

# # print(videoThumbnail)


# from youtubesearchpython import VideosSearch

# def search_youtube(keyword, limit=10):
#     videos_search = VideosSearch(keyword, limit=limit)
#     return videos_search.result()

# # Example usage
# keyword = 'seo'
# search_results = search_youtube(keyword, limit=100)


# print(len(search_results['result']))

# for video in search_results['result']:
#    print(f"Title: {video['title']}, Views: {video.get('viewCount', {}).get('text', 'Unknown')}, URL: {video['link']}")



import datetime
import re
import time
from youtubesearchpython import VideosSearch
from pytrends.request import TrendReq

# Google Trends setup
pytrends = TrendReq()

def parse_relative_date(text):
    current_time = datetime.datetime.now()
    numbers = re.findall(r'\d+', text)
    number = int(numbers[0]) if numbers else 0

    if 'minute' in text or 'minutes' in text:
        return current_time - datetime.timedelta(minutes=number)
    elif 'hour' in text or 'hours' in text:
        return current_time - datetime.timedelta(hours=number)
    elif 'day' in text or 'days' in text:
        return current_time - datetime.timedelta(days=number)
    elif 'week' in text or 'weeks' in text:
        return current_time - datetime.timedelta(weeks=number)
    elif 'month' in text or 'months' in text:
        return current_time - datetime.timedelta(days=number * 30)  # Approximate each month as 30 days
    elif 'year' in text or 'years' in text:
        return current_time - datetime.timedelta(days=number * 365)  # Approximate each year as 365 days
    else:
        return current_time  # Default to now if parsing fails

def calculate_video_age_weight(publish_date_text):
    video_date = parse_relative_date(publish_date_text)
    days_old = (datetime.datetime.now() - video_date).days
    return max(0, 1 - days_old / 365)

def search_youtube(keyword, limit=50):
    print(f"Starting YouTube search for keyword: '{keyword}' with a limit of {limit} results.")
    videos_search = VideosSearch(keyword, limit=limit)
    results = videos_search.result()

    video_details = []
    print("Processing video results...")
    for index, video in enumerate(results['result'], start=1):
        title = video['title']
        description = video['descriptionSnippet'][0]['text'] if 'descriptionSnippet' in video else ""
        publish_date_text = video['publishedTime']
        view_count = int(video['viewCount']['text'].replace(' views', '').replace(',', '')) if 'viewCount' in video else 0

        semantic_relevance = 0.5 if keyword.lower() in title.lower() else 0
        semantic_relevance += 0.5 if keyword.lower() in description.lower() else 0
        age_weight = calculate_video_age_weight(publish_date_text)

        video_details.append({
            'views': view_count,
            'semantic_relevance': semantic_relevance,
            'age_weight': age_weight
        })

        print(f"Video {index}: {title[:50]} | Views: {view_count} | Relevance: {semantic_relevance} | Age Weight: {age_weight}")

    return video_details

def get_trends_data(keyword, retries=5, backoff_factor=1.5):
    for attempt in range(retries):
        try:
            pytrends.build_payload([keyword], cat=0, timeframe='today 12-m', geo='', gprop='youtube')
            data = pytrends.interest_over_time()
            if not data.empty:
                return data[keyword].iloc[-1]  # Return the most recent data point
        except Exception as e:
            sleep_time = backoff_factor ** attempt
            print(f"Exception: {e}. Retrying in {sleep_time} seconds...")
            time.sleep(sleep_time)
    return 0  # No data available or max retries reached

def calculate_search_volume(video_details, trend_value):
    total_weighted_views = 0
    total_relevance_weight = 0

    for video in video_details:
        relevance_weight = (video['semantic_relevance'] + video['age_weight']) / 2
        adjusted_views = video['views'] * (trend_value / 100)
        weighted_views = adjusted_views * relevance_weight

        total_weighted_views += weighted_views
        total_relevance_weight += relevance_weight

    return total_weighted_views / total_relevance_weight if total_relevance_weight > 0 else 0

def calculate_difficulty(video_details):
    total_views = sum(video['views'] for video in video_details)
    average_views = total_views / len(video_details) if video_details else 0

    high_competition_videos = sum(1 for video in video_details if video['views'] > average_views and video['semantic_relevance'] > 0.1)
    return high_competition_videos / len(video_details) if len(video_details) > 0 else 0

# Main execution
start_time = time.time()
print("Script started.")
keyword = 'what is seo'
video_details = search_youtube(keyword, limit=50)
trend_value = get_trends_data(keyword)
search_volume = calculate_search_volume(video_details, trend_value)
difficulty = calculate_difficulty(video_details)
elapsed_time = time.time() - start_time

print(f"Calculated Search Volume: {search_volume:.2f}")
print(f"Calculated Difficulty: {difficulty:.2f}")
print(f"Elapsed Time: {elapsed_time:.2f} seconds")



# import datetime
# from googleapiclient.discovery import build
# from googleapiclient.errors import HttpError
# import pandas as pd
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity
# import numpy as np

# # Replace with your actual API key


# youtube = build('youtube', 'v3', developerKey=API_KEY)

# def search_youtube(keyword, max_results=100,region_code='US', language='en'):
#     try:
#         search_response = youtube.search().list(
#             q=keyword,
#             type='video',
#             part='id,snippet',
#             maxResults=max_results,
#             order='relevance',
#             regionCode=region_code,  # Add region code
#             relevanceLanguage=language  # Add relevant language
#         ).execute()

#         video_ids = [item['id']['videoId'] for item in search_response['items']]
        
#         # YouTube API allows only 50 video IDs per request, so we need to split our requests
#         video_responses = []
#         for i in range(0, len(video_ids), 50):
#             video_response = youtube.videos().list(
#                 id=','.join(video_ids[i:i+50]),
#                 part='statistics,snippet'
#             ).execute()
#             video_responses.extend(video_response['items'])

#         return video_responses
#     except HttpError as e:
#         print(f"An HTTP error {e.resp.status} occurred: {e.content}")
#         return []

# def calculate_semantic_relevance(text, keyword):
#     vectorizer = TfidfVectorizer()
#     tfidf_matrix = vectorizer.fit_transform([text, keyword])
#     return cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]

# def calculate_video_age_weight(publish_date):
#     video_date = datetime.datetime.strptime(publish_date, "%Y-%m-%dT%H:%M:%SZ")
#     days_old = (datetime.datetime.now(datetime.timezone.utc) - video_date.replace(tzinfo=datetime.timezone.utc)).days
#     return np.exp(-days_old / 365)  # Exponential decay

# def get_channel_stats(channel_id):
#     try:
#         channel_response = youtube.channels().list(
#             id=channel_id,
#             part='statistics'
#         ).execute()
#         return channel_response['items'][0]['statistics']
#     except HttpError as e:
#         print(f"An HTTP error {e.resp.status} occurred: {e.content}")
#         return {}

# def analyze_keyword(keyword, max_results=100, region_code='US', language='en'):
#     videos = search_youtube(keyword, max_results,region_code,language)
#     video_details = []

#     for video in videos:
#         snippet = video['snippet']
#         statistics = video['statistics']
#         channel_stats = get_channel_stats(snippet['channelId'])

#         title = snippet['title']
#         description = snippet['description']
#         tags = snippet.get('tags', [])
#         publish_date = snippet['publishedAt']  # Changed from 'publishedTime' to 'publishedAt'

#         view_count = int(statistics.get('viewCount', 0))
#         like_count = int(statistics.get('likeCount', 0))
#         comment_count = int(statistics.get('commentCount', 0))
#         subscriber_count = int(channel_stats.get('subscriberCount', 0))

#         age_weight = calculate_video_age_weight(publish_date)
#         semantic_relevance = calculate_semantic_relevance(f"{title} {description} {' '.join(tags)}", keyword)

#         engagement_rate = (like_count + comment_count) / view_count if view_count > 0 else 0
        
#         # Calculate days since publication
#         publish_datetime = datetime.datetime.strptime(publish_date, "%Y-%m-%dT%H:%M:%SZ")
#         days_since_publish = (datetime.datetime.now(datetime.timezone.utc) - publish_datetime.replace(tzinfo=datetime.timezone.utc)).days
#         normalized_views = view_count / (days_since_publish + 1)  # Add 1 to avoid division by zero for very recent videos

#         video_details.append({
#             'title': title,
#             'views': view_count,
#             'normalized_views': normalized_views,
#             'semantic_relevance': semantic_relevance,
#             'age_weight': age_weight,
#             'engagement_rate': engagement_rate,
#             'subscriber_count': subscriber_count
#         })

#     return video_details

# def calculate_search_volume(video_details):
#     total_weighted_views = 0
#     total_weight = 0

#     for video in video_details:
#         weight = (video['semantic_relevance'] + video['age_weight'] + video['engagement_rate']) / 3
#         weighted_views = video['normalized_views'] * weight

#         total_weighted_views += weighted_views
#         total_weight += weight

#     return total_weighted_views / total_weight if total_weight > 0 else 0

# def calculate_difficulty(video_details):
#     df = pd.DataFrame(video_details)
    
#     # Normalize metrics
#     df['norm_views'] = (df['views'] - df['views'].min()) / (df['views'].max() - df['views'].min())
#     df['norm_relevance'] = (df['semantic_relevance'] - df['semantic_relevance'].min()) / (df['semantic_relevance'].max() - df['semantic_relevance'].min())
#     df['norm_engagement'] = (df['engagement_rate'] - df['engagement_rate'].min()) / (df['engagement_rate'].max() - df['engagement_rate'].min())
#     df['norm_subscribers'] = (df['subscriber_count'] - df['subscriber_count'].min()) / (df['subscriber_count'].max() - df['subscriber_count'].min())

#     # Calculate competition score
#     df['competition_score'] = (df['norm_views'] + df['norm_relevance'] + df['norm_engagement'] + df['norm_subscribers']) / 4

#     # Calculate difficulty as the average competition score
#     difficulty = df['competition_score'].mean()

#     return difficulty

# # Main execution
# keyword = 'what is seo'
# region_code = 'US'
# language = 'en'
# video_details = analyze_keyword(keyword, max_results=100, region_code=region_code, language=language)
# search_volume = calculate_search_volume(video_details)
# difficulty = calculate_difficulty(video_details)

# print(f"Keyword: {keyword}")
# print(f"Region: {region_code}")
# print(f"Language: {language}")
# print(f"Number of videos analyzed: {len(video_details)}")
# print(f"Estimated Search Volume: {search_volume:.2f}")
# print(f"Estimated Difficulty: {difficulty:.2f}")
