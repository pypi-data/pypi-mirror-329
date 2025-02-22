from fire import Fire
from TexSoup import TexSoup
from TexSoup.data import BraceGroup
import bibtexparser as b
from pathlib import Path
from unisim import TextSim

class BibSim(TextSim):
    def embed(self, inputs):
        txts = [entry['author'] + ' " ' + entry['title'] + '"' 
         if 'author' in entry else entry['title']
         for entry in inputs
         if 'title' in entry]
        return super().embed(txts)

def recite(doc, old_bib, new_bib):
    doc = TexSoup(doc)
    text_sim = BibSim()

    old_entries, new_entries = (
        [entry for entry in b.parse_string(bib).entries if 'title' in entry]
        for bib in (old_bib, new_bib)
    )

    match = text_sim.match(old_entries, new_entries, similarity_threshold=0.9)
    match = match[match['is_match']]
    key_update = {k.key: v.key for k, v in zip(match['query'], match['target'])}

    for cite in doc.find_all('cite'):
        for arg in cite.args:
            if isinstance(arg, BraceGroup):
                keys = arg.string.replace(' ', '').split(',')
                keys = [key_update.get(k, k) for k in keys]
                arg.string = ','.join(keys)

    return str(doc)

def recite_(doc, old_bib, new_bib):
    return recite(
        Path(doc).read_text(),
        Path(old_bib).read_text(),
        Path(new_bib).read_text()
    )

def recite__():
    Fire(recite_)

if __name__ == '__main__':
    recite__()