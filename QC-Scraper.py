import signal, sys, requests, bs4, os
signal.signal(signal.SIGINT, lambda x,y: sys.exit(0))

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.149 Safari/537.36'}

startPage = input("Enter Start Page: ")

url = 'https://questionablecontent.net/view.php?comic='+startPage
os.makedirs('QuesCon', exist_ok=True)

getLatest = requests.get(url, headers=headers, stream = True)
getLatest.raise_for_status()
soLatest = bs4.BeautifulSoup(getLatest.text, "lxml")
qcLatest = soLatest.find('a', text='Latest')
lastPage = qcLatest.get('href').rpartition('=')[-1]

while (int(startPage) < int(lastPage)+1):
    res = requests.get(url, headers=headers, stream = True)

    if res.status_code == 404:
        print("quitting...")
        quit()

    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, "lxml")
    qcNext = soup.find('a', text='Next')
    nextPage = qcNext.get('href')
    comicSrc = soup.select('#strip')
    comicImg = comicSrc[0].get('src').partition('.')[-1]
    print()
    if comicImg == []:
         print('Could not find comic image.')
    else:
         comicUrl = 'https://questionablecontent.net'+comicImg
         print('*********************************')
         print('Downloading image %s...' % (comicUrl))
         res = requests.get(comicUrl, headers=headers, stream = True)
         res.raise_for_status()
    imageFile = open(os.path.join('QuesCon', 'QC-'+comicImg.rpartition('/')[-1]), 'wb')
    for chunk in res.iter_content(1024):
        imageFile.write(chunk)
    imageFile.close()
    print('Downloaded')
    print('*********************************')
    startPage = int(startPage)+1
    url = 'https://questionablecontent.net/'+nextPage
