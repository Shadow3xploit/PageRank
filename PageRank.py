import sqlite3

class Page:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.outgoingLinks = []
        self.ingoingLinks = []
        self.pageRank = 1
        
    def __lt__(self, other):
        return self.pageRank > other.pageRank
        
    def addLink(self, toPage):
        self.outgoingLinks.append(toPage)
        toPage.ingoingLinks.append(self)
        
    def calculatePageRank(self, d=0.85):
        sum = 0
        for link in self.ingoingLinks:
            sum += link.pageRank / len(link.outgoingLinks)
        
        self.pageRank = (1 - d) + (d * sum)
        
    def checkPageRank(self, correct):
        return abs(self.pageRank - correct) < 0.0000001
        

class PageController:
    def __init__(self):
        self.pages = []
        
    def clearPages(self):
        self.pages = []
        
    def addPage(self, id, name):
        self.pages.append(Page(id, name))
        
    def getPage(self, identifier):
        if type(identifier) is int:
            for page in self.pages:
                if page.id == identifier:
                    return page
        
        if type(identifier) is str:
            for page in self.pages:
                if page.name == identifier:
                    return page
            
    def readPagesFromWiki(self):
        con = sqlite3.connect('mediawiki.sqlite', detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES, check_same_thread = False)
        cur = con.cursor()
        cur.execute("SELECT page_id, page_title FROM mdk_page")
        for page in cur.fetchall():
            pageId = page[0]
            pageTitle = page[1]
            if pageId != None and pageTitle != None:
                self.addPage(pageId, pageTitle)
            
        cur.execute("SELECT pl_from, pl_title FROM mdk_pagelinks")
        for link in cur.fetchall():
            pageFrom = self.getPage(link[0])
            pageTo = self.getPage(link[1])
            if pageFrom != None and pageTo != None:
                pageFrom.addLink(pageTo)
            
        con.close()
        print(f"Added {len(self.pages)} from MediaWiki")

    def calculateAllPageRanks(self, iterations):
        for i in range(iterations):
            for page in self.pages:
                page.calculatePageRank()
                
        self.pages.sort()
                
    def printAllPagePanks(self):
        sum = 0
        for page in self.pages:
            sum += page.pageRank
            print(f"PageRank for {page.name} is {page.pageRank}")
            
        print(f"Sum of all PageRanks: {sum}")
            
    def runTests(self): # pragma: no cover
        print("Running Test 1")
        self.clearPages()
        self.addPage(1, "A")
        self.addPage(2, "B")

        self.getPage(1).addLink(self.getPage(2))
        self.getPage(2).addLink(self.getPage(1))
            
        self.calculateAllPageRanks(10)
        assert self.getPage(1).checkPageRank(1)
        assert self.getPage(2).checkPageRank(1)
        
        print("Running Test 2")
        self.clearPages()
        self.addPage(1, "A")
        self.addPage(2, "B")
        self.addPage(3, "C")

        self.getPage(1).addLink(self.getPage(3))
        self.getPage(2).addLink(self.getPage(1))
        self.getPage(3).addLink(self.getPage(2))
            
        self.calculateAllPageRanks(10)
        assert self.getPage(1).checkPageRank(1)
        assert self.getPage(2).checkPageRank(1)
        assert self.getPage(3).checkPageRank(1)
        
        print("Running Test 3")
        self.clearPages()
        self.addPage(1, "A")
        self.addPage(2, "B")
        self.addPage(3, "C")

        self.getPage(1).addLink(self.getPage(2))
        self.getPage(1).addLink(self.getPage(3))
        self.getPage(2).addLink(self.getPage(1))
        self.getPage(2).addLink(self.getPage(3))
            
        self.calculateAllPageRanks(10)
        assert self.getPage(1).checkPageRank(0.2608696295025553)
        assert self.getPage(2).checkPageRank(0.2608696295025553)
        assert self.getPage(3).checkPageRank(0.3717391693674851)
        
        print("Running Test 4")
        self.clearPages()
        self.addPage(1, "A")
        self.addPage(2, "B")
        self.addPage(3, "C")

        self.getPage(1).addLink(self.getPage(2))
        self.getPage(2).addLink(self.getPage(3))
            
        self.calculateAllPageRanks(10)
        assert self.getPage(1).checkPageRank(0.15)
        assert self.getPage(2).checkPageRank(0.2775)
        assert self.getPage(3).checkPageRank(0.385875)
        
        print("Tests Successful")
        

if __name__ == "__main__":
    controller = PageController()
    controller.readPagesFromWiki()
    controller.calculateAllPageRanks(15)
    controller.printAllPagePanks()
