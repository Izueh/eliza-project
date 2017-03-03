import re
import random

def reply(human): 
	generic_replies = [ "Show me where he touched you.", "I see.", "I understand.", "Go on.", "How does that make you feel?" ]
	rand = random.randint(0, len(generic_replies) - 1)
	reply = generic_replies[rand]

	hello_reply = "Hello. How are you feeling?"
	hello_regex = re.compile('(hello)|(hi)|(hey)', re.I)

	whatup_reply = "All good homie. How you hangin'?"
	whatup_regex = re.compile('(what.*up\?*$)', re.I)

	feelingGood_reply = "That's good to hear."
	feelingGood_regex = re.compile('(fine)|(good)|(well)|(splendid)|(great)|(never better)|(happy)|(jolly)|(fun)|(ok)|(perfect)', re.I)

	feelingBad_reply = "Oh dear. Are you taking your medication?"
	feelingBad_regex = re.compile('(bad)|(not good)|(not well)|(terrible)|(awful)|(sad)|(could be better)|(angry)|(unhappy)|(depressed)', re.I)

	iam_reply = "Why are you " 
	iam_regex = re.compile('i am (\w+)', re.I)


	if hello_regex.search(human):
		reply = hello_reply	
	elif whatup_regex.search(human):
		reply = whatup_reply
	elif feelingGood_regex.search(human):
		reply = feelingGood_reply
	elif feelingBad_regex.search(human):
		reply = feelingBad_reply
	elif iam_regex.search(human):
		reply = iam_reply + re.group(1)

	return reply
