# from jira_routine_job import  *
import logging
import os
import photo_merge

class parsetxtfile:
		def __init__(self, file_path):
			self.parser_des=[]
			self.parser_summary=[]
			self.parser_assignee=[]
			self.parser_photos=[]  #[[A,B,C],[D,E,F]]
			self.flag=-1
			self.des=""
			self.summary=""
			self.assignee="" 
			self.photos=[]
			self.parse_file(file_path)

			print  self.parser_des
			print  self.parser_summary
			print  self.parser_assignee
			print  self.parser_photos

 
		def  check_parser_key(self, line):
			if self.flag == 1:
				line=line+"\n"
				self.des+=line
			elif self.flag== 2 :
				line+="\n"
				self.summary+=line
			elif self.flag== 3 :
				self.assignee+=line
			elif self.flag== 4 and line:
				photo_list=[x for x in line.strip().split(',')]
				self.photos+=photo_list


		def  check_content_exist(self):		
			if  self.des != "":
				self.parser_des.append(self.des)
				self.des = ""
			if self.summary != "":
				self.parser_summary.append(self.summary)
				self.summary = ""
			if self.assignee != "":
				self.parser_assignee.append(self.assignee)
				self.assignee=""
			if  self.photos :
				self.parser_photos.append(self.photos)
				self.photos=[]

		def parse_file(self,file_path):
			with open(file_path) as  f:
				for  line  in iter(f):
					line =line.rstrip()
					if line.startswith('@des') or line.startswith('@summary') or line.startswith('@assignee') \
					or line.startswith('!exit') or line.startswith('@photos'):
						if line.startswith('@des'):
							self.check_content_exist()
							self.flag=1
						elif line.startswith('@summary'):
							self.check_content_exist()
							self.flag=2
						elif line.startswith('@assignee'):
							self.check_content_exist()
							self.flag=3
						elif line.startswith('@photos'):
							self.check_content_exist()
							self.flag=4
						else :
							self.check_content_exist()
					else:
						self.check_parser_key(line)

			if len(self.parser_des) != len(self.parser_assignee) or  len(self.parser_des)==0  or len(self.parser_assignee)==0:
				raise  "parser description size is not match with parser assignee size"
				# raise "test_step size %d and test data result %d len not matches" % ( len(test_step), len(test_result))

if __name__ == "__main__":

		# file_path=os.path.join(
        # os.path.dirname(os.path.abspath(__file__)), 'uploads', 'parser.txt')
		jiraparser1=parsetxtfile('story.txt')
		



