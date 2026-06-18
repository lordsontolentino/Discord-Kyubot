import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = commands.Bot(command_prefix = '!', status=discord.Status.online, activity=discord.Game('Imong mama'), intents=discord.Intents.all())
players = {}

@client.event
async def on_ready():
    print('Bot is running.')

class Menu(discord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=1800)
        self.value = None
        self.ctx = ctx

    @discord.ui.button(label= "@Jimmy", style=discord.ButtonStyle.green)
    async def menu1(self, interaction: discord.Interaction, button: discord.ui.Button):
        channel_players = players.setdefault(interaction.channel_id, [])
        if interaction.user.mention not in channel_players and len(channel_players) < 5:
            channel_players.append(interaction.user.mention)    

        if len(channel_players) == 5:
            player_names = ", ".join(channel_players)

            self.clear_items()
            await interaction.response.edit_message(view=self, content=f"{player_names}\n{len(channel_players)}/5\nQueue full")
            channel_players.clear()
            self.stop()

            return

        player_names = ", ".join(channel_players)          

        await interaction.response.edit_message(content = f"{player_names}\n{len(channel_players)}/5" if player_names else f"{len(channel_players)}/5")       

    @discord.ui.button(label= "Leave", style=discord.ButtonStyle.red)
    async def menu2(self, interaction: discord.Interaction, button: discord.ui.Button):
        channel_players = players.setdefault(interaction.channel_id, [])
        player_names = ''
        if interaction.user.mention in channel_players:
            channel_players.remove(interaction.user.mention)

        player_names = ", ".join(channel_players)

        await interaction.response.edit_message(content = f"{player_names}\n{len(channel_players)}/5" if player_names else f"{len(channel_players)}/5")

    @discord.ui.button(label= "Finish", style=discord.ButtonStyle.blurple)
    async def menu3(self, interaction: discord.Interaction, button: discord.ui.Button):
        channel_players = players.setdefault(interaction.channel_id, [])
        player_names = ", ".join(channel_players)

        if interaction.user == self.ctx.author:
            self.clear_items()
            await interaction.response.edit_message(view=self, content=f"{player_names}\n{len(channel_players)}/5\nQueue finished")
            channel_players.clear()
            self.stop()

    @discord.ui.button(label= "Cancel", style=discord.ButtonStyle.gray)
    async def menu4(self, interaction: discord.Interaction, button: discord.ui.Button):
        channel_players = players.setdefault(interaction.channel_id, [])
        if interaction.user == self.ctx.author:
            self.clear_items()
            await interaction.response.edit_message(view=self, content=f"Queue cancelled")
            channel_players.clear()
            self.stop()

    async def on_timeout(self):
        channel_players = players.setdefault(self.ctx.channel.id, [])
        channel_players.clear()
        self.clear_items()
        await self.message.edit(view=self, content="Queue timed out")

@client.command()
async def q(ctx):
    if len(players.get(ctx.channel.id, [])) == 0:
        view = Menu(ctx)
        view.message = await ctx.reply(view=view)
    else:
        await ctx.reply('Queue in progress')

client.run(TOKEN)