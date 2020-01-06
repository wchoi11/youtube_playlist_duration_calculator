# Youtube Playlist Total Duration Calculator
* A Python script that calculates the total duration of any Youtube playlist using the Youtube Data API
  * Just copy and paste the URL to the playlist as an argument to the script e.g. python youtube_playlist_total_time.py PLAYLIST_URL
* Runs out of box: just need an API key for Youtube Data API which you can get here [here](https://console.developers.google.com)
  * All you need to do is enable the Youtube Data API and copy and paste your API key into the script
  * No need for the additional OAuth credentials
* Script makes (Number of videos in playlist)/25 API calls and free tier gives around 10,000 calls/day so basically no limit
