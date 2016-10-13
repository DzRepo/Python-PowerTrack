
import requests
import json
import sys
import base64


activity_callback = None
error_callback = None

error_count = 0


def log_error(ex, description):
	if error_callback is not None:
		error_callback(ex, description)
	else:
		print "Error:", description
		print "Exception:", str(ex)
		print 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno)


def process_activity(activity):
	global activity_callback
	if activity_callback is None:
		print(activity)
	else:
		activity_callback(activity)


def generate_headers(username, password):
	try:
		# Note the removal of the last character of credentials to strip off newline character
		# that gets generated for no good reason whatsoever.
		encoded_credentials = base64.encodestring('%s:%s' % (username, password))[:-1]
		headers = {'Accept': 'application/json',
					'Connection': 'Keep-Alive',
					'Accept-Encoding': 'gzip',
					'Authorization': 'Basic %s' % encoded_credentials}
		return headers
	except Exception as e:
		log_error(e, "Error in stream configuration")
		exit()


def start_stream(username, password, url):
	global error_count
	stay_connected = True

	while stay_connected:
		try:
			headers = generate_headers(username, password)
			r = requests.get(url, stream=True, headers=headers)

			for line in r.iter_lines():
				try:
					if line:
						process_activity(json.loads(line))
				except Exception as iex:
					log_error(iex,"Message Exception")
		except Exception as ex:
			log_error(ex, "Stream Exception")



def set_activity_callback(callback):
	global activity_callback
	activity_callback = callback


def set_error_callback(callback):
	global error_callback
	error_callback = callback


