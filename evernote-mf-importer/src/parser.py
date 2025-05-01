from bs4 import BeautifulSoup

def parse_enex(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'xml')
    notes = soup.find_all('note')
    titles = [note.title.text for note in notes]
    return titles
