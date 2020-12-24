import os
import sys
import django
import csv
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dmfriends.settings")
django.setup()
from user.models import Member, BoardLike, CommentLike, RecentView
from board.models import Board, Comment, BoardImage

CSV_PATH = '.members.csv'
with open(CSV_PATH) as csv_file:
    data_reader = csv.reader(csv_file)
    rows = csv.reader(csv_file, delimiter=',')
    next(rows)
    for row in rows:
        Member.objects.create(email=row[0], nickname=row[1], privacy_agreement=row[2], anonymous=row[3], random_number=[4], password=row[5])
CSV_PATH = '.data/boards.csv'
with open(CSV_PATH) as csv_file:
    data_reader = csv.reader(csv_file)
    rows = csv.reader(csv_file, delimiter=',')
    next(rows)
    for row in rows:
        Board.objects.create(uploader=row[0], created_at=row[1], title=row[2], content=row[3], theme=[4])
CSV_PATH = '.data/board_images.csv'
with open(CSV_PATH) as csv_file:
    data_reader = csv.reader(csv_file)
    rows = csv.reader(csv_file, delimiter=',')
    next(rows)
    for row in rows:
        BoardImage.objects.create(image_url=row[0], board_id=row[1])
CSV_PATH = '.data/board_likes.csv'
with open(CSV_PATH) as csv_file:
    data_reader = csv.reader(in_file)
    rows = csv.reader(csv_file, delimiter=',')
    next(rows)
    for row in rows:
        BoardLike.objects.create(member_id=row[0], is_like=row[1], board_id=row[2])
CSV_PATH = '.data/comments.csv'
with open(CSV_PATH) as csv_file:
    data_reader = csv.reader(csv_file)
    rows = csv.reader(csv_file, delimiter=',')
    next(rows)
    for row in rows:
        Comment.objects.create(content=row[0], created_at=row[1], board_id=row[2], self_comment_id=row[3], writer_id=row[4])
CSV_PATH = '.data/comment_likes.csv'
with open(CSV_PATH) as csv_file:
    data_reader = csv.reader(csv_file)
    rows = csv.reader(csv_file, delimiter=',')
    next(rows)
    for row in rows:
        CommentLike.objects.create(is_like=row[0], comment_id=row[1], member_id=row[2])