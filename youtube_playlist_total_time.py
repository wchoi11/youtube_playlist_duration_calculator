import sys
import requests
from functools import reduce
import re

key = # YOUR API KEY HERE


def get_playlist_id(url):
    '''
    Takes in url for a Youtube playlist and returns the
    id of the playlist.

    Arguments
    url: String representing url for Youtube playlist
    '''

    p = url.partition("https://www.youtube.com/playlist?list=")
    return p[2]

def get_video_ids(url):
    '''
    Takes in url for a Youtube playlist and returns
    list of video ids in that playlist.

    Arguments
    url: String representing url for Youtube playlist
    '''

    playlistId = get_playlist_id(url)
    maxResults = 50
    url = ("https://www.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults=" +
    str(maxResults) +
    "&playlistId=" +
    playlistId +
    "&key=" + key)

    # GET https://www.googleapis.com/youtube/v3/playlistItems
    response = requests.get(url).json()

    video_ids = []
    for v in response["items"]:
        video_ids.append(v["contentDetails"]["videoId"])

    while response.get("nextPageToken"):

        url = ("https://www.googleapis.com/youtube/v3/playlistItems" +
        "?part=" + "contentDetails" +
        "&pageToken=" + response["nextPageToken"] +
        "&maxResults=" + str(maxResults) +
        "&playlistId=" + playlistId +
        "&key=" + key)
        response = requests.get(url).json()

        for v in response["items"]:
            video_ids.append(v["contentDetails"]["videoId"])


    return video_ids

def get_durations(video_ids):
    '''
    Takes in list of Youtube video ids and returns
    list of durations for each video in ISO 8601
    format.

    Arguments
    video_ids: List of Youtube video ids
    '''
    max_queries = 50

    video_ids = [video_ids[i:i + max_queries] for i in range(0, len(video_ids), max_queries)]

    durations = []

    for some_ids in video_ids:
        ids = ','.join(some_ids)
        url = ("https://www.googleapis.com/youtube/v3/videos?part=contentDetails" +
        "&id=" + ids +
        "&key=" + key)

        # GET https://www.googleapis.com/youtube/v3/videos
        response = requests.get(url).json()

        for v in response["items"]:
            duration = v["contentDetails"]["duration"]
            durations.append(duration)

    return durations

def format_duration(hms):
    '''
    Takes in a triple of the form (h,m,s), where
    h is number of hours, m is minutes, and s is
    seconds. If duration is less than 1 hour,
    outputs duration as m:s. Else, outputs duration
    as h:m:s.

    Arguments
    hms: Triple of number of hours, minutes, and seconds
    '''

    if hms[0] == 0:
        if hms[2] < 10:
            return str(hms[1]) + ":0" + str(hms[2])
        else:
            return str(hms[1]) + ":" + str(hms[2])
    else:
        return (str(hms[0]) +
        ":" +
        (str(hms[1]) if hms[1] >= 10 else "0" + str(hms[1])) +
        ":" +
        (str(hms[2]) if hms[2] >= 10 else "0" + str(hms[2])))

def iso_to_seconds(s):
    '''
    Takes in string of a duration s in ISO 8601 format
    and converts to seconds.

    Arguments
    s: String that represents duration in ISO 8601
    '''

    lookup = { 'H': 3600, 'M': 60, 'S': 1 }

    assert s[0:2] == "PT", "String is not in ISO 8601 format e.g. PT#H#M#S"

    total_seconds = 0
    n = ""
    for c in s[2:]:
        if c.isdigit():
            n += c
        else:
            total_seconds += lookup[c] * int(n)
            n = ""

    return total_seconds


def seconds_to_total_duration(times):
    '''
    Takes in list of durations in ISO 8601 format and outputs
    total in the format given from above format_duration
    function.

    Arguments
    times: List of durations in seconds
    '''

    total_seconds = reduce(lambda x,y: x + y, map(iso_to_seconds, times))

    h = total_seconds // 3600
    total_seconds %= 3600

    m = total_seconds // 60
    total_seconds %= 60

    return format_duration((h,m,total_seconds))




if __name__ == "__main__":
    # the only argument for this script should be the Youtube playlist URL
    # that is being queried for total duration
    assert len(sys.argv) == 2, "This script only takes in 1 argument-a Youtube playlist URL"

    playlist_url = sys.argv[1]
    playlist_url_pattern = re.compile(r'^https://www.youtube.com/playlist\?list=')

    assert playlist_url_pattern.match(playlist_url), \
    "Not a valid URL for a Youtube playlist. Make sure the URL was correctly copied"

    video_ids = get_video_ids(playlist_url)
    durations = get_durations(video_ids)
    print("Total duration: " + seconds_to_total_duration(durations))
