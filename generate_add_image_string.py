#!/opt/local/bin/python

if __name__ == '__main__':

	print '==========[ Enter image properties: ]=========='
	artist = raw_input ("Artist: ")
	description = raw_input ("Description: ")
	url = raw_input ("URL: ")

	print '/add_image?artist=' + artist + '&description=' + description + '&URL=' + url
	

