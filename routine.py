from jira import JIRA
import cgi
import re
import urllib3
import requests
import sys

class routine:
    def __init__(self, jira_user, jira_password):
      requests.packages.urllib3.disable_warnings()
      self.jira_user = jira_user
      self.jira_password = jira_password
      self.jira_server = 'https://carousell.atlassian.net'
      self.cs_board = 53
      self.jira_authentication()
      self.get_cs_current_sprint()
      self.get_cs_future_sprint()

    def jira_authentication(self):
      options = {
          'server': self.jira_server,
          'verify': False
      }
      jira = JIRA(options, basic_auth=(self.jira_user, self.jira_password))
      self.jira=jira
      print "authentication success"

    def  get_cs_current_sprint(self):
      r=self.jira._session.get(self.jira_server+'/rest/agile/1.0/board/'+str(self.cs_board)
        +'/sprint?state=active')
      self.current_sprint_id=r.json().get('values')[0].get('id')
      return self.current_sprint_id,str(self.get_sprint_name(self.current_sprint_id))

    def  get_cs_future_sprint(self):
      r=self.jira._session.get(self.jira_server+'/rest/agile/1.0/board/'+str(self.cs_board)
        +'/sprint?state=future')
      self.future_sprint_id=r.json().get('values')[0].get('id')
      return self.future_sprint_id,str(self.get_sprint_name(self.future_sprint_id))

    def get_sprints(self):
      sprint_info=self.jira.sprints(self.cs_board)
      return sprint_info

    def get_sprint_name(self,sprintid):
      sprints = {}
      for s in self.jira.sprints(self.cs_board):
        if s.id == sprintid:
          return s.name

    def get_issue_summary(self,issue):
          jiraissue = self.jira.issue(issue)
      summary = str(jiraissue.fields.summary)
      return summary

    def get_epic_link(self,issue):
      jiraissue = self.jira.issue(issue)
      epic_link=str(jiraissue.fields.customfield_10015)
      return epic_link

    def get_components(self,issue):
      jiraissue = self.jira.issue(issue)
      components= jiraissue.fields.components
      return components

    def get_description(self,issue):
      jiraissue = self.jira.issue(issue)
      description= jiraissue.fields.description
      return description

    def get_labels(self,issue):
      jiraissue = self.jira.issue(issue)
      labels= jiraissue.fields.labels
      return labels

    def get_QA_point(self,issue):
          jiraissue = self.jira.issue(issue)
      QA_point=jiraissue.fields.customfield_11765
      print "{} QA point for ticekt {}".format(QA_point,issue)
      return QA_point

    def calculate_QA_point(self, list_tickets=[]):
          sum=0
          print list_tickets
          for issue in list_tickets:
          sum+=self.get_QA_point(issue)
      return sum

    def create_issue_link(self, parentkey, childkey ):
            # create jira issue link(outwardIssue:parent-issue,inwardIssue=child-issue )
      self.jira.create_issue_link(type="relates to",inwardIssue=childkey,outwardIssue=parentkey)
      print  "successfully create issue link relating {} to {} ".format(parentkey,childkey)

    def create_issue_links(self, parentkeys, childkeys ):
          for i in range (len(parentkeys)):
            self.create_issue_link(parentkeys[i],childkeys[i])


    def create_one_task(self,project_key, issue, prefix):
      description=self.get_description(issue)
      epic_link=self.get_epic_link(issue)
      summary=self.get_issue_summary(issue)
      labels=self.get_labels(issue)
      existingLabels=[]
      existingComponents = []
      task= {
              'project': {'key': "CS"},
              'summary': prefix+' - '+summary,
              'description': description,
              'issuetype': { 'name' : 'Task' },
              'assignee' : { 'name' : 'daisy.liu' },
              'customfield_10015': epic_link,
            'labels': labels

          }
      task = self.jira.create_issue(fields=task)

      for component in self.get_components(issue):
          existingComponents.append({"name" : component.name})
      task.update(fields={"components": existingComponents})

      return task

    def create_bug(self, project_key ,assignee, summary, description):
      bugs = []
      for i in range (0, len(description)) :
        bug= {
              'project': {'key': project_key},
              'summary': summary[i],
              'description': description[i],
              'issuetype': { 'name' : 'Bug' },
              'assignee' : { 'name' : assignee[i] }
          }
        bugs.append(bug)
      issues = self.jira.create_issues(field_list=bugs)
      print "successfully create cs bugs"
      return [ issue.get('issue').key for issue in issues]


    def create_story(self, assignee, summary, description):
      storys = []
      for i in range (0, len(description)) :
        story= {
              'project': {'key': 'QA'},
              'summary': summary[i],
              'description': description[i],
              'issuetype': { 'name' : 'Story' },
              'assignee' : { 'name' : assignee[i] }
          }
        storys.append(story)
      issues = self.jira.create_issues(field_list=storys)
      print "successfully create Story"
      return [ issue.get('issue').key for issue in issues]

    def add_issues_to_sprint(self, sprint_id ,list_tickets=[]):
      list_issue_id=[]
      for issue in list_tickets:
        jiraissue = self.jira.issue(issue)
        list_issue_id.append(jiraissue.id)
      self.jira.add_issues_to_sprint( sprint_id, list_issue_id)
      print  "successfully add to sprint %s" % (self.get_sprint_name(sprint_id))

    def add_attachment(self, ticket , filepath):
      jiraissue = self.jira.issue(ticket)
      self.jira.add_attachment(issue=jiraissue, attachment=filepath)
      print "successfully upload file attachment"

    def search_current_sprint_issue(self):
          self.get_cs_current_sprint()
      print "current sprint id is {}".format(self.current_sprint_id)
      current_sprint_untested_issue_JQL = 'project = CS AND Sprint = {}'.format(self.current_sprint_id)
      issues=self.jira.search_issues(current_sprint_untested_issue_JQL)
      for issue in issues:
            print "In this sprint, ticket_id is {} and ticket key is {}".format(issue.id , issue.key)
      return [ issue.key for issue in issues]

    def search_current_sprint_test_done(self):
      self.get_cs_current_sprint()
      print "current sprint id is {}".format(self.current_sprint_id)
      current_sprint_test_done_JQL = 'project = CS AND issuetype in (Bug, Story) AND status in ("In Acceptance Testing", "Deployed" ) AND Sprint = {}'.format(self.current_sprint_id)
      issues=self.jira.search_issues(current_sprint_test_done_JQL)
      for issue in issues:
            print "test done ticket_id is {} and ticket key is {}".format( issue.id , issue.key)
      return [ issue.key for issue in issues]


    def search_current_sprint_untested_issue(self, testing_type):
      self.get_cs_current_sprint()
      print "current sprint id is {}".format(self.current_sprint_id)
      current_sprint_untested_issue_JQL = 'project = CS AND issuetype in (Bug, Story) AND status in ("{}") AND Sprint = {}'.format(testing_type,self.current_sprint_id)
      issues=self.jira.search_issues(current_sprint_untested_issue_JQL)
      for issue in issues:
            print "untested {} ticket_id is {} and ticket key is {}".format(testing_type, issue.id , issue.key)
      return [ issue.key for issue in issues]


    def create_untested_tasks(self,prefix,list_tickets=[]):
      tasks_key=[]
      for issue in list_tickets:
        jiraissue=self.jira.issue(issue)
        task=self.create_one_task('CS',jiraissue, prefix)
        tasks_key.append(task.key)
        print "create task key {} from story key {}".format(task.key,jiraissue.key)
      return tasks_key

    def get_transitions(self,ticket):
      jiraissue = self.jira.issue(ticket)
      transitions = self.jira.transitions(jiraissue)
      print [(t['id'], t['name']) for t in transitions]
      return transitions

    def transition_issues(self,list_tickets=[]):
        # Story in Test [(u'101', u'Archive'), (u'111', u'To Do'), (u'41', u'For Acceptance Testing'), (u'61', u'Reopen')]
      # Story in Accept [(u'101', u'Archive'), (u'111', u'To Do'), (u'51', u'Accept'), (u'61', u'Reopen')]
      # Bug in Test only (u'101', u'Archive'), (u'111', u'To Do'), (u'71', u'Accept'), (u'61', u'Reopen')]
      for issue in list_tickets:
        jiraissue = self.jira.issue(issue)
        transitions=self.get_transitions(issue)
        if transitions[2]['id']== "41":
          self.jira.transition_issue(jiraissue, '41' )
          self.jira.transition_issue(jiraissue, '51' )
        if transitions[2]['id']== "51":
          self.jira.transition_issue(jiraissue, '51' )
        if transitions[2]['id']== "71":
          self.jira.transition_issue(jiraissue, '71' )
        print "succefully move story {} to Done".format(issue)

    def auto_createTask_MoveTickets(self):
      # # search story tickets in Acceptance test and In testing or bug ticket in testing
      untest_acceptance_keys=self.search_current_sprint_untested_issue('In Acceptance Testing')
      untest_test_keys=self.search_current_sprint_untested_issue('In Testing')

      # # create tasks (label, component, epic link, summary ,description)
      tasks_acceptance_key=self.create_untested_tasks('Acceptance', untest_acceptance_keys )
      tasks_test_key=self.create_untested_tasks('Test',untest_test_keys)

      # # update tasks to future sprint
      self.add_issues_to_sprint(self.future_sprint_id,tasks_acceptance_key)
      self.add_issues_to_sprint(self.future_sprint_id,tasks_test_key)

      # # link issue to original tickets
      self.create_issue_links(untest_acceptance_keys,tasks_acceptance_key)
      self.create_issue_links(untest_test_keys,tasks_test_key)

      # move tickets to done
      self.transition_issues(untest_acceptance_keys)
      self.transition_issues(untest_test_keys)



if __name__ == "__main__":
  # {In Acceptance Testing}
  # {In Testing}
  # routine1.auto_createTask_MoveTickets()
