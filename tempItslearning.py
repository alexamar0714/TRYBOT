
from bs4 import BeautifulSoup
from urllib.request import urlopen
from robobrowser import RoboBrowser

class Browser(RoboBrowser):

    def get_text(self):
        return self.parsed.get_text()




class_id2 = '58af27f1e03422c1'
class_id = "input_fields"
url = 'http://ilearn.sexy'
url2 = 'https://ntnu.itslearning.com/ContentArea/ContentArea.aspx?LocationID=64756&LocationType=1'
url3 = 'https://ntnu.itslearning.com/essay/read_essay.aspx?EssayID=3222889'
#content = urlopen(url).read()
#soup = BeautifulSoup(content)

br = Browser()
br.open(url)
signup_form = br.get_form()
#signup_form

passwd = input("passwd?")
signup_form['feidename'].value = 'alexamar'
signup_form['password'].value = passwd
br.submit_form(signup_form)

m = br.get_form()
br.submit_form(m)
br.open(url2)
br.open(url3)
soup = BeautifulSoup(br, "html.parser")


print(soup)
