import spotipy
import json

'''
Client ID
8eb8f36812a44993aab94c9b2ac7efb7

Client Secret
e941a852d4da41f38ac9a4249ab3bd27
'''


'''
0 uri
1 album
2 track_number
3 external_ids
4 name
5 preview_url
6 available_markets
7 explicit
8 disc_number
9 artists
10 external_urls
11 duration_ms
12 type
13 href
14 id
'''

sp = spotipy.Spotify()

search = input('search: ')

while search:
    results = sp.search(q=search, limit=20)
    tracks = []
    for info in results['tracks']['items']:
        tracks.append(info)

    print()
    s = sorted(tracks, key=lambda x: x['popularity'], reverse=True)
    for i in range(len(s)):
        print(i+1, s[i]['popularity'], s[i]['name'], '-', s[i]['artists'][0]['name'])

    print()
    search = input('search: ')

