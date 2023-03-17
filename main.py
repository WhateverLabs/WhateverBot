import os
from dotenv import load_dotenv
import random
import simplematrixbotlib as botlib
import requests

config = botlib.Config()
config.join_on_invite = False # Change for initial invites if needed
config.encryption_enabled = True
store_path = './crypt_storage/'
config.emoji_verify = True
config.ignore_unverified_devices = True

INSTANCE = os.getenv("INSTANCE")
NAME = os.getenv("USERNAME")
PW = os.getenv("PASSWORD")
creds = botlib.Creds(INSTANCE, NAME, PW)
bot = botlib.Bot(creds, config)
PREFIX = 'whatever '

UPTIME_KEY = os.getenv("UPTIME_KEY")


@bot.listener.on_message_event
async def echo(room, message):
    match = botlib.MessageMatch(room, message, bot, PREFIX)
    if match.is_not_from_this_bot()\
            and match.prefix()\
            and match.command("help"):

        await bot.api.send_markdown_message(room.room_id, "**Command List:** \n"
                                            "- hello/hi\n"
                                            "- status\n"
                                            "- instances\n"
                                            "- ping"
                                            )
    if match.is_not_from_this_bot()\
            and match.prefix()\
            and match.command("hello") or match.command("hi"):

        await bot.api.send_markdown_message(room.room_id, "👋")
    elif match.is_not_from_this_bot()\
            and match.prefix()\
            and match.command("ping"):
        replyList = ["eat shit", "stfu", "ping dn", "\"whatever ping\" -🤓"]
        await bot.api.send_markdown_message(room.room_id, random.choice(replyList))
    elif match.is_not_from_this_bot()\
            and match.prefix()\
            and match.command("status"):
        try:
            ENDPOINT = 'https://betteruptime.com//api/v2/monitors'
            headers = {
                'Authorization': f'Bearer {UPTIME_KEY}'
            }

            response = requests.get(ENDPOINT, headers=headers)
            if response.status_code == 200:
                monitorData = response.json()["data"]
                downMonitors = []
                for monitor in monitorData:
                    if (f"{monitor['attributes']['status']}") != 'up':
                        downMonitors.append(f"{monitor['attributes']['pronounceable_name']} is {monitor['attributes']['status']}")
                if len(downMonitors) > 0:
                    await bot.api.send_text_message(room.room_id, "The following instances are affected: " + '\n'.join(downMonitors) + "\nAll other instances should be up")
                else:
                    await bot.api.send_text_message(room.room_id, "All Whatever instances seem to be online, it may be an issue on your end")
            else:
                await bot.api.send_text_message(room.room_id, "Welp, I couldn't reach the monitor servers")
        except Exception as error:
            print(f"Error getting answer: {error}")
    elif match.is_not_from_this_bot()\
            and match.prefix()\
            and match.command("instances"):
        try:
            ENDPOINT = 'https://betteruptime.com//api/v2/monitors'
            headers = {
                'Authorization': f'Bearer {UPTIME_KEY}'
            }

            response = requests.get(ENDPOINT, headers=headers)
            if response.status_code == 200:
                instanceData = response.json()["data"]
                outage = False
                for instance in instanceData:
                    if (f"{instance['attributes']['status']}") != 'up':
                        outage = True
                        break
                if outage == False:
                    await bot.api.send_markdown_message(room.room_id, "Here's the full list of Whatever's instances: \n\n"
                    "- [AnonymousOverflow](https://code.whateversocial): A frontend for StackOverflow developed by Whatever's http.james\n"
                    "- [Dumb](https://sing.whatever.social): A frontend for Genius\n"
                    "- [Hyperpipe](https://listen.whatever.social): A frontend for YouTube Music\n"
                    "- [Libreddit](https://discuss.whatever.social): A frontend for Reddit\n"
                    "- [Nitter](https://read.whatever.social): A frontend for Twitter\n"
                    "- [Piped](https://watch.whatever.social): A frontend for YouTube\n"
                    "- [ProxiTok](https://cringe.whatever.social): A frontend for... TikTok\n\n"
                    "All systems seem to be up and running")
                else:
                    await bot.api.send_markdown_message(room.room_id, "Here's the full list of Whatever's instances: \n\n"
                    "- [AnonymousOverflow](https://code.whateversocial): A frontend for StackOverflow developed by Whatever's http.james\n"
                    "- [Dumb](https://sing.whatever.social): A frontend for Genius\n"
                    "- [Hyperpipe](https://listen.whatever.social): A frontend for YouTube Music\n"
                    "- [Libreddit](https://discuss.whatever.social): A frontend for Reddit\n"
                    "- [Nitter](https://read.whatever.social): A frontend for Twitter\n"
                    "- [Piped](https://watch.whatever.social): A frontend for YouTube\n"
                    "- [ProxiTok](https://cringe.whatever.social): A frontend for... TikTok\n\n"
                    "Some instances seem to be down, run \'whatever status\' to view them")
            else:
                await bot.api.send_text_message(room.room_id, "Welp, I couldn't reach the monitor servers")
        except Exception as error:
            print(f"Error getting answer: {error}")
            await bot.api.send_text_message(room.room_id, "Welp that's awkward, something went wrong")


bot.run()
