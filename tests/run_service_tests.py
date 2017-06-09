import getopt
import getpass
import sys

# Modules whose tests we will run.
from . import atom_tests
from .gdata_test import service_test
from .gdata_test.apps import  service_test
#TODO FIXME
.blogger. import  service_test
.calendar.service_test
.contacts.profiles.service_test
.contacts.service_test
.docs.service_test
.photos.service_test
.service_test
.spreadsheet.service_test
.spreadsheet.text_db_test
from . import gdata_tests.youtube.service_test
from . import module_test_runner


def RunAllTests(username, password, spreadsheet_key, worksheet_key,
                apps_username, apps_password, apps_domain):
    test_runner = module_test_runner.ModuleTestRunner()
    test_runner.modules = [atom_tests.service_test,
                           gdata_tests.service_test,
                           gdata_tests.apps.service_test,
                           gdata_tests.calendar.service_test,
                           gdata_tests.docs.service_test,
                           gdata_tests.spreadsheet.service_test,
                           gdata_tests.spreadsheet.text_db_test,
                           gdata_tests.contacts.service_test,
                           gdata_tests.youtube.service_test,
                           gdata_tests.photos.service_test,
                           gdata_tests.contacts.profiles.service_test, ]
    test_runner.settings = {'username': username, 'password': password,
                            'test_image_location': 'testimage.jpg',
                            'ss_key': spreadsheet_key,
                            'ws_key': worksheet_key,
                            'apps_username': apps_username,
                            'apps_password': apps_password,
                            'apps_domain': apps_domain}
    test_runner.RunAllTests()


def GetValuesForTestSettingsAndRunAllTests():
    username = ''
    password = ''
    spreadsheet_key = ''
    worksheet_key = ''
    apps_domain = ''
    apps_username = ''
    apps_password = ''

    print('NOTE: Please run these tests only with a test account. '
          'The tests may delete or update your data.')
    try:
        opts, args = getopt.getopt(sys.argv[1:], '', ['username=', 'password=',
                                                      'ss_key=', 'ws_key=',
                                                      'apps_username=',
                                                      'apps_password=',
                                                      'apps_domain='])
        for o, a in opts:
            if o == '--username':
                username = a
            elif o == '--password':
                password = a
            elif o == '--ss_key':
                spreadsheet_key = a
            elif o == '--ws_key':
                worksheet_key = a
            elif o == '--apps_username':
                apps_username = a
            elif o == '--apps_password':
                apps_password = a
            elif o == '--apps_domain':
                apps_domain = a
    except getopt.GetoptError:
        pass

    if username == '' and password == '':
        print('Missing --user and --pw command line arguments, '
              'prompting for credentials.')
    if username == '':
        username = input('Please enter your username: ')
    if password == '':
        password = getpass.getpass()
    if spreadsheet_key == '':
        spreadsheet_key = input(
            'Please enter the key for the test spreadsheet: ')
    if worksheet_key == '':
        worksheet_key = input(
            'Please enter the id for the worksheet to be edited: ')
    if apps_username == '':
        apps_username = input('Please enter your Google Apps admin username: ')
    if apps_password == '':
        apps_password = getpass.getpass()
    if apps_domain == '':
        apps_domain = input('Please enter your Google Apps domain: ')
    RunAllTests(username, password, spreadsheet_key, worksheet_key,
                apps_username, apps_password, apps_domain)


if __name__ == '__main__':
    GetValuesForTestSettingsAndRunAllTests()
