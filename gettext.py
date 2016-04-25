from HTMLParser import HTMLParser

# f2 = open('data/set1/a1.htm')
# htmlText = f2.read()

class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.h1 = False
        self.h2 = False
        self.h3 = False
        self.h4 = False
        self.h5 = False
    	self.h6 = False
        self.currh1 = ""
        self.currh2 = ""
        self.currh3 = ""
        self.currh4 = ""
        self.currh5 = ""
        self.currh6 = ""
        self.d = dict()
        self.key = ""
    def handle_starttag(self, tag, attrs):
        # print "Start tag:", tag
        if tag == 'h1':
            self.h1 = True
        elif tag == 'h2':
            self.h2 = True
        elif tag == 'h3':
            self.h3 = True
        elif tag == 'h4':
            self.h4 = True
        elif tag == 'h5':
            self.h5 = True
        elif tag == 'h6':
            self.h6 = True

        # for attr in attrs:
        #     print "     attr:", attr
        # print self.isTitle, tag
    def handle_endtag(self, tag):
        # print self.isTitle
        # print "End tag  :", tag
        if tag == 'h1':
            self.h1 = False
        elif tag == 'h2':
            self.h2 = False
        elif tag == 'h3':
            self.h3 = False
        elif tag == 'h4':
            self.h4 = False
        elif tag == 'h5':
            self.h5 = False
        elif tag == 'h6':
            self.h6 = False
    def handle_data(self, data):
        # print self.isTitle, data
        data = data.strip()
        data = data.decode('utf-8')
        if self.h1:
            self.currh1 = data
            self.key = self.currh1
        elif self.h2:
            self.currh2 = data
            self.key = (self.currh1,self.currh2)
        elif self.h3:
            self.currh3 = data
            self.key = (self.currh1,self.currh2,self.currh3)
        elif self.h4:
            self.currh4 = data
            self.key = (self.currh1,self.currh2,self.currh3,self.currh4)
        elif self.h5:
            self.currh5 = data
            self.key = (self.currh1,self.currh2,self.currh3,self.currh4,self.currh5)
        elif self.h6:
            self.currh6 = data
            self.key = (self.currh1,self.currh2,self.currh3,
                self.currh4,self.currh5,self.currh6)
        else:
            if self.key == '':
                pass
            elif self.key in self.d:
                self.d[self.key] = self.d[self.key] + ' ' + data
            else:
                self.d[self.key] = data
        # print "Data     :", data

# parser = MyHTMLParser()
# parser.feed(htmlText)
# print parser.d