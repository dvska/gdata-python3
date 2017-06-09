#
# Copyright (C) 2007 Google Inc.
#
# Licensed under the Apache License 2.0;


# # __author__ = 'api.laurabeth@gmail.com (Laura Beth Lincoln)'

import getpass
import unittest

import gdata.service
import gdata.spreadsheet
import gdata.spreadsheet.service

username = ''
password = ''
ss_key = ''
ws_key = ''


class DocumentQueryTest(unittest.TestCase):
    def setUp(self):
        self.query = gdata.spreadsheet.service.DocumentQuery()

    def testTitle(self):
        self.query['title'] = 'my title'
        self.assertTrue(self.query['title'] == 'my title')
        self.assertTrue(self.query.ToUri() == '?title=my+title')

    def testTitleExact(self):
        self.query['title-exact'] = 'true'
        self.assertTrue(self.query['title-exact'] == 'true')
        self.assertTrue(self.query.ToUri() == '?title-exact=true')


class CellQueryTest(unittest.TestCase):
    def setUp(self):
        self.query = gdata.spreadsheet.service.CellQuery()

    def testMinRow(self):
        self.query['min-row'] = '1'
        self.assertTrue(self.query['min-row'] == '1')
        self.assertTrue(self.query.ToUri() == '?min-row=1')

    def testMaxRow(self):
        self.query['max-row'] = '100'
        self.assertTrue(self.query['max-row'] == '100')
        self.assertTrue(self.query.ToUri() == '?max-row=100')

    def testMinCol(self):
        self.query['min-col'] = '2'
        self.assertTrue(self.query['min-col'] == '2')
        self.assertTrue(self.query.ToUri() == '?min-col=2')

    def testMaxCol(self):
        self.query['max-col'] = '20'
        self.assertTrue(self.query['max-col'] == '20')
        self.assertTrue(self.query.ToUri() == '?max-col=20')

    def testRange(self):
        self.query['range'] = 'A1:B4'
        self.assertTrue(self.query['range'] == 'A1:B4')
        self.assertTrue(self.query.ToUri() == '?range=A1%3AB4')

    def testReturnEmpty(self):
        self.query['return-empty'] = 'false'
        self.assertTrue(self.query['return-empty'] == 'false')
        self.assertTrue(self.query.ToUri() == '?return-empty=false')


class ListQueryTest(unittest.TestCase):
    def setUp(self):
        self.query = gdata.spreadsheet.service.ListQuery()

    def testSpreadsheetQuery(self):
        self.query['sq'] = 'first=john&last=smith'
        self.assertTrue(self.query['sq'] == 'first=john&last=smith')
        self.assertTrue(self.query.ToUri() == '?sq=first%3Djohn%26last%3Dsmith')

    def testOrderByQuery(self):
        self.query['orderby'] = 'column:first'
        self.assertTrue(self.query['orderby'] == 'column:first')
        self.assertTrue(self.query.ToUri() == '?orderby=column%3Afirst')

    def testReverseQuery(self):
        self.query['reverse'] = 'true'
        self.assertTrue(self.query['reverse'] == 'true')
        self.assertTrue(self.query.ToUri() == '?reverse=true')


class SpreadsheetsServiceTest(unittest.TestCase):
    def setUp(self):
        self.key = ss_key
        self.worksheet = ws_key
        self.gd_client = gdata.spreadsheet.service.SpreadsheetsService()
        self.gd_client.email = username
        self.gd_client.password = password
        self.gd_client.source = 'SpreadsheetsClient "Unit" Tests'
        self.gd_client.ProgrammaticLogin()

    def testGetSpreadsheetsFeed(self):
        entry = self.gd_client.GetSpreadsheetsFeed(self.key)
        self.assertTrue(isinstance(entry, gdata.spreadsheet.SpreadsheetsSpreadsheet))

    def testGetWorksheetsFeed(self):
        feed = self.gd_client.GetWorksheetsFeed(self.key)
        self.assertTrue(isinstance(feed, gdata.spreadsheet.SpreadsheetsWorksheetsFeed))
        entry = self.gd_client.GetWorksheetsFeed(self.key, self.worksheet)
        self.assertTrue(isinstance(entry, gdata.spreadsheet.SpreadsheetsWorksheet))

    def testGetCellsFeed(self):
        feed = self.gd_client.GetCellsFeed(self.key)
        self.assertTrue(isinstance(feed, gdata.spreadsheet.SpreadsheetsCellsFeed))
        entry = self.gd_client.GetCellsFeed(self.key, cell='R5C1')
        self.assertTrue(isinstance(entry, gdata.spreadsheet.SpreadsheetsCell))

    def testGetListFeed(self):
        feed = self.gd_client.GetListFeed(self.key)
        self.assertTrue(isinstance(feed, gdata.spreadsheet.SpreadsheetsListFeed))
        entry = self.gd_client.GetListFeed(self.key, row_id='cpzh4')
        self.assertTrue(isinstance(entry, gdata.spreadsheet.SpreadsheetsList))

    def testUpdateCell(self):
        self.gd_client.UpdateCell(row='5', col='1', inputValue='', key=self.key)
        self.gd_client.UpdateCell(row='5', col='1', inputValue='newer data',
                                  key=self.key)

    def testBatchUpdateCell(self):
        cell_feed = self.gd_client.GetCellsFeed(key=self.key)
        edit_cell = cell_feed.entry[0]
        old_cell_value = 'a1'

        # Create a batch request to change the contents of a cell.
        batch_feed = gdata.spreadsheet.SpreadsheetsCellsFeed()
        edit_cell.cell.inputValue = 'New Value'
        batch_feed.AddUpdate(edit_cell)
        result = self.gd_client.ExecuteBatch(batch_feed,
                                             url=cell_feed.GetBatchLink().href)
        self.assertEqual(len(result.entry), 1)
        self.assertEqual(result.entry[0].cell.inputValue, 'New Value')

        # Make a second batch request to change the cell's value back.
        edit_cell = result.entry[0]
        edit_cell.cell.inputValue = old_cell_value
        batch_feed = gdata.spreadsheet.SpreadsheetsCellsFeed()
        batch_feed.AddUpdate(edit_cell)
        restored = self.gd_client.ExecuteBatch(batch_feed,
                                               url=cell_feed.GetBatchLink().href)
        self.assertEqual(len(restored.entry), 1)
        self.assertEqual(restored.entry[0].cell.inputValue, old_cell_value)

    def testInsertUpdateRow(self):
        entry = self.gd_client.InsertRow({'a1': 'new', 'b1': 'row', 'c1': 'was',
                                          'd1': 'here'}, self.key)
        entry = self.gd_client.UpdateRow(entry, {'a1': 'newer',
                                                 'b1': entry.custom['b1'].text, 'c1': entry.custom['c1'].text,
                                                 'd1': entry.custom['d1'].text})
        self.gd_client.DeleteRow(entry)

    def testWorksheetCRUD(self):
        # Add a new worksheet.
        new_worksheet = self.gd_client.AddWorksheet('worksheet_title_test_12', '2',
                                                    3, self.key)
        self.assertEqual(new_worksheet.col_count.text, '3')
        self.assertEqual(new_worksheet.row_count.text, '2')
        self.assertEqual(new_worksheet.title.text, 'worksheet_title_test_12')

        # Change the dimensions and title of the new worksheet.
        new_worksheet.col_count.text = '1'
        new_worksheet.title.text = 'edited worksheet test12'
        edited_worksheet = self.gd_client.UpdateWorksheet(new_worksheet)
        self.assertEqual(edited_worksheet.col_count.text, '1')
        self.assertEqual(edited_worksheet.row_count.text, '2')
        self.assertEqual(edited_worksheet.title.text, 'edited worksheet test12')

        # Delete the new worksheet.
        result = self.gd_client.DeleteWorksheet(edited_worksheet)
        self.assertEqual(result, True)


if __name__ == '__main__':
    print('Spreadsheet Tests\nNOTE: Please run these tests only with a test '
          'account. The tests may delete or update your data.')
    print('These tests must be run on a sheet with this data:\n'
          'a1,b1,c1,d1\n'
          '1,2,3,4')
    username = input('Please enter your username: ')
    password = getpass.getpass()
    ss_key = input('Please enter your spreadsheet key: ')
    ws_key = input('Please enter your worksheet key (usually od6): ')
    unittest.main()
