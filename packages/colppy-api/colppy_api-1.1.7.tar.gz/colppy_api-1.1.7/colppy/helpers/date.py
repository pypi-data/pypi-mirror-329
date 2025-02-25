from datetime import datetime

from dateutil.relativedelta import relativedelta

from colppy.helpers.logger import logger


class ColppyDate:
    def __init__(self) -> None:
        self.today = datetime.now()

    def get_today(self) -> str:
        logger.debug(f"Today: {self.today.strftime('%Y-%m-%d')}")
        return self.today.strftime("%Y-%m-%d")

    def get_months_ago(self, months: int) -> str:
        months_ago = self.today - relativedelta(months=months)
        logger.debug(f"{months} months ago: {months_ago.strftime('%Y-%m-%d')}")
        return months_ago.strftime("%Y-%m-%d")


if __name__ == '__main__':
    colppy_date = ColppyDate().get_months_ago(8)
