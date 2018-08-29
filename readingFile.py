import argparse
from bs4 import BeautifulSoup
import requests
import json
import os

def search_domain(index,liste):

    record_list = []
    warc_set= set()

    os.system('cls')

    if os.path.exists(index)==False:

        os.mkdir('C:\\Users\\hexka\\Desktop\\Python\\All\\' + str(index))

    for domain in liste:

        domainName=domain
        domainName=domainName.split("/")
        iwarcset = 1

        _folder='C:\\Users\\hexka\\Desktop\\Python\\All\\' + str(index) + '\\' + str(domainName[2])

        if os.path.exists(_folder)==False:

            os.mkdir(_folder)

        print
        "[*] Trying index %s" % index
        cc_url = "http://index.commoncrawl.org/CC-MAIN-%s-index?" % index
        cc_url += "url=%s&matchType=domain&output=json" % domain

        print("requested Url: ", cc_url)

        response = requests.get(cc_url)

        if response.status_code == 200:

            print("response [OK]")

            records = response.content.splitlines()
            print("total Records: ", len(records))

            recordi=1

            for record in records:

                recordFile=open(r'C:\Users\hexka\Desktop\Python\\All\\' + str(index) + '\\' + str(domainName[2]) + '\\' + str(recordi)+".txt","w")

                record=record.decode("utf-8")
                recordFile.write(record)
                decoded_record=record
                print (decoded_record)
                decoded_record=decoded_record.split('warc.gz')
                decoded_record2=decoded_record[0]
                decoded_record3=decoded_record2.split('"')[-1]
                decoded_record3=decoded_record3+"warc.gz"
                warc_set.add(decoded_record3)

                json_record = json.loads(record)
                record_list.append(json_record)
                recordFile.close()
                recordi=recordi+1

            ws = open(r'C:\Users\hexka\Desktop\Python\\All\\' + str(index) + '\\' + str(domainName[2]) + '\\warcSet' + str(iwarcset) + '.txt', 'w')

            for every in warc_set:

                ws.write(every+"\n")

            ws.close()

            iwarcset = iwarcset + 1

            print("[*] Added %d results." % len(records))
            print("*******************************************")

        else:

            print("response [ERROR]")

    print("[*] Found a total of %d hits." % len(record_list))

    return record_list

def main():

    WARC = []
    S3 = []

    page = requests.get("http://commoncrawl.org/the-data/get-started/")
    soup = BeautifulSoup(page.content, 'html.parser')

    f = open("index.html", "w")
    f.write(str(soup.prettify()))
    f.close()

    with open("index.html", "r") as f:

        contents = f.read()

        soup = BeautifulSoup(contents, 'lxml')

        for tag in soup.find_all("li"):

            if 's3://commoncrawl/' in tag.text:

                liTag = tag.text.replace("\n", "").strip()

                if "[WARC]" in liTag:

                    warcsplit = liTag.split("-")

                    item1 = warcsplit[3]

                    _item2 = warcsplit[4].split(" ")

                    item2 = _item2[0].replace("/", "").strip()

                    item3 = _item2[-2] + " " + _item2[-1]

                    WARC.append((item1, item2, item3))

                elif "[ARC]" not in liTag:

                    s3split = liTag.split("-")

                    item1 = s3split[3]

                    _item2 = s3split[4].split(" ")

                    item2 = _item2[0].replace("/", "").strip()

                    item3 = _item2[-2] + " " + _item2[-1]

                    S3.append((item1, item2, item3))

        allOfThem = []

        allOfThem = WARC + S3

    parser = argparse.ArgumentParser()

    parser.add_argument("--index", "-i", help="Istenen tarihin indexi")
    parser.add_argument("--topSitesList", "-t", help="Istenen Top List")

    veri = parser.parse_args()

    if (veri.index):
        print("Index: {}".format(veri.index))

    if (veri.topSitesList):
        print("TopSitesList: {}".format(veri.topSitesList))

    dosya = open(str(veri.topSitesList), "r")

    i = 0
    liste = list()

    while (i < 30):
        site = dosya.readline()
        site = site.strip()
        liste.append(site)
        i = i + 1

    z = 0
    wantedDate = None
    index_list = []

    for allOfThem_item in allOfThem:
        wantedDate = (allOfThem[z][0] + "-" + allOfThem[z][1])
        index_list.append(wantedDate)
        z = z + 1

    os.mkdir('C:\\Users\\hexka\\Desktop\\Python\\' + "All")

    index_list = [str(veri.index)]

    for index in index_list:

        sonuc = search_domain(index,liste)
        print(sonuc, "\n")

if __name__=="__main__":

    main()

