import csv
import datetime as dt
from collections import defaultdict
from pathlib import Path

from .utils import rename_first_row


BASE_DIR = Path(__file__).parent.parent / 'results'


class PepParsePipeline:
    def open_spider(self, spider):
        self.status_counts = defaultdict(int)

    def process_item(self, item, spider):
        status = item['status']
        self.status_counts[status] += 1
        return item

    def close_spider(self, spider):
        timestamp = dt.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f'status_summary_{timestamp}.csv'

        fieldnames = ['Статус', 'Количество']

        with (BASE_DIR / filename).open('w', encoding='utf-8',
                                        newline='') as file:
            writer = csv.writer(file)
            writer.writerow(fieldnames)
            writer.writerows(self.status_counts.items())
            writer.writerow(['Total', sum(self.status_counts.values())])

        rename_first_row()
