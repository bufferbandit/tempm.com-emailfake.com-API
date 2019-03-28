from xml.etree.ElementTree import ElementTree
from lxml import etree,html

import requests


class TEMPM_API:

	def __init__(self,email=None):
		self.session = requests.session()
		if email:
			username,domain = email.split("@")
			r = self.session.get("https://tempm.com/{domain}/{username}".format(
			   username=username,	
			   domain=domain
				)
			)
		else:
			r = self.session.get("https://tempm.com")
			
		self.tree = etree.HTML(r.text)
		self.email_urls = []
		self.emails = []
		self.email_addr = self.tree.xpath("//span[@id='email_ch_text']")[0].text

		

	def get_emails(self):
		try:
			email_urls = []
			collected_emails =  self.tree.xpath("//div[@id='email-table']")[0].getchildren()
			for email_path_url in collected_emails:
				                
				try:
					email_url = "https://tempm.com" + email_path_url.attrib["href"]
					_xpath = "//div[@id='iddelet2']"
					_break = False
				except KeyError:
					email_url = "https://tempm.com"
					_xpath = "//div[@class='e7m row list-group-item']"
					_break = True
					
				email_urls.append(email_url)
				
				r = self.session.get(email_url)
				tree = etree.HTML(r.text)
				
				_html = tree.xpath(_xpath)[0]
				
				childs = _html.getchildren()
				
				meta_data = childs[0]
				body = childs[3]
				
				
				body_childs = meta_data.getchildren()
				
				
				email_meta = {
                    
                    "from_email" :  body_childs[4].text,
                    "received"   :  body_childs[10].text,
                    "to_email"   :  body_childs[1].text,
                    "subject"    :  body_childs[7][0].text,
                    "body"       :  body.getchildren()[2][0].text
                            
                            }
				self.emails.append(email_meta)
				if _break:break
				else:continue

			self.email_urls = email_urls	
			return email_urls	
		except IndexError: 
			return []      
