import requests
from discord import Embed, Color
from .enums import FeatTypes

class FeatClient():

    cache = {}
    feat_url = 'https://api.ashenkingdoms.com/v1/feats'

    def __init__(self):
        self.refresh_cache()

    def search(self, query):
        feats = list(filter(lambda x : str(query).lower() in x.get('name', '').lower(), self.cache))

        if len(feats) == 1 or query.lower() in list(map(lambda x : x['name'].lower(), feats)):
            # Only a single feat was found, so return all the details about it
            feat = feats[0]
            feat['featType'] = FeatTypes[feat['featType']]

            res = Embed(title=f"{feat['name']}", color=feat['featType'].value)
            res.add_field(name='Type', value=feat['featType'].name.capitalize(), inline=False)
            res.add_field(name='Description', value=feat['description'], inline=False)
            res.add_field(name='Requirements', value='\n'.join(feat['requirements']) if feat['requirements'] else 'None' , inline=False)
            res.add_field(name='Prerequisite', value=feat['requiredFeat'], inline=False)
        elif len(feats) >= 1:
            # User is searching based on a query, so return a list of feats based on that name
            res = Embed(title=f"Features Matching \"{query}\":", color=Color.dark_gold())
            feat_map = {feat_name: [] for feat_name in list(map(lambda x : x['featType'].capitalize(), feats))}
            for feat in list(map(lambda x : {'name': x['name'], 'type': x['featType'].capitalize()}, feats)):
                feat_map[feat['type']].append(feat['name'])

            for type, names in feat_map.items():
                res.add_field(name=type, value='\n'.join(names), inline=False)
        else:
            res = Embed(title=f"Feat not found: \"{query}\"", color=Color.red())

        return res

    def refresh_cache(self):
        headers = {
            'Accept': 'application/json'
        }
        response = requests.get(url=self.feat_url, headers=headers, verify=False)

        if response.status_code >= 400:
            raise RuntimeError(f"Unable to call AshRPG API, reason: {response.json()}")

        self.cache = response.json()
