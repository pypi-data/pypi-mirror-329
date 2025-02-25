# pylint: disable=line-too-long, invalid-name, too-many-arguments, too-many-locals, fixme
"""
Basking.io — Python SDK
- Occupancy Class: handles all functionality related to occupancy.
"""

import json
import logging
import os
from datetime import datetime, timedelta, date, time
from typing import Tuple, Iterator, Union, List, Literal, Optional

import pandas
import pandas as pd
from pip._internal.utils.deprecation import deprecated

SQM_TO_SQF_RATE = 10.7639

CapacityType = Literal['workstations', 'total_seats']


class Occupancy:
    """
    Handles all functionality related to occupancy data.
    The occupancy class can be accessed as follows
    ::
        basking.occupancy
    """

    def __init__(self, basking_obj):
        self.basking = basking_obj
        self.log = logging.getLogger(self.__class__.__name__)
        basking_log_level = logging.getLogger(self.basking.__class__.__name__).level
        self.log.setLevel(basking_log_level)

    def get_building_occupancy_stats_daily(
            self, building_id,
            start_date: date,
            end_date: date,
            floor_ids: [str] = None,
            floor_area_ids: [int] = None,
            pandify=False,
            *,
            capacity_type: CapacityType = None,
    ) -> Union[pandas.DataFrame, List[dict]]:
        """
        Returns daily statistical occupancy data for a building between the given time frames.
        """
        start_date = self.basking.utils.convert_timestamp_to_building_timezone(building_id, start_date)
        end_date = self.basking.utils.convert_timestamp_to_building_timezone(building_id, end_date)

        try:
            page_size_d = int(os.getenv('API_PAGESIZE', '30'))
            date_slices = self._paginate_dates(start_date, end_date, page_size_d)
            data = []

            for start_date, end_date in date_slices:
                result = self.basking.graphql_query.graphql_executor(
                    *self.basking.graphql_query.get_building_occupancy_stats_daily_graphql_query(
                        building_id,
                        start_date,
                        end_date,
                        floor_ids,
                        floor_area_ids,
                        capacity_type,
                    )
                )
                data += json.loads(result)['data']['location']['occupancy']['daily']

            if pandify:
                df = pd.DataFrame(data)
                if len(df):
                    try:
                        df.set_index('date', inplace=True)
                        df.rename(columns={
                            'avgCount': 'occupancy_daily_avg',
                            'peakCount': 'occupancy_daily_peak',
                            'uniqueCount': 'occupants_daily_unique',
                        }, inplace=True)
                        df = df[
                            ['occupancy_daily_avg', 'occupancy_daily_peak', 'occupants_daily_unique',
                             'capacity', 'adjustedCapacity', 'capacityPct']]
                        df.index = pd.to_datetime(df.index)
                        building = self.basking.location.get_building(building_id=building_id, pandify=False)
                        tz_str = building['data']['getBuilding']['timeZone']
                        if not tz_str:
                            raise AssertionError(f'length for time zone {len(tz_str)} is not correct.')
                        df.index = df.index.tz_localize(None).tz_localize(tz_str, nonexistent='shift_forward')
                    except TypeError:
                        self.log.error("getting error in dataframe portion")
                else:
                    self.log.debug('no data returned for %s', building_id)
                return df
            return data
        except TypeError:
            self.log.error('no data returned for %s', building_id)

    @staticmethod
    def _paginate_dates(start: datetime, end: datetime, page_size: int) -> Iterator[Tuple[datetime, datetime]]:
        date_slices = []
        slice_start = start
        while slice_start < end:
            next_slice_start = slice_start + timedelta(days=page_size)
            date_slices += [(slice_start, min(next_slice_start, end) - timedelta(seconds=1))]
            yield slice_start, min(next_slice_start, end) - timedelta(seconds=1)
            slice_start = next_slice_start

    def get_building_occupancy_hourly(
            self,
            building_id: str,
            start_date: date,
            end_date: date,
            floor_ids: [str] = None,
            floor_area_ids: [int] = None,
            ap_id=0,
            pandify=True,
            *,
            capacity_type: CapacityType = None,
    ) -> Union[pandas.DataFrame, List[dict]]:
        """
        This function returns the hourly occupancy data for the specified range aggregated in 3 levels.
        You can choose the aggregation level by specifying the parameters.
            - Building (specify building_id)
            - Floor  (specify building_id + floor_id)
            - Access Point (specify building_id + floor_id + ap_id)

        TODO: prevent passing floor and floor_area at the same time. only 1 is possible, or none.
        """
        start_date = self.basking.utils.convert_timestamp_to_building_timezone(building_id, start_date)
        end_date = self.basking.utils.convert_timestamp_to_building_timezone(building_id, end_date)
        building = self.basking.location.get_building(building_id=building_id)

        try:
            page_size_d = int(os.getenv('API_PAGESIZE', '30'))
            date_slices = self._paginate_dates(start_date, end_date, page_size_d)
            data = []

            for start_date, end_date in date_slices:
                data_ = self._get_building_occupancy_hourly_pagination(
                    start_date,
                    end_date,
                    building_id,
                    floor_ids,
                    floor_area_ids,
                    ap_id,
                    capacity_type=capacity_type,
                )
                if 'message' in data:
                    self.basking.api_timeout_handler(data)
                data += data_['data']['location']['occupancy']['hourly']

            self.log.debug('Done with pagination')
            if len(data):
                if pandify:
                    df = pd.DataFrame(data)
                    df.rename(columns={
                        'hour': 'timestamp',
                        'occupancy': 'occupancy_hourly'
                    }, inplace=True)

                    df.set_index(pd.to_datetime(df['timestamp']), inplace=True)

                    # convert the tz to building tz
                    df.index = df.tz_convert(building['data']['getBuilding']['timeZone']).index
                    df = df[['occupancy_hourly', 'capacity', 'adjustedCapacity', 'capacityPct']]
                    return df
                return data
            else:
                self.log.info('got no data')
                if pandify:
                    return pd.DataFrame()
        except Exception as e:
            self.log.error(e)
            raise e

    def _get_building_occupancy_hourly_pagination(
            self,
            start_date: datetime,
            end_date: datetime,
            building_id: str,
            floor_ids: [str],
            floor_area_ids: [int],
            ap_id: int,
            *,
            capacity_type: CapacityType = None
    ) -> dict:
        """
        Internal method used to paginate long queries of hourly data.
        Callers are responsible to convert dates to building's timezone
        """

        query, variables = self.basking.graphql_query.get_building_occupancy_hourly_pagination_graphql_query(
            building_id,
            start_date,
            end_date,
            capacity_type,
        )
        variables.update({'floorIds': [], 'floorAreaIds': []})
        if ap_id:
            variables['ap_id'] = ap_id
            # if not specified, then aggregation level will be floor

        for floor_id in floor_ids or []:
            variables['floorIds'].append(floor_id)

        for floor_area_id in floor_area_ids or []:
            variables['floorAreaIds'].append(floor_area_id)
            # if not specified, then aggregation level will be Building

        result = self.basking.graphql_query.graphql_executor(query=query, variables=variables)

        data = json.loads(result)
        if 'message' in data:
            self.basking.api_timeout_handler(data)
        if 'errors' in data:
            self.log.error('Error in query:')
            self.log.error(data['errors'])
        return data

    def get_floor_heatmap_kpi(
            self,
            basking_floor_id: int,
            start_date: date,
            end_date: date,
            pandify=False
    ) -> Union[pandas.DataFrame, List[dict]]:
        """
        Returns the peak occupancy KPI by areas for a floor id between the specified time period.
        """
        building_id = self.basking.location.get_floor_meta_info(basking_floor_id)['data']['getFloor']['buildingId']
        start_date = self.basking.utils.convert_timestamp_to_building_timezone(building_id, start_date)
        end_date = self.basking.utils.convert_timestamp_to_building_timezone(building_id, end_date)
        self.log.debug(
            """Started get_floor_heatmap_kpi with
                    - basking_floor_id=%s
                    - start_date=%s
                    - end_date=%s
            """,
            basking_floor_id,
            start_date,
            end_date
        )
        query, variables = self.basking.graphql_query.get_floor_heatmap_kpi_graphql_query(
            basking_floor_id,
            start_date,
            end_date
        )

        result = self.basking.graphql_query.graphql_executor(query=query, variables=variables)
        data = json.loads(result)
        if 'message' in data:
            self.basking.api_timeout_handler(data)
        try:
            data = data['data']['getFloorHeatmapKPI']
            if len(data):
                if pandify:
                    df = pd.DataFrame(data)
                    return df
                return data
        except TypeError:
            self.log.info('got no data')

    def get_location_duration_of_visits(
            self,
            building_id: str,
            start_date: date,
            end_date: date,
            floor_ids: [str] = None,
            floor_area_ids: [int] = None,
            pandify=True,
            *,
            capacity_type: CapacityType = None,
    ) -> Union[pandas.DataFrame, List[dict]]:
        """
        Returns the histogram of the duration of visits between 2 dates at building level.
        Read more about this feature here: https://basking.io/blog/new-features/understand-the-duration-of-visits/

         """
        start_date = self.basking.utils.convert_timestamp_to_building_timezone(building_id, start_date)
        end_date = self.basking.utils.convert_timestamp_to_building_timezone(building_id, end_date)
        query, variables = self.basking.graphql_query.get_location_duration_of_visits_graphql_query(
            building_id,
            start_date,
            end_date,
            floor_ids,
            floor_area_ids,
            capacity_type,
        )

        result = self.basking.graphql_query.graphql_executor(query=query, variables=variables)

        data = json.loads(result)
        if 'message' in data:
            self.basking.api_timeout_handler(data)

        try:
            data = data['data']['location']['occupancy']['duration']
        except TypeError:
            self.log.error('no data')
            return data

        if 'message' in data:
            self.basking.api_timeout_handler(data)

        if 'errors' in data:
            self.log.error('Error in query:')
            self.log.error(data['errors'])
            return data

        if len(data) > 0:
            if pandify:
                df = pd.DataFrame(data)
                return df
            return data
        self.log.info('got no data')
        return pd.DataFrame()

    def get_location_frequency_of_visits(
            self,
            building_id: str,
            start_date: date,
            end_date: date,
            floor_ids: [str] = None,
            floor_area_ids: [int] = None,
            pandify=None,
            *,
            capacity_type: CapacityType = None,
    ) -> Union[pandas.DataFrame, List[dict]]:

        """
        Returns the histogram of the frequency of visits between 2 dates at building level.
        Read more about this feature here:
        https://basking.io/blog/new-features/understand-the-frequency-of-visits-to-your-office/.
         """
        start_date = self.basking.utils.convert_timestamp_to_building_timezone(building_id, start_date)
        end_date = self.basking.utils.convert_timestamp_to_building_timezone(building_id, end_date)

        query, variables = self.basking.graphql_query.get_location_frequency_of_visits_graphql_query(
            building_id,
            start_date,
            end_date,
            floor_ids,
            floor_area_ids,
            capacity_type,
        )

        result = self.basking.graphql_query.graphql_executor(query=query, variables=variables)
        data = json.loads(result)

        if 'message' in data:
            self.basking.api_timeout_handler(data)

        data = data['data']['location']['occupancy']['frequencyOfVisits']

        if 'errors' in data:
            self.log.error('Error in query:')
            self.log.error(data['errors'])
            return data

        if len(data) > 0:
            if pandify:
                df = pd.DataFrame(data)
                return df
            return data
        self.log.info('got no data')

    def get_density_for_building(
            self,
            building_id: str,
            start_date: date,
            end_date: date,
            floor_ids: [str] = None,
            floor_area_ids: [int] = None,
            *,
            capacity_type: CapacityType = None,
    ) -> Optional[int]:
        """
        Returns the density of the office in RSM at peak between the time period defined.

        :return: density in RSM
        """
        # 1. get the area
        try:
            building = self.basking.location.get_building(building_id=building_id)

            area_location = building['data']['getBuilding']['area']

            building_measurement_units = building['data']['getBuilding']['measurementUnits']

            user_measurement_units = self.basking.user.get_user(pandify=False)['measurementUnits']

            if (user_measurement_units == 'Imperial' and building_measurement_units == 'Imperial'
                    or user_measurement_units == 'Metric' and building_measurement_units == 'Metric'):
                area_metric = area_location
            elif user_measurement_units == 'Imperial' and building_measurement_units == 'Metric':
                area_metric = area_location * SQM_TO_SQF_RATE
            elif user_measurement_units == 'Metric' and building_measurement_units == 'Imperial':
                area_metric = area_location / SQM_TO_SQF_RATE
        except (AttributeError, TypeError):
            self.log.error('no data')

        try:
            # 2. get the daily peaks occupancy
            df_building_daily_stats = self.get_building_occupancy_stats_daily(
                building_id=str(building_id),
                start_date=start_date,
                end_date=end_date,
                floor_ids=floor_ids,
                floor_area_ids=floor_area_ids,
                pandify=True,
                capacity_type=capacity_type,
            )
        except (AttributeError, TypeError):
            self.log.error('no data')

        peak_counts = []
        for index, row in df_building_daily_stats.iterrows():
            peak_counts.append(row['occupancy_daily_peak'])
        peak_occupancy = max(peak_counts) if peak_counts else False
        return area_metric / peak_occupancy if peak_occupancy else False

    def get_density_for_building_last_days(
            self,
            building_id: str,
            days=7,
            *,
            capacity_type: CapacityType = None,
    ):
        """
        Returns the density of an office in RSM at peak for the last 7 days from now.
        """
        end_date_obj = date.today()
        start_date_obj = end_date_obj - timedelta(days=days)
        return (
            self.get_density_for_building(
                building_id=building_id,
                start_date=start_date_obj,
                end_date=end_date_obj,
                capacity_type=capacity_type,
            )
        )

    def get_location_popular_days_of_visits(
            self,
            building_id: str,
            start_date: date,
            end_date: date,
            floor_ids: [str] = None,
            floor_area_ids: [int] = None,
            pandify=None,
            *,
            capacity_type: CapacityType = None,
    ):
        """
        Returns the popular days of visits for a location between the specified dates.
        :return: Data frame or array of popular days of visit.
        """
        try:
            start_date = self.basking.utils.convert_timestamp_to_building_timezone(building_id, start_date)
            end_date = self.basking.utils.convert_timestamp_to_building_timezone(building_id, end_date)

            self.log.debug('Started get_popular_day_of_visit with'
                           ' - building_id=%s'
                           ' - start_date_str=%s'
                           ' - end_date_str=%s',
                           building_id, start_date.isoformat(), end_date.isoformat())

            query, variables = self.basking.graphql_query.get_location_popular_days_of_visits_graphql_query(
                building_id,
                start_date,
                end_date,
                floor_ids,
                floor_area_ids,
                capacity_type,
            )
            result = self.basking.graphql_query.graphql_executor(query=query, variables=variables)
            data = json.loads(result)
            if 'message' in data:
                self.basking.api_timeout_handler(data)
            if pandify:
                popular_day_data = data['data']['location']['occupancy']['popularDaysOfVisit']
                df = pd.DataFrame(popular_day_data)
                return df
            return data
        except TypeError:
            self.log.error('no data')

    def get_organization_duration_of_visits(
            self,
            organization_id: int,
            start_date: date,
            end_date: date,
            floor_ids: [str] = None,
            floor_area_ids: [int] = None,
            pandify=True
    ) -> Union[pandas.DataFrame, List[dict]]:
        """
        Returns the duration of visits in for an organization between the specified time range.
        """

        try:
            query, variables = self.basking.graphql_query.get_organization_duration_of_visits_graphql_query(
                organization_id=organization_id,
                start_date=datetime.combine(start_date, time()),
                end_date=datetime.combine(end_date, time()),
                floor_ids=floor_ids,
                floor_area_ids=floor_area_ids,
            )
            result = self.basking.graphql_query.graphql_executor(query=query, variables=variables)
            data = json.loads(result)
            if 'message' in data:
                self.basking.api_timeout_handler(data)
            if 'errors' in data:
                self.log.error(data)
                return data
            pd_data = data['data']['organization']['durationOfVisits']
            if pandify:
                df = pd.DataFrame(pd_data)
                return df
            return data
        except TypeError:
            self.log.error('no data')

    def get_organization_frequency_of_visits(
            self,
            organization_id: int,
            start_date: date,
            end_date: date,
            floor_ids: [str] = None,
            floor_area_ids: [int] = None,
            pandify=True
    ) -> Union[pandas.DataFrame, List[dict]]:
        """
        Returns the frequency of visits for an organization between the selected dates.
        """

        try:
            query, variables = self.basking.graphql_query.get_organization_frequency_of_visits_graphql_query(
                organization_id=organization_id,
                start_date=datetime.combine(start_date, time()),
                end_date=datetime.combine(end_date, time()),
                floor_ids=floor_ids,
                floor_area_ids=floor_area_ids,
            )

            result = self.basking.graphql_query.graphql_executor(query=query, variables=variables)
            data = json.loads(result)
            if 'message' in data:
                self.basking.api_timeout_handler(data)
            if 'errors' in data:
                self.log.error(data)
                return data

            pd_data = data['data']['organization']['frequencyOfVisits']
            if pandify:
                df = pd.DataFrame(pd_data)
                return df
            return data
        except TypeError:
            self.log.error('no data')

    def get_organization_popular_days_of_visits(
            self,
            organization_id: int,
            start_date: date,
            end_date: date,
            floor_ids: [str] = None,
            floor_area_ids: [int] = None,
            pandify=True
    ) -> Union[pandas.DataFrame, List[dict]]:

        """
        Returns the popular days of visit between the specified time range at organization level.
        """
        query, variables = self.basking.graphql_query.get_organization_popular_days_of_visits_graphql_query(
            organization_id=organization_id,
            start_date=datetime.combine(start_date, time()),
            end_date=datetime.combine(end_date, time()),
            floor_ids=floor_ids,
            floor_area_ids=floor_area_ids,
        )
        result = self.basking.graphql_query.graphql_executor(query=query, variables=variables)
        data = json.loads(result)
        if 'errors' in data:
            return data
        if pandify:
            pd_data = data['data']['organization']['popularDaysOfVisits']
            if pd_data:
                df = pd.DataFrame(pd_data)
                return df
            else:
                self.log.error('no data')
        return data
