import os
import discord
from discord import app_commands

TOKEN = os.environ["DISCORD_TOKEN"]

intents = discord.Intents.default()


class DMClient(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()


client = DMClient()


@client.event
async def on_ready():
    print(f"Logged in as {client.user}")


@client.tree.command(name="dm", description="Send a DM to a specific user")
@app_commands.describe(recipient="The user to DM", message="Message content to send")
async def dm_command(
    interaction: discord.Interaction,
    recipient: discord.User,
    message: str,
):
    if recipient.bot:
        await interaction.response.send_message(
            "Bots cannot DM other bots.", ephemeral=True
        )
        return

    try:
        await recipient.send(message)
        await interaction.response.send_message(
            f"Sent DM to **{recipient}**.", ephemeral=True
        )
    except discord.Forbidden:
        await interaction.response.send_message(
            f"Could not DM **{recipient}**. They likely have DMs closed or don't share a server with the bot.",
            ephemeral=True,
        )
    except discord.HTTPException as e:
        await interaction.response.send_message(
            f"Failed to send DM: {e}", ephemeral=True
        )


client.run(TOKEN)
