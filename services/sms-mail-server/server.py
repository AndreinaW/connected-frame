import pytextbelt
import sys

user_settings = "user.settings"
settings = []

with open(user_settings, 'r') as ustg:
	for line in ustg:
		if line[0] != '#':
			words = line.strip().split('=')
			settings.append(words[1])

phone = settings[0]
region = settings[1]
message = settings[2]

print("Config: phone=" + phone + "; region=" + region + "; message=\"" + message + "\"")

recipient = pytextbelt.Textbelt.Recipient(phone, region)
response = recipient.send(message)

print(response)

#if response["success"]:
#	print("Successfully sent message to" + phone + " (" + region + ")")
#else:
#	print("Sending to" + phone + " (" + region + ") failed!")

