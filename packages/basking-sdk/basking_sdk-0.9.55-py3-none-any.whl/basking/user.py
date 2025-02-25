# pylint: disable=line-too-long, invalid-name, too-many-arguments, too-many-locals

"""
Basking.io — Python SDK
- User Class: handles all functionality related to users.
"""

import json
import logging

import pandas as pd


class User:
    """ User class """

    def __init__(self, basking_obj):
        self.basking = basking_obj
        self.log = logging.getLogger(self.__class__.__name__)
        basking_log_level = logging.getLogger(self.basking.__class__.__name__).level
        self.log.setLevel(basking_log_level)

    def get_user(self, pandify=False):
        query = self.basking.graphql_query.get_user_graphql_query()

        result = self.basking.graphql_query.graphql_executor(query=query, variables={})

        data = json.loads(result)

        if 'message' in data:
            self.basking.api_timeout_handler(data)

        data = data['data']['viewer']

        if pandify:
            df = pd.DataFrame(data)
            df.set_index('id', inplace=True)
            return df
        return data

    def get_preferences(self, user_id=None, organization_id=None, location_id=None) -> dict:
        query = self.basking.graphql_query.get_composite_preferences_query()
        data = json.loads(self.basking.graphql_query.graphql_executor(
            query=query,
            variables={
                'userId': user_id,
                'organizationId': organization_id,
                'locationId': location_id,
            }))
        return data['data']['getCompositePreferences']
