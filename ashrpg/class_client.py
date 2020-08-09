import requests
from discord import Embed, Color
from html2text import html2text
from .enums import ClassColors


class ClassClient:

    class_list = {}

    class_list_url = "https://api.ashenkingdoms.com/v1/classes"

    def __init__(self):
        self.refresh_class_list()

    def get_class_info(self, class_name):
        cls = self.class_list[class_name]
        res = Embed(
            title=f"{class_name.capitalize()} - {cls['classType'].capitalize()} Class",
            color=ClassColors[class_name.upper()].value,
        )
        res.add_field(
            name="Signature Ability", value=cls["signatureAbility"], inline=False
        )
        res.add_field(name="Hit Dice", value=cls["hitDice"], inline=False)
        res.add_field(
            name="Weapon Proficiencies",
            value=", ".join(cls["weaponProficiencies"]),
            inline=False,
        )
        res.add_field(
            name="Armor Proficiencies",
            value=", ".join(cls["armorProficiences"]),
            inline=False,
        )

        self.refresh_class_details(class_name)

        return res

    def search_talents_and_feats(self, class_name, query):
        # Check if cache is populated for this class
        if not self.class_list[class_name].get("feats", None):
            self.refresh_class_details(class_name)

        talents = list(
            filter(
                lambda x: str(query).lower() in x.get("name", "").lower(),
                self.class_list[class_name]["feats"],
            )
        )

        if len(talents) == 1 or query.lower() in list(
            map(lambda x: x["name"].lower(), talents)
        ):
            # Only a single talent found, so return all details about it
            talent = (
                talents[0]
                if len(talents) == 1
                else list(
                    filter(lambda x: x["name"].lower() == str(query).lower(), talents)
                )[0]
            )

            res = Embed(
                title=f"{talent['name']} -- Level {talent['level']} {class_name.capitalize()} {talent['talentType'].capitalize()}",
                color=ClassColors(class_name.upper()).value,
            )
            res.add_field(name="Cast Type", value=talent["castTime"], inline=True)
            res.add_field(name="Duration", value=talent["duration"], inline=True)
            res.add_field(
                name="Description",
                value=html2text(talent["description"]).strip(),
                inline=False,
            )
            res.add_field(
                name="Requirements",
                value="\n".join(talent["requirements"])
                if talent["requirements"]
                else "None",
                inline=False,
            )
            res.add_field(
                name="Prerequisite", value=talent["requiredFeat"], inline=False
            )
        elif len(talents) >= 1:
            # User is searching based on a query, so return a list of talents
            res = Embed(title=f'Features Matching "{query}":', color=Color.dark_gold())
            talent_map = {
                feat_name: []
                for feat_name in list(
                    map(lambda x: x["talentType"].capitalize(), talents)
                )
            }
            for talent in list(
                map(
                    lambda x: {"name": x["name"], "type": x["talentType"].capitalize()},
                    talents,
                )
            ):
                talent_map[talent["type"]].append(talent["name"])

            for type, names in talent_map.items():
                res.add_field(name=type, value="\n".join(names), inline=False)

        else:
            res = Embed(
                title=f'Feature/ talent not found for class {class_name.capitalize()}: "{query}"',
                color=Color.red(),
            )

        return res

    def refresh_class_list(self):
        headers = {"Accept": "application/json"}
        response = requests.get(url=self.class_list_url, headers=headers, verify=False)

        if response.status_code >= 400:
            raise RuntimeError(
                f"Unable to call AshRPG Class List API, reason: {response.json()}"
            )

        # Set the class list with the key as the class name and value as basic values
        self.class_list = {x["name"]: x for x in response.json()}

    def refresh_class_details(self, class_name):
        headers = {"Accept": "application/json"}
        response = requests.get(
            url=f"{self.class_list_url}/{class_name}", headers=headers, verify=False
        )

        if response.status_code >= 400:
            raise RuntimeError(
                f"Unable to call AshRPG Class List API, reason: {response.json()}"
            )

        # Update the class cache with updated info
        self.class_list[class_name] = response.json()

        # Delete class table and combine talent/ feat lists for ease of searching
        self.class_list[class_name]["feats"] = [
            *self.class_list[class_name]["features"],
            *self.class_list[class_name]["talents"],
        ]
        del self.class_list[class_name]["levelTable"]
        del self.class_list[class_name]["features"]
        del self.class_list[class_name]["talents"]
