"""
This is the Python ItsLearning Scraper for the TRYBOT.
The purpose of this module is to serve as a fetching device to retrieve information
from ItsLearning.
To initiate, first call self.establish_connection().
Call self.bulletins() to retrieve the Bulletins of the main page.
Call self.initiate_exploration_of_folders() to explore the course's folders, and retrieve data with
self.get_data and self.get_pdf_data.

To write data to a file, user codecs.
"""




from robobrowser import RoboBrowser
import PyPDF2
from urllib.request import urlopen
from io import BytesIO


class Browser(RoboBrowser): #adds get_text() to Robobrowser to fetch text in a clearer way
    def get_text(self):
        return self.parsed.get_text() #is similar to Beautifoulsoup's get_text()

class Pils:

    def __init__(self, username, password):
        self.br = Browser()
        self.url1 = "http://ilearn.sexy" #URL to a site that bypasses Innsida
        self.url2 = "https://ntnu.itslearning.com/ContentArea/ContentArea.aspx?LocationID=64756&LocationType=1" #Course's main page
        self.url3 = "https://ntnu.itslearning.com/Course/course.aspx?CourseId=64756#" #Course's bulletins
        self.__username = username #ItsLearning username (for NTNU)
        self.__password = password #ItsLearning password
        self.data = []
        self.pdf_data = []
        self.explored_folders = []


    def establish_connection(self):

        """
        Establishes a connection to ItsLearning by logging through Feide.

        :return: False if connection cannot be established.
        :return: False if connection is successfully established.
        """

        try:
            self.br.open(self.url1)#connects to itslearning's feide portal
            feide_form = self.br.get_form()
            feide_form['feidename'].value = self.__username
            feide_form['password'].value = self.__password
            self.br.submit_form(feide_form)
            m = self.br.get_form()  # gets past the non-Javascript blocker
            self.br.submit_form(m)
            return True
        except:
            return False

    def get_bulletins(self):

        """
        Fetches the written content of all bulletins.

        :return: the text of all the bulletins.
        :return: False if fetching cannot be achieved.
        """

        try:
            self.br.open(self.url3) #gets the iframe of the course page, containing all Bulletins
            return self.br.get_text() #this is a big string
        except:
            return False

    def initiate_exploration_of_folders(self):

        """
        Initiates the exploration of folders.

        :return: False if initiation fails.
        :return: True if initiation succeeds.
        """

        try:
            self.br.open(self.url2)
            links = self.br.get_text()
            self.explore_folders(links)
            return True
        except:
            return False

    def explore_folders(self, string):

        """
        Recursive function that explores folders using a top-down approach.

        :param string: a single link contained in the present folder.
        :return: False if exploration fails.
        :return: True if exploration is successful.
        """

        try:
            location = string.find("/Folder/processfolder.aspx?FolderID=") #checks if this is a link to a folder
            location2 = string.find("/File/fs_folderfile.aspx?FolderFileID=") #checks if this is a link to a file

            if location == -1 and location2 == -1: #if there is no link to either a folder or a file, gets the page's text
                self.data.append(self.br.get_text())
                return 0

            elif location2 == -1: #if the link leads to a folder, explores that folder recursively
                id = string[(location+36):(location+36+7)]
                if id in self.explored_folders: #if the folder has already been explored, skips it
                    return 0
                self.explored_folders.append(id)
                end = "/Folder/processfolder.aspx?FolderID=" + id #builds the URL for the folder
                self.br.open("https://ntnu.itslearning.com"+end)
                links = self.br.get_links()
                for i in range(0, len(links)):
                    v = links[i]
                    self.explore_folders(str(v))
                return 0

            elif location == -1: #if the link leads to a file, calls the pdf reader
                id = string[(location2+38):(location2+38+7)]
                if id in self.explored_folders: #id the file has already been read, skips it
                    return 0
                self.explored_folders.append(id)
                end = "/File/fs_folderfile.aspx?FolderFileID=" + id #builds the URL for the file
                self.br.open("https://ntnu.itslearning.com"+end)
                self.get_pdf()
                return 0
            return True
        except:
            return False

    def get_pdf(self):

        """
        Opens the file and extracts the text (assuming the file is in pdf-format).

        :return: False if extraction fails.
        :return: True if extraction is successful.
        """

        try:
            qw = self.br.get_link("Download") #attempts to get the Download button

            if qw is None: #chekcs if there is a Download button, aborts if it is absent
                return 0

            else:
                self.br.follow_link(qw) #follows the link

                r = urlopen(self.br.url) #opens the file with urllib instead of Robobrowser
                mem = BytesIO(r.read()) #creates a temporary memory of the content of the file

                pdf = PyPDF2.PdfFileReader(mem) #opens the file with PyPDF2
                number_of_pages = pdf.getNumPages()

                for i in range(0, number_of_pages): #goes through all pages of the file and extracts the text
                    page = pdf.getPage(i)
                    self.pdf_data.append(page.extractText())
            return True
        except:
            return False

    def get_data(self):
        return self.data

    def get_pdf_data(self):
        return self.pdf_data

    def get_explored_folders(self):
        return self.explored_folders




