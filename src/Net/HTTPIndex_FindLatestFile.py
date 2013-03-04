import os, urllib2, re
from distutils.version import LooseVersion

def findLatestFile(baseURL, filePrefix):
    try:
        contents = urllib2.urlopen(baseURL, timeout=4).read()
    except TypeError:    # <= py 2.6
        contents = urllib2.urlopen(baseURL).read()
    
    links = re.findall('''href=["'](.[^"']+)["']>''', contents, re.I)
    linkModTimes = re.findall(r'\d\d-(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)-\d{4} \d{2}:\d{2}', contents, re.I)
    
    if len(linkModTimes) != 0:
        # heading links have no mod times, so remove those
        links = links[(len(links) - len(linkModTimes)) : ]
        linkTuples = filter(lambda x: x[0].find(filePrefix) != -1, zip(links, linkModTimes))
        linkTuples = sorted(linkTuples, key = lambda x: LooseVersion(x[1]))
        filename = linkTuples[-1][0]
    else:
        # don't use linkModTimes
        links = filter(lambda x: x.find(filePrefix) != -1, links)
        links.sort(key=LooseVersion)
        filename = links[-1]
    return os.path.join(baseURL, filename)

