import os 
import sys
import django
import csv

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dmfriends.settings")
django.setup()

from user.models import Member, BoardLike, CommentLike, RecentView

CSV_PATH_PRODUCTS = './board_likes.csv'

with open(CSV_PATH_PRODUCTS) as in_file:
	data_reader = csv.reader(in_file)
	next(data_reader, None)
	for row in data_reader:
		created = BoardLike.objects.get_or_create(
			member_id = row[0]
		    is_like   = row[1]
            board_id  = row[2]
        )        
	

