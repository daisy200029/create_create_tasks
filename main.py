
'''
    A Test helper tool for carousell tester.
    * Description:
    This tool enables you to do some actions easier and quicker.
    Basically you just type specific command to do.
    If you don't know how to use it and how many command you can use,
    Just type help, and you will get all commands you can use:
    Or if you want to know how to use the specific command:
    Just type help <command name>
    
    * Current commands (type help <topic>):
    ========================================
    bump_onetime  get_token  get_userid  help  list  list_by_user  register
    
    '''
import requests
import json
import cmd
import webbrowser
from parsetxtfile  import parsetxtfile
from routine import routine
from photo_merge  import photo_merge

# Created by Jerry
class CarousellTestShell(cmd.Cmd):
    '''
        A CarousellTestShell class.
        All method which start from do_ will be consider as a feature command.
        so if let's say you want to create a command:
        Just do this as below:
        
        def do_XXX(self, args):
        ...
        ...
        
        After you created that, then you can use that XXX as a command.
        '''
    # All paramete
    base_url = "https://icetea.carousell.com"
    token = ""
    headers = {'Authorization': ''}
    api_key_bump = \
        'Iwn55O6N7rOWyepXck7UfcmgMlhjUxUoR8vJ2mC626emECaYp6JywZEtmiKGEm7'
    ticket_url='https://carousell.atlassian.net/browse/'

# ALL Endpoints
login_endpoint = "/api/2.0/login/"
    discover_endpoint = "/api/2.5/purchases/discover/"
    products_endpoint = "/api/2.0/products/?count={0}"
    my_products_endpoint = "/api/2.0/user/{0}/products"
    userid_endpoint = "/api/2.0/user/{0}/"
    offer_endpoint = "/api/2.0/offers/"
    register_endpoint = "/api/2.0/register/"
    bump_endpoint = "/api/2.5/helper/products/bump/"
    
    def do_get_token(self, args):
        '''
            Description: Get user token
            Example:
            get_token 001stage stage123
            Flow:
            request  -->
            token    <--
            '''
        try:
            usr,pwd = args.split()
            self.__login(usr,pwd)
        except:
            print 'login error = example: get_token 001stage, stage123'

def do_bump_onetime(self, pid):
    '''
        Description: bump product
        Example:
        bump <product id>
        '''
            try:
            data = {'api_key':self.api_key_bump, 'ids':str(pid)}
            res = requests.post(self.base_url + self.bump_endpoint, data)
            print 'bump success!!'
                except:
                    print 'bump error :  example: bump 4343'

def do_register(self, usr):
    '''
        Description: Do register and mail verification
        Example:
        register <new username>
        Flow:
        --> register --> send verification --> verify user automatic
        Output:
        successful if username can be registered
        '''
            try:
            self.__register(usr)
                except:
                    print 'try example: register <new_username>'

def do_get_userid(self,username):
    '''
        Description: Get user id
        Example:
        get_userid 001stage
        Flow:
        request -->
        userid  <--
        '''
            try:
            jsonstr = self.__get(self.userid_endpoint.format(username))
            print "{0} - {1}".format(jsonstr['username'],jsonstr['id'])
                except:
                    print "userid get error"

def do_list(self,args=40):
    '''
        Description: List all top of products by count
        Example:
        list 5
        Flow:
        request -->
        lists   <--
        Output:
        <2017-04-04T08:35:22Z> | [L] | [ID=3892] | 0.25 | Test
        <2017-04-03T07:57:22Z> | [L] | [ID=3819] | 250.00 | Heheheeh
        <2017-03-15T04:17:15Z> | [L] | [ID=2882] | 222.22 | COFFEE
        <2017-04-04T08:26:45Z> | [L] | [ID=3887] | 2.55 | Sdd
        <2017-04-04T08:18:42Z> | [L] | [ID=3882] | 0.25 | Twat
        '''
            try:
            self.__list_product(self.products_endpoint.format(args))
                except:
                    print "list error = example: list 5"

def do_list_by_user(self, usr):
    '''
        Desciption: List all product details by user
        Example:
        list_by_user 006stage
        Flow:
        request -->
        lists   <--
        Output:
        <2017-04-04T08:35:22Z> | [L] | [ID=3892] | 0.25 | Test
        <2017-04-03T07:57:22Z> | [L] | [ID=3819] | 250.00 | Heheheeh
        <2017-03-15T04:17:15Z> | [L] | [ID=2882] | 222.22 | COFFEE
        <2017-04-04T08:26:45Z> | [L] | [ID=3887] | 2.55 | Sdd
        <2017-04-04T08:18:42Z> | [L] | [ID=3882] | 0.25 | Twat
        '''
            try:
            self.__list_product(self.my_products_endpoint.format(usr))
                except:
                    print 'try example: list_by_user 002stage'

def do_offer(self, args):
    pid, price = args.split()
    data={'product_id':pid,'latest_price':price}
        jsonstr = self.__post(self.offer_endpoint, data)
        print jsonstr
    
    def do_create_bug(self,args):
        try:
            jira_user,  jira_password , project_key, text_bug_file = args.split()
            try:
                routine1=routine(jira_user,jira_password)
                try:
                    bug_parser=parsetxtfile(text_bug_file)
                    bug_tickets=routine1.create_bug(project_key=project_key,assignee=bug_parser.parser_assignee, \
                                                    summary=bug_parser.parser_summary, description=bug_parser.parser_des)
                                                    print bug_tickets
                                                    try:
                                                        for i in range (0,len(bug_tickets)):
                                                            if bug_parser.parser_photos[i][0]!='NULL':
                                                                photo_merge1 =photo_merge(photoNames=bug_parser.parser_photos[i])
                                                                routine1.add_attachment(bug_tickets[i],photo_merge1.final_photo)
                                                                    try:
                                                                        for bug in bug_tickets:
                                                                            webbrowser.open(self.ticket_url + bug)
                                                                                except:
                                                                                    print 'unable open browser'
                                                                                except:
                                                                                    print 'unable merge photo or upload photo'
                                                                                except:
                                                                                    print 'unanble create bug because wrong bug format'
        except:
            print 'Authorization fail, please check jira profile to see or reset on-demand password'
        except:
            print 'try example: create_bug {user_name} {passowrd} CS bug.txt' \
                'or try example: create_bug {user_name} {passowrd} ISSUERPTS bug.txt'


def do_create_story(self,args):
    try:
        jira_user,  jira_password, text_story_file = args.split()
        try:
            routine1=routine(jira_user,jira_password)
            try:
                #routine1.get_cs_future_sprint()
                story_parser=parsetxtfile(text_story_file)
                print "here!!"
                    print story_parser.parser_assignee
                    print story_parser.parser_summary
                    print story_parser.parser_des
                    story_tickets=routine1.create_story(assignee=story_parser.parser_assignee, \
                                                        summary=story_parser.parser_summary, description=story_parser.parser_des)
                                                        print "here2!!"
                                                        #routine1.add_issues_to_sprint(sprint_id=routine1.future_sprint_id \
                                                        #   ,list_tickets=story_tickets)
                                                        try:
                                                            for story in story_tickets:
                                                                webbrowser.open(self.ticket_url + story)
                                                            except:
                                                                print 'unable open browser'
                                                            except:
                                                                print 'unanble create ticket because wrong ticket format'
        except:
            print 'Authorization fail, please check jira profile to see or reset on-demand password'
        except:
            print 'try example: create_story {user_name} {passowrd} story.txt'


# private method
def __list_product(self, endpoint):
    r = ""
        jsonstr = self.__get(endpoint)
        #jsonstr = self.__get(self.my_products_endpoint.format(usr))
        if not endpoint:
            print 'please given a username as a parameter'
    else:
        r = jsonstr
            if 'Not found' in str(r):
                print 'user not exist!'
        else:
            for item in r:
                print "<{3}> | [{0}] | [ID={2}] | {4} | {1}".format(\
                                                                    item['status'],item['title'],\
                                                                    item['id'],item['time_created'],\
                                                                    item['price'])


def __login(self, usr, pwd):
    '''
        private method: this is a common method
        for user login action
        
        '''
            data={'username':usr,"password":pwd}
                jsonstr = self.__post(self.login_endpoint, data)
                token = jsonstr['token']
                self.headers['Authorization'] = "Token " +token
                print token

def __get(self, endpoint):
    '''
        private method: this is a common method
        for get request
        
        '''
            res = requests.get(
                               self.base_url + endpoint,
                               headers=self.headers,
                               )
                json_text = res.text
                    jsonstr = json.loads(json_text)
                    return jsonstr

def __post(self, endpoint, data):
    '''
        private method: this is a common method
        for post request
        
        '''
            res = requests.post(
                                self.base_url + endpoint,
                                data=data
                                )
                json_text =  res.text
                    jsonstr = json.loads(json_text)
                    return jsonstr

def __register(self,username):
    verifycode.verify_user(username, self.base_url + self.register_endpoint)
    
    def do_exit(self,*args):
        return True

if __name__ == '__main__':
    CarousellTestShell().cmdloop()
