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


def run_discord_bot():
    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')

    @client.tree.command()
    async def ping(interaction: discord.Interaction):
        await interaction.response.send_message("pong")

    @client.tree.command()
    async def ola(interaction: discord.Interaction):
        """Diz Olá!"""
        await interaction.response.send_message(f'Olá, {interaction.user.mention}')

    @client.tree.command()
    @app_commands.rename(text_to_send='texto')
    @app_commands.describe(text_to_send='Texto para enviar para o canal.')
    async def enviar(interaction: discord.Interaction, text_to_send: str):
        """Envia texto para o canal."""
        await interaction.response.send_message(text_to_send)

    @client.tree.command()
    @app_commands.rename(target_user='usuário')
    @app_commands.describe(target_user='Usuário que passará por votação para ser mutado.')
    async def mute(interaction: discord.Interaction, target_user: discord.Member):
        """Inicia uma votação para mutar um usuário."""
        await interaction.response.send_message(f'Uma votação para mutar o usuário {target_user} foi iniciada.')

        # await require_lower_permissions(ctx, target_user, bot)

        # if target_user in muting_users:
        #     await ctx.send("There is already a mute vote on `{}`!".format(target_user))
        #     return
        # elif target_user in muted_users:
        #     await ctx.send("`{}` is already muted!".format(target_user))
        #     return
        #
        # muting_users.append(target_user)
        # vote_passed = await take_vote(ctx, "Mute `{}`?\n⚠ NOTE: Can't mute users with an equal or higher role.".format(
        #     target_user), MUTE_VOTE_TIME, MIN_MUTE_VOTERS)
        # muting_users.remove(target_user)
        #
        # if vote_passed:
        #     try:
        #         # Add to muted_users
        #         muted_users.append(target_user)
        #         # add temp. role for mute, edit role position to take precedence over other roles
        #         muted_role = await ctx.guild.create_role(name="Muted")
        #         await muted_role.edit(position=ctx.guild.get_member(target_user.id).top_role.position + 1)
        #
        #         # change channel permissions for new role
        #         for channel in ctx.guild.channels:
        #             if type(channel) is discord.TextChannel and target_user in channel.members:
        #                 await channel.set_permissions(muted_role, read_messages=True, send_messages=False,
        #                                               add_reactions=False)
        #
        #             elif type(channel) is discord.VoiceChannel:
        #                 await channel.set_permissions(muted_role, connect=False)
        #
        #         # Give role to member
        #         await ctx.guild.get_member(target_user.id).add_roles(muted_role)
        #         await ctx.send(
        #             "**{0}, the majority has ruled that you should be muted.** See ya in {1} minutes!".format(
        #                 target_user, int(MUTE_TIME / 60)))
        #         await asyncio.sleep(MUTE_TIME)
        #         await muted_role.delete()
        #
        #         # Remove from muted_users
        #         muted_users.remove(target_user)
        #     except discord.ext.commands.errors.CommandInvokeError:
        #         await error_admin_targeted(ctx)
        #         muted_users.remove(target_user)


    client.run(TOKEN)
