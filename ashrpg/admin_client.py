import json
from io import StringIO
from discord import Embed, Color, File


class AdminClient:
    def get_guild_list(self, bot):
        response = Embed(
            title="Audit list for the bot. See attached file for details.",
            color=Color.red(),
        )
        guild_list = []

        for guild in bot.guilds:
            owner = bot.get_user(guild.owner_id)
            guild_list.append(
                {
                    "id": guild.id,
                    "name": guild.name,
                    "owner": {
                        "id": owner.id,
                        "name": owner.name,
                        "isBot": owner.bot,
                        "isSystem": owner.system,
                    },
                    "description": guild.description,
                }
            )

        response.add_field(
            name="Guild Name", value="\n".join([g["name"] for g in guild_list])
        )

        return (
            response,
            File(
                StringIO(json.dumps({"guilds": guild_list})),
                filename="guild-list.json",
                spoiler=True,
            ),
        )
