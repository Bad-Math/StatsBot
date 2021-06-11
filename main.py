import os
import discord

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("$keywords"):
        parameters = message.content[10:].split(
        )  #start the parameter string on 8th character
        user_id = int(parameters[0][3:-1])
        keywords = parameters[1:]

        print("generating report for " + str(user_id))

        data = [0 for key in keywords]

        messages = await message.channel.history(limit=None).flatten()

        total_mssgs_by_author = 0

        for past_mssg in messages:
            if past_mssg.author.id == user_id:
                total_mssgs_by_author += 1
                for i in range(len(keywords)):
                    if past_mssg.content.find(keywords[i]) > -1:
                        data[i] += 1

        report_message = parameters[0] + ": \n"
        for i in range(len(keywords)):
            count = data[i]
            percent = round(100 * count / total_mssgs_by_author, 1)
            report_message += " has sent a message with word " + keywords[
                i] + " " + str(
                    count) + " times. This word is present in " + str(
                        percent) + "% of their messages.\n"

        await message.channel.send(report_message)

    # if message.content.startswith('$hello'):
    #     await message.channel.send('Hello!')


client.run(os.getenv('TOKEN'))
