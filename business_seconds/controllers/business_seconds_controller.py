import logging
from datetime import datetime, timedelta
from typing import List

import holidays


class BusinessSecondsController:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.start_date: datetime = datetime.strptime(
            '19000101000000', '%Y%m%d%H%M%S'
        )
        self.start_date_begin: datetime = datetime.strptime(
            '19000101000000', '%Y%m%d%H%M%S'
        )
        self.start_date_closure: datetime = datetime.strptime(
            '19000101000000', '%Y%m%d%H%M%S'
        )
        self.end_date: datetime = datetime.strptime(
            '29991231235959', '%Y%m%d%H%M%S'
        )
        self.end_date_begin: datetime = datetime.strptime(
            '19000101000000', '%Y%m%d%H%M%S'
        )
        self.end_date_closure: datetime = datetime.strptime(
            '19000101000000', '%Y%m%d%H%M%S'
        )

    def business_seconds(self, start: datetime, end: datetime):
        """
        Args:

        Returns:

        """
        # Check how many weekend and public holidays are between the start
        # date and end date
        if start == end:
            return 0

        self.start_date_begin = datetime.strptime(
            f'{start.year}{start.month}'
            f'{start.day if len(str(start.day)) > 1 else f"0{start.day}"}080000',
            '%Y%m%d%H%M%S',
        )
        self.start_date_closure = datetime.strptime(
            f'{start.year}{start.month}'
            f'{start.day if len(str(start.day)) > 1 else f"0{start.day}"}170000',
            '%Y%m%d%H%M%S',
        )
        self.end_date_begin = datetime.strptime(
            f'{end.year}{end.month}'
            f'{end.day if len(str(end.day)) > 1 else f"0{end.day}"}080000',
            '%Y%m%d%H%M%S',
        )
        self.end_date_closure = datetime.strptime(
            f'{end.year}{end.month}'
            f'{end.day if len(str(end.day)) > 1 else f"0{end.day}"}170000',
            '%Y%m%d%H%M%S',
        )
        self.start_date: datetime = start - timedelta(days=1)
        self.end_date: datetime = end
        holiday = self.holidays(self.start_date, self.end_date)
        business_days = self.calculate_business_days(holiday)
        business_seconds = self.calculate_business_seconds(
            business_days, holiday
        )

        return business_seconds

    def calculate_business_seconds(self, business_days: int, holiday):
        # business_secs = 0
        # if business_days <= 0:
        #     return business_secs
        next_working_day = self.calculate_working_day('start', holiday)
        prev_working_day = self.calculate_working_day('end', holiday)
        total_seconds = self.calculate_total_seconds(
            next_working_day, prev_working_day, holiday
        )

        return total_seconds

    @staticmethod
    def calculate_total_seconds(
        start_date: datetime, end_date: datetime, holiday: dict
    ):
        if end_date < start_date:
            return 0

        total_days = (end_date - start_date).days
        total_seconds = (end_date - start_date).total_seconds()
        total_holidays = sum(list(holiday.values()))
        non_bus_days_sec = total_days * 15 * 60 * 60

        if end_date.date() > start_date.date():
            total_seconds = (
                total_seconds
                - non_bus_days_sec
                - (total_holidays * 9 * 60 * 60)
            )

        return total_seconds

    def calculate_working_day(self, date_type: str, holiday: dict):
        start_hol = holiday['start_hol']
        end_hol = holiday['end_hol']
        start_date = self.start_date + timedelta(days=1)
        end_date = self.end_date

        if date_type == 'start':
            next_day = self.start_date_begin
            if start_hol:
                next_day = self.calc_next_day(next_day, 'start')
            elif start_date > next_day:
                if start_date > self.start_date_closure:
                    next_day = next_day + timedelta(days=1)
                    next_day = self.calc_next_day(next_day, 'start')
                else:
                    next_day = start_date
        elif date_type == 'end':
            next_day = self.end_date_closure
            if end_hol:
                next_day = self.calc_next_day(next_day, 'end')
                if next_day < start_date:
                    next_day = start_date
            elif end_date < next_day:
                if end_date < self.end_date_begin:
                    next_day = next_day - timedelta(days=1)
                    next_day = self.calc_next_day(next_day, 'end')
                if (
                    next_day - end_date
                ).total_seconds() > 32400 and not end_date.date() == next_day.date():
                    next_day = next_day - timedelta(days=1)
                    next_day = self.calc_next_day(next_day, 'end')
                else:
                    next_day = end_date

        return next_day

    def calc_next_day(
        self, date_value: datetime, date_type: str, check_holiday=True
    ):
        next_day = date_value

        while check_holiday:
            check_holiday = (
                True
                if 1 in list(self.check_holiday([next_day]).values())
                else False
            )

            if not check_holiday:
                break

            if date_type == 'start':
                if next_day >= date_value:
                    next_day = datetime.strptime(
                        f'{next_day.year}{next_day.month}'
                        f'{next_day.day if len(str(next_day.day)) > 1 else f"0{next_day.day}"}080000',
                        '%Y%m%d%H%M%S',
                    )
                    next_day = next_day + timedelta(days=1)

            if date_type == 'end':
                if next_day <= date_value:
                    next_day = datetime.strptime(
                        f'{next_day.year}{next_day.month}'
                        f'{next_day.day if len(str(next_day.day)) > 1 else f"0{next_day.day}"}170000',
                        '%Y%m%d%H%M%S',
                    )
                    next_day = next_day - timedelta(days=1)

        return next_day

    def calculate_business_days(self, holiday: dict) -> int:
        diff_days = (self.end_date - self.start_date).days

        if holiday['public'] > 0 or holiday['weekend'] > 0:
            diff_days = diff_days - holiday['public'] - holiday['weekend']

        return diff_days

    @staticmethod
    def check_holiday(dates: List[datetime]) -> dict:
        pub = 0
        weekend = 0

        for date in dates:
            if date in holidays.ZA() and date.weekday() in [5, 6]:
                pub += 1
            elif date.weekday() in [5, 6]:
                weekend += 1
            elif date in holidays.ZA():
                pub += 1

        return {
            'public': pub,
            'weekend': weekend,
        }

    def holidays(self, start_date: datetime, end_date: datetime):
        diff_days = (end_date - start_date).days
        dates_in_between = []

        while diff_days > 0:
            dates_in_between = dates_in_between + [
                start_date + timedelta(days=diff_days)
            ]
            diff_days -= 1

        check_holidays = self.check_holiday(dates_in_between)
        start_hol = (
            True
            if 1
            in list(
                self.check_holiday([start_date + timedelta(days=1)]).values()
            )
            else False
        )
        end_hol = (
            True
            if 1 in list(self.check_holiday([end_date]).values())
            else False
        )

        check_holidays.update({'start_hol': start_hol, 'end_hol': end_hol})

        return check_holidays
