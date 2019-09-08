#!/usr/bin/env python
# coding: utf-8
import spotipy
from itertools import permutations
import networkx as nx
from textdistance import jaccard
from spotipy.oauth2 import SpotifyClientCredentials
import pickle

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

client_id = ""
client_secret = ""
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager) 
name = "Lady Gaga"
result = sp.search(name) 
gag_uri = result['tracks']['items'][0]['artists'][0]['uri']
G = nx.Graph()
known_albums = {}
known_songs = {}


def artistAlbums(sp, artist_uri, limit=50): # todo: more than 50!!
    """ Returns a list of names,uris """
    sp_albums = sp.artist_albums(artist_uri, album_type='album', limit=50)
    albums = []
    for album in sp_albums['items']:
        if album['name'] not in album_names:
            albums.append(Album(album['uri'], album['name'], album['artists']))
    return albums

def albumSongs(sp,album_uri, need_feats=True): 
    """ Returns a list of names,uris """
    songs = []
    tracks = sp.album_tracks(album_uri) 
    for track in tracks['items']: 
        if len(track['artists']) > 1 and need_feats:
            temp = []
            for artist in track['artists']:
                temp.append(artist['name']) 
                songs.append(Song(track['uri'], track['name'], tuple(temp)))
        elif not need_feats:
            temp = []
            for artist in track['artists']:
                temp.append(artist['name']) 
            songs.append(Song(track['uri'], track['name'], tuple(temp)))
    return songs
def albumsSongs(sp, albums, need_feats=True):
    
    """ Returns a list of names,uris for each album in the list"""
    songs = []
    for album in albums:
        songs.extend(albumSongs(sp, album.uri))
    return songs
    
def useSearch(sp, name, qtype='track', offset_=0, limit_=50, total=100, need_feats=True):
    songs = []
    while offset_ < total:
        tracks = sp.search(q='artist:' + name, type=qtype, offset=offset_, limit=limit_)
        offset_ += limit_
        for track in tracks['tracks']['items']:
            if len(track['artists']) > 1 and need_feats:
                temp = ""
                for artist in track['artists']:
                    temp +=(artist['name']) + " " 
                temp.strip()
                songs.append(Song(track['uri'], track['name'], temp))
            elif not need_feats:
                temp = ""
                for artist in track['artists']:
                    temp +=(artist['name']) + " " 
                temp.strip()
                songs.append(Song(track['uri'], track['name'], temp))
    return songs


gaga_albums = artistAlbums(sp, gag_uri)
gaga_f_songs = albumsSongs(sp, gaga_albums)

known_artists = set()

for song in gaga_f_songs:
    known_songs[song.uri] = vars(song)
    for artist in song.artists:
        known_artists.add(artist)
for artist in known_artists.copy():
    result = sp.search(artist) 
    artist_uri = result['tracks']['items'][0]['artists'][0]['uri']
    artist_albums = artistAlbums(sp, artist_uri)
    artist_songs = albumsSongs(sp, artist_albums)
    for song in artist_songs:
        known_songs[song.uri] = vars(song)
        for artist_ in song.artists:
            known_artists.add(artist_)

G.clear()
for key, song in known_songs.items():
    for artist in song['artists']:
        G.add_node(artist)
    perm = permutations(song['artists'])
    for x in list(perm):
        G.add_edge(x[0],x[1], val=song['name'])
list(G.nodes)
print(list(G.edges))
