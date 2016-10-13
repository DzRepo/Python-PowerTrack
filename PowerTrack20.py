#!/usr/bin/env python
import RealtimePowerTrack
import time
import os
import sys
import locale

username = "USERNAME"
password = "PASSWORD"
account = "ACCOUNTNAME"
label = "LABEL"  # usually prod or dev

records_read = 0
long_records = 0
retweets = 0
replies = 0
quotes = 0
posts = 0
hashtags = 0
urls = 0
user_mentions = 0
symbols = 0

error_count = 0
error_limit = 100

tweet_date_format = '%Y-%m-%dT%H:%M:%S.%fZ'
str_format = '{:>8}'


def print_at(x=0, y=0, print_string=""):
	x = int(x)
	y = int(y)
	if x >= 255: x = 255
	if y >= 255: y = 255
	if x <= 0: x = 0
	if y <= 0: y = 0
	VERT = str(x)
	HORIZ = str(y)
	print("\033[" + VERT + ";" + HORIZ + "f" + str(print_string))


def clear():
	os.system('cls' if os.name == 'nt' else 'clear')


def print_labels():
	clear()
	data_column = 1
	data_row = 4
	print "PowerTrack Stream Processor"
	print_at(data_row, data_column, "Activities")
	data_row += 1
	print_at(data_row, data_column, "Retweets")
	data_row += 1
	print_at(data_row, data_column, "Long Tweets")
	data_row += 1
	print_at(data_row, data_column, "Replies")
	data_row += 1
	print_at(data_row, data_column, "Quote Tweets")
	data_row += 1
	print_at(data_row, data_column, "Posts")
	data_row += 1
	print_at(data_row, data_column, "Hashtags")
	data_row += 1
	print_at(data_row, data_column, "Urls")
	data_row += 1
	print_at(data_row, data_column, "User Mentions")
	data_row += 1
	print_at(data_row, data_column, "Symbols")


def format_int(num):
	return str_format.format(locale.format('%d', num, grouping=True))


def process_activity(activity):
	global records_read, long_records, retweets, replies, quotes, posts, hashtags, urls, user_mentions, symbols
	records_read += 1

	# if it's a "more with 140" Tweet, get the data from the long_object, otherwise, from the root object
	if "long_object" in activity:
		long_records += 1
		hashtags += len(activity["long_object"]["twitter_entities"]["hashtags"])
		urls += len(activity["long_object"]["twitter_entities"]["urls"])
		user_mentions += len(activity["long_object"]["twitter_entities"]["user_mentions"])
		symbols += len(activity["long_object"]["twitter_entities"]["symbols"])
	else:
		hashtags += len(activity["twitter_entities"]["hashtags"])
		urls += len(activity["twitter_entities"]["urls"])
		user_mentions += len(activity["twitter_entities"]["user_mentions"])
		symbols += len(activity["twitter_entities"]["symbols"])

	if activity["verb"] == "share":
		retweets += 1

	if "inReplyTo" in activity:
		replies += 1

	if activity["verb"] == "post":
		posts += 1
		if "twitter_quoted_status" in activity:
			quotes += 1


	data_column = 15
	data_row = 4

	print_at(data_row, data_column, format_int(records_read))
	data_row += 1
	print_at(data_row, data_column, format_int(retweets))
	data_row += 1
	print_at(data_row, data_column, format_int(long_records))
	data_row += 1
	print_at(data_row, data_column, format_int(replies))
	data_row += 1
	print_at(data_row, data_column, format_int(quotes))
	data_row += 1
	print_at(data_row, data_column, format_int(posts))
	data_row += 1
	print_at(data_row, data_column, format_int(hashtags))
	data_row += 1
	print_at(data_row, data_column, format_int(urls))
	data_row += 1
	print_at(data_row, data_column, format_int(user_mentions))
	data_row += 1
	print_at(data_row, data_column, format_int(symbols))


def handle_error(ex, description = None):
	global error_count
	error_count += 1

	print_at(20, 0, " ")
	print " "
	print "----------------------------------------------------------------------------"
	if ex is not None:
		print "Error # ", str(error_count), ":", str(ex)
	if description is not None:
		print "Description:", description
	print "----------------------------------------------------------------------------"
	print " "
	if error_count > error_limit:
		sys.exit(2)


if __name__ == "__main__":

	locale.setlocale(locale.LC_ALL, 'en_US')

	try:
		clear()
		print_labels()

		url = "https://gnip-stream.twitter.com/stream/powertrack/accounts/" + account + \
				"/publishers/twitter/" + label + ".json"

		print_at (3, 1, "Stream URL:" + url)
		RealtimePowerTrack.set_activity_callback(process_activity)
		RealtimePowerTrack.set_error_callback(handle_error)

		connection_count = 0
		keep_connected = True
		while keep_connected:
			connection_count += 1
			try:
				RealtimePowerTrack.start_stream(username, password, url)
			except Exception as ex:
				handle_error(ex)

			if connection_count < 10:
				print_at(25, 1, "Stream restarting in 2 seconds.")
				time.sleep(2)
				print_at(25, 1, "                                ")

			else:
				keep_connected = False
	except KeyboardInterrupt as ex:
		handle_error(ex, "Manually stopped")
