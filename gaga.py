#!/usr/bin/env python
# coding: utf-8

import os
try:
	os.chdir(os.path.join(os.getcwd(), 'gaga'))
	print(os.getcwd())
except:
	pass


# In[ ]:



class Song:
    def __init__(self, uri, name, artists):
        self.uri = uri
        self.name = name
        self.artists = artists
class Album:
    def __init__(self, uri, name, artists):
        self.uri = uri
        self.name = name
        self.artist = artists

#import spotipy
from mining import albumSongs, artistAlbums, albumsSongs, useSearch, getSpotify
import networkx as nx
import pickle
from itertools import permutations

G = nx.Graph()
known_songs = {}
known_artists = set()
def updateSongsSearch(known_songs, known_artists,query):
    newSongs = useSearch(sp, query)
    addToSongs(newSongs, known_songs, known_artists)


def addToSongs(songs, known_songs, known_artists):
    for song in songs:
        known_songs[song.uri] = vars(song)
        for artist in song.artists:
            known_artists.add(artist)

def updateFromArtists(sp, user_given=None):
    i = 0
    use = known_artists
    if user_given:
        use = user_given
    for artist in use:
        if not G.has_node(artist):
            G.add_node(artist)
        if i > 30:
            break
        if  G.degree(artist) > 2:
            print("skipp", end ="")
            print(artist, end=" has degree")
            print(G.degree(artist), end="\n")
            i -= 1
            pass
        else:
            print("ayy ", end="")
            print(artist)
            result = sp.search(artist) #search query
            try:
                artist_uri = result['tracks']['items'][0]['artists'][0]['uri']
            except IndexError:
                print("oops")
                pass

            artist_albums = artistAlbums(sp, artist_uri)
            artist_songs = albumsSongs(sp, artist_albums)
            i += 1
            for song in artist_songs:
                known_songs[song.uri] = vars(song)
                for artist_ in song.artists:
                    known_artists.add(artist_)

def deserializeAndPopulate():
    known_songs = {}
    known_artists = set()
    with open('kkk.pkl', 'rb') as handle:
        known_songs = pickle.load(handle)
    for key, song in known_songs.items():
        for artist in song['artists']:
            G.add_node(artist)
            known_artists.add(artist)
        perm = permutations(song['artists'])
        for x in list(perm):
            G.add_edge(x[0],x[1], edge_song=song['name'])
    return known_songs, known_artists

def save_obj(obj, name ):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
save_obj(known_songs, "aftermulti-")
def updateGraphFromSongs():
    for key, song in known_songs.items():
        for artist in song['artists']:
            G.add_node(artist)
            known_artists.add(artist)
        perm = permutations(song['artists'])
        for x in list(perm):
            G.add_edge(x[0],x[1], edge_song=song['name'])

def get_shortest_path(G, target):
    try:
        shortest_path = nx.shortest_path(G, source="Lady Gaga", target=target)
    except nx.exception.NetworkXNoPath: 
        return "∞", "INF"
    outstr=""
    for i in range(1,len(shortest_path)):
        outstr += shortest_path[i-1] + " ---> "
        data = G.edges[shortest_path[i-1], shortest_path[i]]['edge_song']
        data_trimmed = data[:19] + (data[19:] and '...')
        outstr += data_trimmed + " ---> "
    outstr += shortest_path[-1]
    return outstr, len(shortest_path) - 1
    


def expandLowDegree():
    for artist in known_artists.copy():
        if not G.has_node(artist):
            G.add_node(artist)
        if  G.degree(artist) < 2:
            updateSongsSearch(known_songs, known_artists, artist)

if __name__ == "__main__":
    client_id = ""
    client_secret = "" 
    known_songs, known_artists = deserializeAndPopulate()
    updateGraphFromSongs()
    print(nx.info(G))
    print(len(known_artists))
    print(len(known_songs))

    sp = getSpotify(client_id, client_secret)
    # nx.write_graphml(G,"test.graphml")

 
