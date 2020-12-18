import logging

from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime, timezone
from simple_salesforce import Salesforce

import config
import package_logger

from symphony.bot_client import BotClient

package_logger.initialize_logging()

def run_sched():
    scheduler = BlockingScheduler()
    scheduler.add_job(run_main, 'cron', hour=1)

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit) as ex:
        logging.info(f'Exiting process...{ex}')

def run_main():

    try:
        users = get_cp2_users()
        update_sfdc_last_login(users)

        logging.info('Update Complete.')
    except Exception as ex:
        logging.exception(ex)

def get_cp2_users():
    logging.info('Downloading CP2 User List...')
    symclient = BotClient(config.bot_config)

    user_list = symclient.Admin.list_users()

    users = []
    for user in user_list:
        u = {
            "id": user['userSystemInfo']['id'],
            "username": user['userAttributes']['userName'],
            "company": user['userAttributes'].get('division'),
            "last_login": parse_last_login(user['userSystemInfo'].get('lastLoginDate'))
        }

        users.append(u)

    return users

def update_sfdc_last_login(user_list):
    logging.info('Updating Contacts in Salesforce...')
    sfdc = Salesforce(username=config.salesforce['username'], password=config.salesforce['password'],
                      security_token=config.salesforce['security_token'])

    contact_list_soql = "SELECT Id, Email, Symphony_CP_User_Id__c FROM Contact WHERE Account.Type = 'Community Connect'"

    contact_dict = {c['Email']: c for c in sfdc.query_all(contact_list_soql)['records']}

    contacts_for_update = []
    for user in user_list:
        username = user['username']

        contact = contact_dict.get(username)

        if contact:
            c = {
                "Id": contact['Id'],
                "Symphony_Last_Login__c": user['last_login']
            }

            if not contact.get('Symphony_CP_User_Id__c'):
                c['Symphony_CP_User_Id__c'] = user['id']

            contacts_for_update.append(c)

    sfdc.bulk.Contact.update(contacts_for_update)


def parse_last_login(timestamp: int):
    if not timestamp:
        return None

    dt = datetime.fromtimestamp(timestamp/1000, timezone.utc)

    return dt.isoformat(timespec='seconds').replace('+00:00', 'Z')


if __name__ == '__main__':
    # run_main()
    run_sched()
