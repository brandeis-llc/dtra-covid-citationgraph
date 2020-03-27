from typing import List


class Paper(object):

    def __init__(self, title: str, authors: List[str], refereces):
        self.title = title
        self.authors = authors
        self.refereces = refereces

    def cites(self, other):
        for ref in self.refereces:
            if ref == other:
                return True
        return False

    def firstauthor_lastname(self):
        return self.authors[0].split()[-1].lower().strip()

    def __eq__(self, other):
        return self.title.lower() == other.title.lower() \
               and len(self.authors) == len(other.authors)\
               and self.firstauthor_lastname() == other.firstauthor_lastname()

    def __str__(self):
        return f'({self.firstauthor_lastname()})-{self.title}'
