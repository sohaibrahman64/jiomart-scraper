# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import gspread
import json
from gspread import Cell


class JiomartscraperPipeline:

    def __init__(self):
        gc = gspread.service_account()
        sheet = gc.open("JioMart Products")
        worksheet_list = sheet.worksheets()
        self.worksheet = sheet.worksheet(worksheet_list[0].title)
        self.items = dict()
        self.list_items = list()

    def write_to_google_sheet_new(self):
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
        self.write_to_google_sheet_new()
        return item
