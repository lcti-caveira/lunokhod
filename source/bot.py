import discord
from discord import app_commands
import discord.ext
import responses
import os

TOKEN = os.environ['DISCORD_TOKEN']
MY_GUILD = discord.Object(id=1102693205662773258)  # ID do servidor LCTI


class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)


intents = discord.Intents.default()
client = MyClient(intents=intents)

# async def send_message(message, user_message, is_private):
#     try:
#         response = responses.handle_response(user_message)
#         await message.author.send(response) if is_private else await message.channel.send(response)
#     except Exception as e:
#         print(e)


def run_discord_bot():

    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')

    @client.tree.command()
    async def ping(interaction: discord.Interaction):
        await interaction.response.send_message("pong")

    @client.tree.command()
    async def hello(interaction: discord.Interaction):
        """Diz Olá!"""
        await interaction.response.send_message(f'Olá, {interaction.user.mention}')

    @client.tree.command()
    @app_commands.rename(text_to_send='texto')
    @app_commands.describe(text_to_send='Texto para enviar para o canal.')
    async def send(interaction: discord.Interaction, text_to_send: str):
        """Envia texto para o canal."""
        await interaction.response.send_message(text_to_send)

    client.run(TOKEN)
