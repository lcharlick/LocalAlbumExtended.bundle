#
# Copyright (c) 2020 Lachlan Charlick. All rights reserved.
#

from mutagen.id3 import ID3
import os

ID3_FILE_TYPES = ('.mp3')

def Start():
    pass


class LocalAlbumExtended(Agent.Album):
    """ Reads extended ID3 metadata from local audio files.
    """

    name = 'Local Album Extended'
    primary_provider = False

    languages = [Locale.Language.NoLanguage]
    contributes_to = [
        'com.plexapp.agents.localmedia',
        'com.plexapp.agents.lastfm',
        'com.plexapp.agents.none'
    ]

    def search(self, results, media, lang):
        results.Append(MetadataSearchResult(id='null', score=100))

    def update(self, metadata, media, lang, prefs):
        if not media.children:
            return

        track = media.children[0]

        if not track.items:
            return

        item = track.items[0]

        if not item.parts:
            return

        part = item.parts[0]

        if os.path.splitext(part.file)[1] in ID3_FILE_TYPES:
            self.update_album(part.file, metadata)


    def update_album(self, path, metadata):
        tags = ID3(path)
        metadata.summary = self.read_summary(tags)


    def read_summary(self, tags):
        comm = tags.getall(Prefs['summary_frame'])
        return comm[0] if comm else ''
