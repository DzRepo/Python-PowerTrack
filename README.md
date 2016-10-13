# Python library and sample application for working with [Gnip](www.gnip.com) Realtime PowerTrack 2.0 API
See:  the Support web site section on [Realtime PowerTrack 2.0](http://support.gnip.com/apis/powertrack2.0/)  for more information.
###Note: Requires [Requests](http://docs.python-requests.org/en/master/) library - to install: 
`pip install requests`
##RealtimePowerTrack.py
Library used to connect and process activities.

##PowerTrack20.py
Sample application that demonstrates how to use the library.
Edit the credentials in this file and execute the file to read data from your PowerTrack stream.

###Usage:
```
./PowerTrack20.py
```
Application will display a real-time view of statistics of Tweets being received based on the rules configured.  Note that the rules management portion of this library will be coming soon(tm)

##Feedback
Please send help requests / comments / complaints / chocolate to [@SteveDz](stevedz@twitter.com)

Note that this code is provide "As Is".  You should review and understand Python code, and be able to debug this code _on your own_ if used in a production environment.  See the License file for more legal limitations.
