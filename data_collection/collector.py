from .scraper import SocialMediaScraper
from .database import Profile

class DataCollector:
    def __init__(self):
        self.scraper = SocialMediaScraper()

    def collect_profile(self, platform, profile_url):
        profile_data = self.scraper.scrape_profile(platform, profile_url)
        username = profile_data['username']

        existing_profile = Profile.find_by_username(platform, username)
        if existing_profile:
            existing_profile.update(profile_data)
        else:
            new_profile = Profile(platform, username, profile_data)
            new_profile.save()

        return profile_data

    def collect_multiple_profiles(self, profile_urls):
        collected_data = []
        for platform, url in profile_urls:
            profile_data = self.collect_profile(platform, url)
            collected_data.append(profile_data)
        return collected_data
