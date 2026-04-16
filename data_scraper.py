import os
import isodate
import numpy as np

from googleapiclient.discovery import build

class YouTubeDataScraper:
    def __init__(self, api_key):
        self.api_key = api_key
        self.youtube = build('youtube', 'v3', developerKey=self.api_key)

    def get_empirical_data(self, keyword, num_videos=50):
        print(f"Fetching real data for keyword: {keyword}")
        request = self.youtube.search().list(
            part="id",
            q=keyword,
            type="video",
            videoDuration="medium",
            maxResults=num_videos,
            order="relevance"
        )
        response = request.execute()
        
        video_ids = [item['id']['videoId'] for item in response.get('items', []) if item['id'].get('videoId')]
        
        if not video_ids:
            return None
            
        stats_request = self.youtube.videos().list(
            part="statistics,contentDetails",
            id=",".join(video_ids)
        )
        stats_response = stats_request.execute()
        
        views = []
        comments = []
        watch_time_est = []
        likes_ratio = []
        
        for item in stats_response.get('items', []):
            stats = item.get('statistics', {})
            content = item.get('contentDetails', {})
            
            vCount = int(stats.get('viewCount', 0))
            cCount = int(stats.get('commentCount', 0))
            lCount = int(stats.get('likeCount', 0))
            
            # Estimate watch time: assume 40% retention of total duration
            duration_str = content.get('duration', 'PT0M0S')
            try:
                dur_seconds = isodate.parse_duration(duration_str).total_seconds()
            except:
                dur_seconds = 600
                
            w_time = (dur_seconds * 0.4) / 60.0 # in minutes
            
            if vCount > 0:
                views.append(vCount)
                comments.append(cCount)
                watch_time_est.append(w_time)
                # Estimating "likes ratio" since dislikes are hidden: 
                # (likes / views) is a better metric, but we'll scale it to percentage
                ratio = lCount / vCount if vCount > 0 else 0
                likes_ratio.append(ratio * 100) 
        
        return {
            "avg_views": round(float(np.mean(views))),
            "avg_comments": round(float(np.mean(comments))),
            "avg_watch_time": round(float(np.mean(watch_time_est)), 2),
            "avg_likes_ratio": round(float(np.mean(likes_ratio)), 1)
        }

if __name__ == '__main__':
    API_KEY = 'AIzaSyBC2zIVu_9EQauhq2aYZdoUuauvvP2blHk'
    scraper = YouTubeDataScraper(API_KEY)
    
    collab_data = scraper.get_empirical_data("Gaming Collaboration", num_videos=50)
    drama_data = scraper.get_empirical_data("Gaming Beef Drama", num_videos=50)
    
    print("\n--- Empirical Data Averages ---")
    print(f"Collaboration: {collab_data}")
    print(f"Beef/Drama: {drama_data}")
