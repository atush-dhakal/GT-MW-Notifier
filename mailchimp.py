import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError
import json

# API Reference https://github.com/mailchimp/mailchimp-marketing-python

MAILCHIMP_API_KEY = '07e52c121142f3edf41a47ce23113d80-us7'
MAILCHIMP_SERVER_PREFIX = 'us7'
GT_ON_CAMPUS_LIST_NAME = 'GT On-Campus Jobs'
GT_ON_CAMPUS_LIST_ID = 'a79502d6f8'

class OnCampusJobList():
    def __init__(self):
        self._client = self.get_mailchimp_client()
        self._info = None
        self._members = None
                
    def get_mailchimp_client(self) -> MailchimpMarketing.Client:
        try:
            client = MailchimpMarketing.Client()
            client.set_config({
                "api_key": MAILCHIMP_API_KEY,
                "server": MAILCHIMP_SERVER_PREFIX
            })
            return client        

        except ApiClientError as error:
            print(error)
            return None

    def get_info(self):
        if self._info is None:
            mailchimp_lists = self._client.lists.get_all_lists()['lists']    
            gt_on_campus_list = list(filter(lambda x: x['name'] == GT_ON_CAMPUS_LIST_NAME, mailchimp_lists))
            if len(gt_on_campus_list) == 1:
                self._info = gt_on_campus_list[0]                
            else:
                raise f"Failed to find a unique list for '{GT_ON_CAMPUS_LIST_ID}'"
       
        return self._info

    def get_members(self):
        if self._members is None:
            list_id = self.get_info()['id']
            self._members = self._client.lists.get_list_members_info(list_id)['members']
        
        return self._members

def get_email_addresses():
    custom_list = OnCampusJobList()
    members = custom_list.get_members()
    return [x['email_address'] for x in members]

print(get_email_addresses())


