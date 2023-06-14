import discord
from discord import app_commands
import discord.ext
import json
from bot_utils import *
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


intents = discord.Intents.all()
client = MyClient(intents=intents)


def run_discord_bot():
    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')

    @client.tree.command()
    async def ping(interaction: discord.Interaction):
        await interaction.channel.send("pong")

    @client.tree.command()
    async def ola(interaction: discord.Interaction):
        """Diz Olá!"""
        await interaction.channel.send(f'Olá, {interaction.user.mention}')

    @client.tree.command()
    @app_commands.rename(text_to_send='texto')
    @app_commands.describe(text_to_send='Texto para enviar para o canal.')
    async def enviar(interaction: discord.Interaction, text_to_send: str):
        """Envia texto para o canal."""
        await interaction.channel.send(text_to_send)

    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

    with open(os.path.join(ROOT_DIR, 'config.json'), 'r') as json_file:
        config = json.load(json_file)

    MUTE_VOTE_TIME = config["MUTE_VOTE_TIME"]
    MIN_MUTE_VOTERS = config["MIN_MUTE_VOTERS"]  # should be 3
    MUTE_TIME = config["MUTE_TIME"]  # 10 mins

    muting_users = []
    muted_users = []

    @client.tree.command()
    @app_commands.rename(target_user='usuário')
    @app_commands.describe(target_user='Usuário que passará por votação para ser mutado.')
    async def mute(interaction: discord.Interaction, target_user: discord.Member):
        """Inicia uma votação para mutar um usuário."""
        if target_user in muting_users:
            await interaction.channel.send(
                f'Já há uma votação em andamento para mutar o usuário {target_user.mention}!')
            return
        elif target_user in muted_users:
            await interaction.channel.send(f'Usuário {target_user.mention} já está mutado!')
            return

        await interaction.channel.send(f'Uma votação para mutar o usuário {target_user.mention} foi iniciada.')
        muting_users.append(target_user)

        vote_passed = await take_vote(interaction,
                                      f'Mute {target_user.mention}?\n⚠ NOTE: Can\'t mute users with an equal or '
                                      f'higher role.',
                                      MUTE_VOTE_TIME, MIN_MUTE_VOTERS)
        muting_users.remove(target_user)

        if vote_passed:
            try:
                # Add to muted_users
                muted_users.append(target_user)
                # add temp. role for mute, edit role position to take precedence over other roles
                muted_role = await interaction.guild.create_role(name="Muted")
                await muted_role.edit(position=target_user.top_role.position + 1)

                # change channel permissions for new role
                for channel in interaction.guild.channels:
                    if type(channel) is discord.TextChannel and target_user in channel.members:
                        await channel.set_permissions(muted_role, read_messages=True, send_messages=False,
                                                      add_reactions=False)
                    elif type(channel) is discord.VoiceChannel:
                        await channel.set_permissions(muted_role, connect=False)

                # Give role to member
                await target_user.add_roles(muted_role)
                await interaction.channel.send(
                    "**{0}, a maioria decidiu que você deveria ser mutado.** Te vejo em {1} minutos!".format(
                        target_user.mention, int(MUTE_TIME / 60)))
                await asyncio.sleep(MUTE_TIME)
                await muted_role.delete()

                # Remove from muted_users
                muted_users.remove(target_user)
            except discord.ext.commands.errors.CommandInvokeError:
                # await error_admin_targeted(ctx)
                muted_users.remove(target_user)

    client.run(TOKEN)
