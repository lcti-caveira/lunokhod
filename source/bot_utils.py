import discord
import requests
import json
import asyncio
import random


async def take_vote(interaction: discord.Interaction, question: str, vote_time, min_voters) -> bool:
    """
    take_vote(interaction: discord.Interaction, question:str, vote_time, min_voters) - Collects votes
    interaction: pass from command function
    question: what to ask
    vote_time: minimum vote time
    min_voters: minimum voters count

    returns [If vote passed].
    """

    embed_title = "NEW VOTE"
    vote_message = await interaction.channel.send(
        embed=discord.Embed(
            type="rich",
            title=embed_title,
            # description="{}\n\n✅ - Yes\n\n❌ - No".format(question)
            description="{0}\n\n✅ - Yes\n❌ - No\nMinimum {1} votes required.".format(question, min_voters)
        )
    )

    await vote_message.add_reaction('✅')
    await vote_message.add_reaction('❌')

    passed = False
    curr_time = 0
    while curr_time < vote_time:
        await asyncio.sleep(5)
        all_in_favor = 0
        not_in_favor = 0
        finished_vote = await vote_message.channel.fetch_message(vote_message.id)
        for reaction in finished_vote.reactions:
            if str(reaction.emoji) == '✅':
                all_in_favor += reaction.count - 1  # don't include bot's reaction
            elif str(reaction.emoji) == '❌':
                not_in_favor += reaction.count - 1

        if all_in_favor > not_in_favor and all_in_favor >= min_voters:
            passed = True
            break

        await asyncio.sleep(5)
        curr_time += 5

    question += "\nVERDICT: **Vote passed!**" if passed else "\nVERDICT: **Vote failed!**"

    await vote_message.edit(embed=discord.Embed(
        type="rich",
        title=embed_title,
        description=question
    ))
    return passed


async def get_random_animal(interaction: discord.Interaction, api_url: str, msg: str):
    """
        get_random_animal(interaction: discord.Interaction, api_url: str, msg: str) -
        Gets a random animal depending on the API URL and responds with a message

        interaction: pass from command function
        api_url: the API Url
        msg: message to send to the channel
        """
    response = requests.get(api_url)
    if response.status_code == 200:
        data = json.loads(response.text)

        # Extract the 'url' field from the response
        if data:
            img_url = data[0].get('url', '')
            # noinspection PyUnresolvedReferences
            await interaction.response.send_message(content=msg,
                                                    embed=discord.Embed(
                                                        color=random.randint(0, 16777215)).set_image(url=img_url)
                                                    )
