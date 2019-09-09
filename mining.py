#!/usr/bin/env python
# coding: utf-8

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials #To access authorised Spotify data


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




































































































def searchArtist(sp, name): #todo exceptio handling
    result = sp.search(name) #search query
    uri = result['tracks']['items'][0]['artists'][0]['uri']
    return uri


def getSpotify(client_id, client_secret):
    client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    return spotipy.Spotify(client_credentials_manager=client_credentials_manager) #spotify object to access API


def artistAlbums(sp, artist_uri, limit=50): # todo: more than 50!!
    """ Returns a list of names,uris """
    sp_albums = sp.artist_albums(artist_uri, album_type='album', limit=50)
    albums = []
    for album in sp_albums['items']:
       # if album['name'] not in albums:
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

