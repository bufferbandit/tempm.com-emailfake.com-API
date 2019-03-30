from urllib.request import build_opener, HTTPCookieProcessor, Request
from xml.etree.ElementTree import ElementTree
from lxml import etree,html
from pprint import pprint


def get_emails(email=None,only_last_email=False,):
		
		session = build_opener(HTTPCookieProcessor())
		base_url="http://tempm.com"
		
		if email:
			username,domain = email.split("@")
			r = session.open( "{base_url}/{domain}/{username}".format(
               base_url=base_url,
			   username=username,	
			   domain=domain
				)
			)
		else:
			r = session.open(base_url)
			
		tree = etree.HTML(r.read().decode("utf-8"))
		email_urls = []
		emails = []
		email_addr = tree.xpath("//span[@id='email_ch_text']")[0].text
		
		try:
			email_urls = []
			collected_emails =  tree.xpath("//div[@id='email-table']")[0].getchildren()
			for email_path_url in collected_emails:
					
				try:
					email_url = base_url + "/" + email_path_url.attrib["href"]
					_xpath = "//div[@id='iddelet2']"
					_break = False
				except KeyError:
					email_url = base_url
					_xpath = "//div[@class='e7m row list-group-item']"
					_break = True
					
				email_urls.append(email_url)
				
				r = session.open(email_url)
				tree2 = etree.HTML(r.read().decode("utf-8"))
				
				_html = tree2.xpath(_xpath)[0]
				
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
				emails.append(email_meta)
				if _break or only_last_email:break
				else:continue

			email_urls = email_urls	
			email_urls = list(set(email_urls))
			#emails = [i for n, i in enumerate(emails) if i not in emails[n + 1:]]
		except IndexError:
			pass
    
		finally:
			return {"email_addr":email_addr,"inbox":emails}
        
