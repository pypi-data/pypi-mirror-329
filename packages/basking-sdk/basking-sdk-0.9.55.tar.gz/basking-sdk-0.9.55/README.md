# Basking.io SDK

Integrate your data with the Basking API, customize the reports & experience,
and join the community of developers building with workplace software apps together with Basking.

Basking.io is a cloud based workplace occupancy platform.
More Information about Basking can be found here: https://basking.io

Basking uses a GraphQL API. The following Python SDK is a wrapper around the production API
designed for our customers that require to access to data programmatically.

## Requirements

* python >=3.7 (current tested version: 3.9)
* pipenv
* A [basking.io account](https://app.basking.io)

## Getting started

#### set the following environment variables:
* `BASKING_USERNAME`: Your username (usually your email)
* `BASKING_USER_PASSWORD`: Your password for Basking. 
* _Optional_: `BASKING_AWS_REGION`: the aws region where your Basking.io instance is hosted. (Defaults to `eu-central-1`)
* _Optional_: `BASKING_API_URL`: the url of the Basking API you would like to query. (Defaults to `api.basking.io`)

```
import logging
from basking.basking_sdk import Basking

# set the default logging
logging.basicConfig()

# mofify the required level of logging for Basking
logging.getLogger('Basking').setLevel(logging.INFO)
logging.getLogger('botocore').setLevel(logging.INFO)

# initialize the SDK and set general query parameters
basking_client = Basking()

# list buildings the current user has access to
df_buildings = basking_client.location.get_user_buildings(pandify=True)

# get building meta data
building_meta_data = basking_client.location.get_building(
building_id=building_id
)
tz_str = building_meta_data['data']['getBuilding']['timeZone']


# get building daily occupancy statistics
df_daily = basking_client.occupancy.get_building_occupancy_stats_daily(
building_id=building_id,
start_obj_tz_unaware=start_date_obj,
end_obj_tz_unaware=end_date_obj,
pandify=True
)
df_daily.to_csv('./df_daily.csv')
```


For more examples, see `basking.api_usage_example`, or [contact us](https://basking.io/contact-us/)