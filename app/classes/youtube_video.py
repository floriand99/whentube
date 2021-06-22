from pytube import YouTube
import re

class YoutubeVideo:
	def __init__(self, url):
		self.yt = YouTube(url)
		self.video_src = url
		self.title = self.yt.title
		self.thumbnail_url = self.yt.thumbnail_url
		self.publish_date = self.yt.publish_date
	def get_mentions(self, query):
		if 'en' in self.yt.captions:
			captions = self.yt.captions['en'].generate_srt_captions()
		else:
			try:
				captions = self.yt.captions['a.en'].generate_srt_captions()
			except:
				return
		text = captions.split('\n')
		mentions = []
		self.full_text = []
		for i in range(0, len(text)):
			if re.search(rf"\b{query}\b", text[i], re.IGNORECASE):
				time_list = text[i-1].split(' --> ')[0].split(',')[0].split(':')
				seconds = (int(time_list[0]) * 3600) + (int(time_list[1]) * 60) + int(time_list[2])
				mentions.append({'time': text[i-1].split(' --> ')[0], 'seconds': seconds, 'text': text[i]})
				self.full_text.append(re.sub(rf'({query})', rf'<strong seconds="{seconds}">{query}</strong>', text[i], flags=re.IGNORECASE) + '\n')
			else:
				self.full_text.append(text[i] + '\n')
		self.full_text = ' '.join(self.full_text[2::4])
		return mentions