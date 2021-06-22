from flask import Flask, jsonify, request, render_template, Markup
from .classes.youtube_video import YoutubeVideo
from markupsafe import escape
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route('/<video_id>')
def hello_world(video_id):
	keyword = request.args.get('keyword')
	video = YoutubeVideo(f'https://www.youtube.com/watch?v={escape(video_id)}')
	mentions = video.get_mentions(keyword)
	full_text = Markup(video.full_text)
	return render_template('index.html', data={
		'video_id': video_id,
		'thumbnail_url': video.thumbnail_url,
		'mentions': mentions,
		'full_text': full_text
	})

@app.route('/', methods=['GET'])
def index():
	return render_template('index.html', data={})

# app.run()