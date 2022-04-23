import discord
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive

client = discord.Client()

if "sad_words" not in db.keys():
  db["sad_words"] = True 

if "leave_words" not in db.keys():
  db["leave_words"] = True

if "sad_responses" not in db.keys(): 
  db["sad_responses"] = True 

if "leave_responses" not in db.keys(): 
  db["leave_responses"] = True 

# FUNCTION DEFINITION: returns quote from the Zenquotes.io API
def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]["q"] + " -" + json_data[0]["a"]
  return(quote)

# FUNCTION DEFINITION: assigns new phrase to the sad_responses
def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [encouraging_message]

# FUNCTION DEFINITION: deletes a response 
def delete_encouragment(index):
  encouragements = db["encouragements"]
  if len(encouragements) > index:
    del encouragements[index]
    db["encouragements"] = encouragements

@client.event
async def on_ready():
  print("We have logged in as {0.user}".format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content

  # If message starts with b$hello, bot returns 'Hello!'.
  if msg.startswith("b$hello"): 
    await message.channel.send("Hello!")

  # If message starts with b$inspire, bot returns a quote.
  if msg.startswith("b$inspire"):
    quote = get_quote()
    await message.channel.send(quote)

  # If message contains a tigger from sad_words, bot returns a sad_response. 
  if db["responses"]: 
    options = starter_encouragements

    if "encouragements" in db.keys():
      options = options + db["encouragements"].value

    if any(word in msg for word in sad_words):
      await message.channel.send(random.choice(options))

  if any(word in msg for word in leave_words):
    await message.channel.send(random.choice(leave_encouragements))

  # If message contains a tigger from sad_words, bot returns a sad_response. 
  if db["responses"]: 
    options = starter_encouragements

    if "encouragements" in db.keys():
      options = options + db["encouragements"].value

    if any(word in msg for word in sad_words):
      await message.channel.send(random.choice(options))

  if any(word in msg for word in leave_words):
    await message.channel.send(random.choice(leave_encouragements))

  # If message starts with b$sadd, bot will add a new word to sad_words. 
  if msg.startswith("b$add"):
    encouraging_message = msg.split("b$add ",1)[1]
    update_encouragements(encouraging_message)
    await message.channel.send("New encouraging message added.")

  # If message starts with b$ladd, bot will add a new word to leave_words. 
  if msg.startswith("b$add"):
    encouraging_message = msg.split("b$add ",1)[1]
    update_encouragements(encouraging_message)
    await message.channel.send("New encouraging message added.")

  # If message starts with b$sdel, bot will delete a matching words from sad_words. 
  if msg.startswith("b$del"):
    encouragements = []
    if "encouragements" in db.keys():
      index = int(msg.split("b$del",1)[1])
      delete_encouragment(index)
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)

  # If message starts with b$ldel, a new word will be deleted from leave_words. 
  if msg.startswith("b$del"):
    encouragements = []
    if "encouragements" in db.keys():
      index = int(msg.split("b$del",1)[1])
      delete_encouragment(index)
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)

  # If message starts with b$slist, 
  if msg.startswith("b$list"): 
    encouragements = []
    if "encouragements" in db.keys(): 
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)

  if msg.startswith("b$responses"): 
    value = msg.split("b$responses ",1)[1]

    if value.lower() == "true": 
      db["responses"] = True 
      await message.channel.send("responses is on.")
    else: 
      db["responses"] = False 
      await message.channel.send("responses is off.")

keep_alive()
client.run(os.getenv("token"))