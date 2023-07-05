import csv
import datetime as dt
from pathlib import Path

from .utils import rename_first_row


BASE_DIR = Path(__file__).parent.parent / 'results'


class PepParsePipeline:
    def open_spider(self, spider):
        self.status_counts = {}

    def process_item(self, item, spider):
        status = item['status']
        count = self.status_counts.get(status, 0)
        self.status_counts[status] = count + 1
        return item

    def close_spider(self, spider):
        timestamp = dt.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f'status_summary_{timestamp}.csv'

        fieldnames = ['Статус', 'Количество']

        with (BASE_DIR / filename).open('w', encoding='utf-8',
                                        newline='') as file:
            writer = csv.DictWriter(file, fieldnames)
            writer.writeheader()
            writer.writerows(
                {'Статус': key, 'Количество': value}
                for key, value in self.status_counts.items()
            )
            writer.writerow({'Статус': 'Total',
                             'Количество': sum(self.status_counts.values())})

        rename_first_row()
