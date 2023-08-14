import math
import sys

import click
from mcstatus import JavaServer
import nextcord
from nextcord.ext import commands


@click.command()
@click.option("--dc-api-key", "-d", help="Discord API key")
@click.option("--host", "-h", help="Minecraft server hostname")
@click.option("--port", "-p", help="Minecraft server port")
def main(dc_api_key: str, host: str, port: str) -> None:
    intents = nextcord.Intents.default()
    bot = commands.Bot(intents=intents)
    server = JavaServer.lookup(f"{host}:{port}")

    @bot.event
    async def on_ready() -> None:
        print(f"Logged in as {bot.user}")

    @bot.slash_command(description="Get server status")
    async def server_status(interaction: nextcord.Interaction) -> None:
        try:
            await interaction.response.defer()

            status = server.status()
            max_players = status.players.max
            motd = status.description
            server_version = status.version.name
            player_count = status.players.online
            latency = status.latency
            embed = nextcord.Embed(title="gescraft", color=nextcord.Color.green())
            embed.set_author(
                name="gescraft",
                url="https://mc.kruhlmann.dev",
                icon_url="http://www.rw-designer.com/icon-image/5547-256x256x8.png",
            )
            embed.add_field(name="Version", value=server_version, inline=False)
            embed.add_field(name="Players online", value=f"{player_count}/{max_players}", inline=False)
            embed.add_field(name="Latency", value=f"{math.ceil(latency)}ms", inline=False)
            embed.add_field(name="MOTD", value=motd, inline=False)

            await interaction.followup.send(embed=embed)
        except Exception as error:
            sys.stderr.write(f"{error}\n")
            await interaction.followup.send("Gah!")

    bot.run(dc_api_key)


if __name__ == "__main__":
    main()
