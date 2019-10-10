# youtubescraper

Youtubescraper allows to scrape video data of playlists, but also lets you collect all uploaded videos on a channel.
The data is scraped using the youtube API. In order to use the script you need to get a authentification file from google
(See https://developers.google.com/explorer-help/guides/code_samples#python for more information).

Usage examples:

python youtube.py --playlists PLAYLIST_ID1 PLAYLIST_ID2

will scrape the video data from 2 playlists with ids PLAYLIST_ID1 and PLAYLIST_ID2.
You can extract the playlistid by visiting the desired youtube playlist and extracting it from the link in the adress bar of the browser
e.g. https://www.youtube.com/watch?v=ToC8rFFp88Y&list=PL8dPuuaLjXtO4A_tL6DLZRotxEb114cMR
PLAYLIST_ID=PL8dPuuaLjXtO4A_tL6DLZRotxEb114cMR

If you want to get all uploaded videos of a channel: python youtube.py --channelid CHANNEL_ID
You can extract a channel id by visiting the desired youtube channel and extracting it from the link in the adress bar of the browser
e.g. https://www.youtube.com/channel/UCX6b17PVsYBQ0ip5gyeme-Q
CHANNEL_ID=UCX6b17PVsYBQ0ip5gyeme-Q
