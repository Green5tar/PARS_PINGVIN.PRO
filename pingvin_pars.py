import urllib.request
from bs4 import BeautifulSoup
import csv

burl = "https://pingvin.pro/category/gadgets/news-gadgets?"

def get_html(url):
    response = urllib.request.urlopen(url)
    return response.read()

def get_page_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    paggination = soup.find('ul', class_='pagination')
    return int(paggination.find_all('li')[-2].text)

def parse(html):
    projects = []
    soup = BeautifulSoup(html, 'html.parser')
    div = soup.find('div', id='main', role='main', class_='row')

    for nev in div.find_all('div', class_='col-lg-4 col-md-6 cat2content'):
        #nev return all news boxes
        mcols = nev.find_all('div')[1:]

        photo = nev.find('div', class_='card-image').find('a').find('img').get('src')
        headerr = nev.find('div', class_='card-body').h3.text.replace('\n', '')
        opis = nev.find('div', class_='card-body').p.text.replace('\n', '').replace('[…]', '')
        link = nev.find('div', class_='card-body').find('a', class_='card-link').get('href').replace('\n', '')
        #mcols return all card image and card body`

        projects.append({
            'image': photo,
            'head': headerr,
            'opis': opis,
            'link': link
        })

    for project in projects:
        print(project)

    return projects


def save(projects, path):

    with open(path, 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')

        writer.writerow(('Image_Link','Title','Discription','News_Link'))

        writer.writerows(
            (project['image'], project['head'], project['opis'], project['link']) for project in projects
        )

def get_pages(html):
    soup = BeautifulSoup(html, 'html.parser')

    pages = soup.find_all('ul', class_='pagination').find_all('a',class_='page_numbers')[-1].get('href')

    print('pages')

def main():

    projects = []

    total_pages = get_page_count(get_html(burl))

    print('%d all_pages...' % total_pages)

    for page in range(1, 11):
        print('\nPars %d%% (%d/%d)' % (page / total_pages * 100, page, total_pages))
        projects.extend(parse(get_html(burl + "page=%d" % page)))

    save(projects, 'pars_pingvin.csv')

if __name__ == '__main__':
    main()
