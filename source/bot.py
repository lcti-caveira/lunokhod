import os
import random

import discord.ext
from bot_utils import *
from discord import app_commands

TOKEN = os.environ['DISCORD_TOKEN']
MY_GUILD = discord.Object(id=1102693205662773258)  # ID do servidor LCTI

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(ROOT_DIR, 'config.json'), 'r') as json_file:
    config = json.load(json_file)

with open(os.path.join(ROOT_DIR, 'status.json'), 'r', encoding='utf-8') as file:
    statuses = json.load(file)

# TODO: MIN_MUTE_VOTERS, MIN_KICK_VOTERS, BAN_VOTE_TIME should be calculated instead of a constant (eg. 50% +1)
MUTE_VOTE_TIME = config["MUTE_VOTE_TIME"]
KICK_VOTE_TIME = config["KICK_VOTE_TIME"]
BAN_VOTE_TIME = config["BAN_VOTE_TIME"]

MIN_MUTE_VOTERS = config["MIN_MUTE_VOTERS"]
MIN_KICK_VOTERS = config["MIN_KICK_VOTERS"]
MIN_BAN_VOTERS = config["MIN_BAN_VOTERS"]

MUTE_TIME = config["MUTE_TIME"]
ANONYMOUS_MESSAGES_MUTE_TIME = config["ANONYMOUS_MESSAGES_MUTE_TIME"]
NOTION_URL = config["NOTION_URL"]

muting_users = []
kicking_users = []
banning_users = []
muted_users = []
anonymous_messages_users = []

STATUS_LOOP = config["STATUS_LOOP"]


class Client(discord.Client):
    def __init__(self, *, intents_local: discord.Intents):
        super().__init__(intents=intents_local)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)


intents = discord.Intents.all()
client = Client(intents_local=intents)


def run_discord_bot():
    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')
        # await asyncio.sleep(300)
        client.loop.create_task(status_loop())

    @client.tree.command()
    async def ping(interaction: discord.Interaction):
        # noinspection PyUnresolvedReferences
        await interaction.response.send_message("pong")

    @client.tree.command()
    async def ola(interaction: discord.Interaction):
        """Diz Olá!"""
        # noinspection PyUnresolvedReferences
        await interaction.response.send_message(f'Olá, {interaction.user.mention}')

    @client.tree.command()
    @app_commands.rename(text_to_send='texto')
    @app_commands.describe(text_to_send='Texto para enviar para o canal.')
    async def enviar(interaction: discord.Interaction, text_to_send: str):
        """Envia texto para o canal."""
        # noinspection PyUnresolvedReferences
        await interaction.response.send_message(text_to_send)

    @client.tree.command()
    @app_commands.rename(text_to_send='texto')
    @app_commands.describe(text_to_send='Texto para enviar para o canal de moderadores de forma anônima.')
    async def anonimo(interaction: discord.Interaction, text_to_send: str):
        """Envia texto para canal de moderadores de forma anônima."""
        if discord.Interaction.user in anonymous_messages_users:
            # noinspection PyUnresolvedReferences
            await interaction.response.send_message(
                f'Você já enviou uma mensagem anônima nas últimas 3 horas... Aguarde e tente novamente!',
                ephemeral=True)
            return

        # noinspection PyUnresolvedReferences
        await interaction.response.send_message('Mensagem anônima enviada aos moderadores 🕵️. Aguarde 3 '
                                                'horas para enviar outra.', ephemeral=True)

        anonymous_messages_users.append(discord.Interaction.user)
        channel_name = '🥀mensagens-anonimas'
        existing_channel = discord.utils.get(
            interaction.guild.channels, name=channel_name)
        if not existing_channel:
            print(f'Creating a new channel: {channel_name}')
            await interaction.guild.create_text_channel(name=channel_name)

        channel = client.get_channel(discord.utils.get(
            interaction.guild.channels, name=channel_name).id)
        await channel.send(text_to_send)

        await asyncio.sleep(ANONYMOUS_MESSAGES_MUTE_TIME)
        # Remove from muted_users
        anonymous_messages_users.remove(discord.Interaction.user)

    @client.tree.command(name='vote-mute')
    @app_commands.rename(target_user='usuário')
    @app_commands.describe(target_user='Usuário que passará por votação para ser mutado.')
    async def mute(interaction: discord.Interaction, target_user: discord.Member):
        """Inicia uma votação para mutar um usuário."""
        if target_user in muting_users:
            # noinspection PyUnresolvedReferences
            await interaction.response.send_message(
                f'Já há uma votação em andamento para mutar o usuário {target_user.mention}!')
            return
        elif target_user in muted_users:
            # noinspection PyUnresolvedReferences
            await interaction.response.send_message(f'Usuário {target_user.mention} já está mutado!')
            return

        # noinspection PyUnresolvedReferences
        await interaction.response.send_message(f'Uma votação para mutar o usuário {target_user.mention} foi iniciada.')
        muting_users.append(target_user)

        vote_passed = await take_vote(interaction,
                                      f'Mutar {target_user.mention}?\n⚠ INFO: Não posso mutar usuários com uma '
                                      f'role maior que a minha.',
                                      MUTE_VOTE_TIME, MIN_MUTE_VOTERS)
        muting_users.remove(target_user)

        if vote_passed:
            try:
                # Add to muted_users
                muted_users.append(target_user)

                # Add temporary role for mute, edit role position to take precedence over other roles
                # TODO: display_icon='😶' if the discord server has enough boosts
                muted_role = await interaction.guild.create_role(name="Muted", colour=discord.Colour.darker_grey())
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
                await interaction.channel.send(f'**{target_user.mention}, a maioria decidiu que você deveria ser '
                                               f'mutado...** Te vejo em {int(MUTE_TIME / 60)} minutos!')
                await asyncio.sleep(MUTE_TIME)
                await muted_role.delete()

                # Remove from muted_users
                muted_users.remove(target_user)
            except discord.ext.commands.errors.CommandInvokeError:
                muted_users.remove(target_user)

    @client.tree.command(name='vote-kick')
    @app_commands.rename(target_user='usuário')
    @app_commands.describe(target_user='Usuário que passará por votação para ser kickado.')
    async def kick(interaction: discord.Interaction, target_user: discord.Member):
        """Inicia uma votação para kickar um usuário."""

        if target_user in kicking_users:
            # noinspection PyUnresolvedReferences
            await interaction.response.send_message(f'Já existe uma votação em andamento para '
                                                    f'kickar {target_user.mention}!')
            return

        # noinspection PyUnresolvedReferences
        await interaction.response.send_message(f'Uma votação para kickar o usuário {target_user.mention}'
                                                f' foi iniciada.')
        # add to kicking_users
        kicking_users.append(target_user)

        vote_passed = await take_vote(interaction, f'Kickar {target_user.mention}?\n⚠ INFO: Não posso kickar '
                                                   f'usuários com uma role maior ou igual a minha.',
                                      KICK_VOTE_TIME, MIN_KICK_VOTERS)

        if vote_passed:
            try:
                await interaction.guild.kick(target_user, reason='Votado para ser kickado')
                # noinspection PyUnresolvedReferences
                await interaction.response.send_message(f'👢 Kickado: {target_user.mention}.')
            except discord.ext.commands.errors.CommandInvokeError:
                # noinspection PyUnresolvedReferences
                await interaction.response.send_message('Ops! Algo de errado aconteceu...')

        kicking_users.remove(target_user)

    @client.tree.command(name='vote-ban')
    @app_commands.rename(target_user='usuário')
    @app_commands.describe(target_user='Usuário que passará por votação para ser banido.')
    async def ban(interaction: discord.Interaction, target_user: discord.Member):
        """Inicia uma votação para banir um usuário."""

        if target_user in banning_users:
            # noinspection PyUnresolvedReferences
            await interaction.response.send_message(f'Já existe uma votação em andamento para '
                                                    f'banir {target_user.mention}!')
            return

        # noinspection PyUnresolvedReferences
        await interaction.response.send_message(f'Uma votação para banir o usuário {target_user.mention}'
                                                f' foi iniciada.')
        # add to banning_users
        banning_users.append(target_user)

        vote_passed = await take_vote(interaction,
                                      f'Banir {target_user.mention}?\n⚠ INFO:Não posso banir '
                                      f'usuários com role igual ou maior que a minha.',
                                      BAN_VOTE_TIME,
                                      MIN_BAN_VOTERS)

        if vote_passed:
            try:
                await interaction.guild.ban(target_user, reason='Votado para ser banido')
                # noinspection PyUnresolvedReferences
                await interaction.response.send_message(f'🦀🦀 {target_user.mention} SE FOI 🦀🦀')
            except discord.ext.commands.errors.CommandInvokeError:
                # noinspection PyUnresolvedReferences
                await interaction.response.send_message('Ops! Algo de errado aconteceu...')

        banning_users.remove(target_user)

    @client.tree.command(name='gatinho')
    async def cat(interaction: discord.Interaction):
        """Responde com um gatinho aleatório."""
        api_url = 'https://api.thecatapi.com/v1/images/search'
        msg = f'{interaction.user.mention}, aqui está o seu gatinho aleatório:'
        await get_random_animal(interaction, api_url, msg)

    @client.tree.command(name='doguinho')
    async def dog(interaction: discord.Interaction):
        """Responde com um doguinho aleatório."""
        api_url = 'https://api.thedogapi.com/v1/images/search'
        msg = f'{interaction.user.mention}, aqui está o seu doguinho aleatório:'
        await get_random_animal(interaction, api_url, msg)

    @client.tree.command(name='infos', description='Responde com informações do servidor.')
    async def infos(interaction: discord.Interaction):
        """Responde com informações do servidor."""
        # noinspection PyUnresolvedReferences
        await interaction.response.send_message(f'Nome do servidor: {interaction.guild.name}\n'
                                                f'Número de membros: {interaction.guild.member_count}\n'
                                                f'Apoie esse bot e outras iniciativas do LCTI: {NOTION_URL}')

    async def status_loop():
        while True:
            status = random.choice(statuses)
            await client.change_presence(
                activity=discord.Game(
                    name=status.format(len(client.guilds)))
            )
            await asyncio.sleep(STATUS_LOOP)

    client.run(TOKEN)
