import json
import requests
from collections import defaultdict
from discord import Embed, Color
from html2text import html2text


class SpellClient:

    cache = []
    spell_url = "https://api.ashenkingdoms.com/v1/spells"

    def __init__(self):
        self.refresh_cache()

    def get_by_cost(self, cost):
        spell_domain_list = defaultdict(list)
        found_list = list(
            map(
                lambda s: {"name": s["name"], "domain": s["domain"]},
                filter(
                    lambda s: str(s["arcanumCost"]).lower() == str(cost).lower(),
                    self.cache,
                ),
            )
        )

        if not found_list or len(found_list) <= 0:
            return Embed(title=f"No spells found with cost {cost}", color=Color.red())

        for spell in found_list:
            spell_domain_list[spell["domain"]].append(spell["name"])

        response = Embed(title=f"Spells With Cost {cost}:", color=Color.dark_purple())
        for domain, spells in spell_domain_list.items():
            response.add_field(name=domain, value="\n".join(spells), inline=False)

        return response

    def get_by_domain(self, domain):
        spell_cost_list = defaultdict(list)
        found_list = list(
            map(
                lambda s: {"name": s["name"], "cost": s["arcanumCost"]},
                filter(lambda s: s["domain"].lower() == domain.lower(), self.cache),
            )
        )

        if not found_list or len(found_list) <= 0:
            return Embed(
                title=f"No spells found matching domain {domain}", color=Color.red()
            )

        for spell in found_list:
            spell_cost_list[spell["cost"]].append(spell["name"])

        response = Embed(
            title=f'Spells Matching Domain "{domain}:"', color=Color.dark_blue()
        )
        for cost, spells in spell_cost_list.items():
            response.add_field(
                name=f"Arcanum Cost: {cost}", value="\n".join(spells), inline=False
            )

        return response

    def search(self, query):
        spells = list(
            filter(
                lambda s: str(query).lower() in s.get("name", "").lower(), self.cache
            )
        )

        if len(spells) == 1 or query.lower() in list(
            map(lambda s: s["name"].lower(), spells)
        ):
            # Only a single spell was found, so return all the details about it
            spell = (
                spells[0]
                if len(spells) == 1
                else list(
                    filter(lambda s: s["name"].lower() == str(query).lower(), spells)
                )[0]
            )

            response = Embed(title=f'{spell["name"]}', color=Color.dark_purple())
            response.add_field(name="Domain", value=spell["domain"], inline=False)
            response.add_field(
                name="Arcanum Cost", value=spell["arcanumCost"], inline=False
            )
            response.add_field(name="Cast Time", value=spell["castTime"], inline=False)
            if "duration" in spell and spell["duration"]:
                response.add_field(
                    name="Duration", value=spell["duration"], inline=False
                )
            response.add_field(name="Range", value=spell["range"], inline=False)
            response.add_field(
                name="Components", value=spell.get("components", "None"), inline=False
            )
            response.add_field(
                name="Concentration",
                value=spell.get("concentration", False),
                inline=False,
            )
            if "area" in spell and spell["area"]:
                response.add_field(name="Area", value=spell["area"], inline=False)
            response.add_field(
                name="Description",
                value=html2text(spell["description"]).strip(),
                inline=False,
            )
        elif len(spells) >= 1:
            response = Embed(title=f'Spells Matching "query":', color=Color.dark_gold())
            search_result_list = defaultdict(list)

            for spell in spells:
                search_result_list[spell["domain"]].append(
                    {"name": spell["name"], "cost": spell["arcanumCost"]}
                )

            for domain, spells in search_result_list.items():
                spell_detail_list = list(
                    map(lambda s: f'{s["cost"]} - {s["name"]}', spells)
                )
                response.add_field(name=domain, value="\n".join(spell_detail_list))
        else:
            response = Embed(title=f'Spell not found: "{query}"', color=Color.red())

        return response

    def refresh_cache(self):
        headers = {"Accept": "application/json"}
        response = requests.get(url=self.spell_url, headers=headers, verify=False)

        if response.status_code >= 400:
            raise RuntimeError(
                f"Unable to call AshRPG spell API, reason: {response.json()}"
            )

        self.cache = response.json()
