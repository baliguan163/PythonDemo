
from bs4 import BeautifulSoup
class person(object):
    def __init__(self, personTag=None):
        self.analysis(personTag)

    def analysis(self, personTag):
        self.analysisName(personTag)
        self.analysisFollowAndFansNumber(personTag)
        self.analysisCity(personTag)
        self.analysisIntroduce(personTag)
        self.analysisFollowWay(personTag)
        self.analysisID(personTag)

    def analysisName(self, personTag):
        self.name = personTag.div.a.string

¡¡¡¡

def analysisFollowAndFansNumber(self, personTag):
    for divTag in personTag.find_all('div'):
        if divTag['class'] == ["info_connect"]:
            infoTag = divTag
    if locals().get("infoTag"):
        self.followNumber = infoTag.find_all('span')[0].em.string
        self.fansNumber = infoTag.find_all('span')[1].em.a.string
        self.assay = infoTag.find_all('span')[2].em.a.string


def analysisCity(self, personTag):
    for divTag in personTag.find_all('div'):
        if divTag['class'] == ['info_add']:
            addressTag = divTag
    if locals().get('addressTag'):
        self.address = addressTag.span.string


def analysisIntroduce(self, personTag):
    for divTag in personTag.find_all('div'):
        if divTag['class'] == ['info_intro']:
            introduceTag = divTag
    if locals().get('introduceTag'):
        self.introduce = introduceTag.span.string


def analysisFollowWay(self, personTag):
    for divTag in personTag.find_all('div'):
        if divTag['class'] == ['info_from']:
            fromTag = divTag
    if locals().get('fromTag'):
        self.fromInfo = fromTag.a.string


def analysisID(self, personTag):
    personRel = personTag.dt.a['href']
    self.id = personRel[personRel.find('=') + 1:-5] + personRel[3:personRel.find('?')]