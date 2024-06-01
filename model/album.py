import string
from dataclasses import dataclass

@dataclass
class Album:
    AlbumId: int
    Title: string
    ArtistId: int
    NumeroCanzoni: int

    def __hash__(self):
        return hash(self.AlbumId)

