# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import gspread
import json
from gspread import Cell
from gspread.exceptions import WorksheetNotFound


class JiomartscraperPipeline:

    def __init__(self):
        self.gc = gspread.service_account()
        self.sheet = self.gc.open("JioMart Products")
        self.worksheet_list = self.sheet.worksheets()
        self.worksheet = None
        self.items = dict()
        self.list_items = list()

    def write_to_sheet(self, sheet_name):
        try:
            self.worksheet = self.sheet.worksheet(sheet_name)
        except WorksheetNotFound:
            self.worksheet = self.sheet.add_worksheet(title=sheet_name, rows=1000, cols=4)

        cells = []
        for i in range(len(self.list_items)):
            item = self.list_items[i]
            for j, key in enumerate(item):
                if i == 0:
                    if j == 0:
                        cells.append(Cell(row=i + 1, col=j + 1, value='Name'))
                    elif j == 1:
                        cells.append(Cell(row=i + 1, col=j + 1, value='Selling Price'))
                    elif j == 2:
                        cells.append(Cell(row=i + 1, col=j + 1, value='Original Price'))
                    elif j == 3:
                        cells.append(Cell(row=i + 1, col=j + 1, value='Product Image'))
                else:
                    if key == 'image':
                        command = f'''=IMAGE("{item[key]}", 1)'''
                        cells.append(Cell(row=i + 1, col=j + 1, value=command))
                    else:
                        cells.append(Cell(row=i + 1, col=j + 1, value=item[key]))
        self.worksheet.update_cells(cells, value_input_option='USER_ENTERED')
        pass

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        self.list_items.append(adapter.asdict())
        if spider.name == 'groceries':
            self.write_to_sheet('Groceries')
        elif spider.name == 'home-kitchen':
            self.write_to_sheet('Home And Kitchen')
        return item
