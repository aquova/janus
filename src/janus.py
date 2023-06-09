import discord

import json

from commonbot.timestamp import calculate_timestamps

CONFIG_PATH = "private/config.json"
with open(CONFIG_PATH) as config_file:
    cfg = json.load(config_file)

class DiscordClient(discord.Client):
    def __init__(self) -> None:
        super().__init__(intents=discord.Intents.default())
        self.tree = discord.app_commands.CommandTree(self)

    async def on_ready(self):
        print(f"Logged in as {str(self.user)} ID: {self.user.id}")

    async def on_guild_available(self, guild: discord.Guild):
        print(f"Syncing with guild {guild.id}")
        self.tree.copy_global_to(guild=guild)
        await self.tree.sync(guild=guild)

client = DiscordClient()

@client.tree.command(name="timestamp", description="Convert a time into a universal timestamp")
@discord.app_commands.describe(date="YYYY/MM/DD", time="HH:MM", tz="Either UTC±X or common name (ex. CST)")
async def janus(interaction: discord.Interaction, date: str, time: str, tz: str):
    try:
        message = calculate_timestamps(date, time, tz)
        await interaction.response.send_message(message, ephemeral=True)
    except Exception:
        await interaction.response.send_message("Error: One of the entries has an invalid format.", ephemeral=True)

client.run(cfg["discord"])
