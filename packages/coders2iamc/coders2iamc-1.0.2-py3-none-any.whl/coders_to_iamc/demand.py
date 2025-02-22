import json
from urllib.request import urlopen
import pandas as pd

from coders_to_iamc.constants import CODERS


def get_canadian_data(api_key: str, province: str, year: int):
    """
    This function is used to get the technology parameter data from the CODERS API
    """
    with urlopen(f"{CODERS}/provincial_demand?key={api_key}&province={province}&year={year}") as response:
        response_content = response.read()
        json_response = json.loads(response_content)
        modeled_attributes = pd.json_normalize(json_response)

    modeled_attributes = modeled_attributes[
        ['local_time', 'demand_MWh', 'province']]
    melted = modeled_attributes.melt(id_vars=['local_time', 'province'], var_name='variable', value_name='value')

    melted['variable'] = 'Demand'
    melted.rename(columns={'province': 'region', 'local_time':'time'}, inplace=True)
    return melted

def get_us_data(api_key: str, province: str, year: int):
    """
    This function is used to get the technology parameter data from the CODERS API
    """
    with urlopen(f"{CODERS}/international_transfers?key={api_key}") as response:
        response_content = response.read()
        json_response = json.loads(response_content)
        modeled_attributes = pd.json_normalize(json_response)

    states = modeled_attributes[modeled_attributes['province'] == province]['us_state'].unique()

    if len(states) == 0:
        return pd.DataFrame()

    states_data = []
    for state in states:
        with urlopen(f"{CODERS}/international_transfers?key={api_key}&province={province}&us_state={state}&year={year}") as response:
            response_content = response.read()
            json_response = json.loads(response_content)
            modeled_attributes = pd.json_normalize(json_response)

        modeled_attributes = modeled_attributes[
            ['local_time', 'transfers_MWh', 'province']]
        melted = modeled_attributes.melt(id_vars=['local_time', 'province'], var_name='variable', value_name='value')

        melted['variable'] = 'US Demand'
        melted.rename(columns={'province': 'region', 'local_time':'time'}, inplace=True)
        states_data.append(melted)

    full_df = pd.concat(states_data)

    full_df = full_df.groupby(['time', 'region', 'variable']).sum().reset_index()
    return full_df


if __name__ == '__main__':
    api_key = ''
    df = get_canadian_data(api_key, 'AB', 2018)
