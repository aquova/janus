import discord

from datetime import datetime, timezone
import json

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

def calculate_timestamps(date: str, time: str, tz: str) -> str:
    tz_offset = tz[3:].zfill(3)
    combined_time = f"{date} {time} {tz_offset}00"
    desired = datetime.strptime(combined_time, "%Y/%m/%d %H:%M %z")
    epoch = datetime(1970, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
    unix = int((desired - epoch).total_seconds())
    output = f"Here are some timestamps and how they'll display!\n`<t:{unix}:F>` - <t:{unix}:F>\n`<t:{unix}:f>` - <t:{unix}:f>\n`<t:{unix}:D>` - <t:{unix}:D>\n`<t:{unix}:d>` - <t:{unix}:d>\n`<t:{unix}:t>` - <t:{unix}:t>\n`<t:{unix}:T>` - <t:{unix}:T>\n`<t:{unix}:R>` - <t:{unix}:R>"
    return output

client = DiscordClient()

@client.tree.command(name="timestamp", description="Convert a time into a universal timestamp")
@discord.app_commands.describe(date="YYYY/MM/DD", time="HH:MM", tz="UTC±X")
async def janus(interaction: discord.Interaction, date: str, time: str, tz: str):
    try:
        message = calculate_timestamps(date, time, tz)
        await interaction.response.send_message(message, ephemeral=True)
    except Exception:
        await interaction.response.send_message("Error: One of the entries has an invalid format.", ephemeral=True)

client.run(cfg["discord"])
