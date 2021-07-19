import json
import requests

from bs4 import BeautifulSoup


class App:
    def __init__(self, app_id) -> None:
        self.app_id = str(app_id)

    def details(self, cc='US', basic_only=False):
        basic_only = 'basic' if basic_only else ''
        data = requests.get(rf'https://store.steampowered.com/api/appdetails/?appids={self.app_id}&cc={cc}&filters={basic_only}').json()

        try:
            return data[self.app_id]["data"]
        except KeyError:
            return None

    def __getitem__(self, key):
        return getattr(self, key)

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return f'<App id:{self.app_id}>'


class Bundle:
    def __init__(self, bundle_id, bundle_data, title) -> None:
        self.bundle_id = bundle_id
        self.bundle_data = json.loads(bundle_data)
        self.title = title

    def items(self):
        items = self.bundle_data["m_rgItems"]
        included_appids = [App(j) for i in items for j in i["m_rgIncludedAppIDs"]]

        return included_appids

    def __getitem__(self, key):
        return getattr(self, key)

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return f'<Bundle id:{self.bundle_id} name:_{self.title}_>'


class Filters:
    def __init__(self, file) -> None:
        with open(file, 'r') as filters_json:
            filters = json.load(filters_json)
        for i in filters:
            setattr(self, i, filters[i])


class Search:
    def __init__(self) -> None:
        pass

    def search(self, search_term: str, full_link=False):
        results = []

        if not full_link:
            search_req = requests.get(rf'https://store.steampowered.com/search/?term={search_term}')
        else:
            search_req = requests.get(search_term)

        if search_req.ok:
            soup = BeautifulSoup(search_req.text, 'html.parser')
            for item in soup.find_all('a', class_='search_result_row ds_collapse_flag'):
                try:
                    results.append(App(app_id=item["data-ds-appid"]))
                except KeyError:
                    results.append(Bundle(
                        bundle_id=item["data-ds-bundleid"],
                        bundle_data=item["data-ds-bundle-data"],
                        title=item.find('div', class_='col search_name ellipsis').span.text
                    ))
            return results

    def advanced_search(self, search_term='', discounted=False, tags='', types='', player_number='', supported_os='',
                        supported_languages=''):
        search_term = rf'https://store.steampowered.com/search/?term={search_term}'

        search_term += '&specials=1' if discounted else ''
        search_term += '&tags=' + (','.join(tags) if len(tags) > 1 and isinstance(tags, list) else tags) if tags else ''
        search_term += '&category1=' + (','.join(types) if len(types) > 1 and isinstance(types, list) else types) if types else ''
        search_term += '&category3=' + (','.join(player_number) if len(player_number) > 1 and isinstance(player_number, list) else player_number) if player_number else ''
        search_term += '&os=' + (','.join(supported_os) if len(supported_os) > 1 and isinstance(supported_os, list) else supported_os) if supported_os else ''
        search_term += '&supportedlangs=' + (','.join(supported_languages) if len(supported_languages) > 1 and isinstance(supported_languages, list) else supported_languages) if supported_languages else ''

        return self.search(search_term, full_link=True)
