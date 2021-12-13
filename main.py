import os
import csv
import googleapiclient.discovery
from key import KEY

# Writes comment data to comments.csv
# Parameters =======
# data: dictionary returned from YouTube API query
# startIdx: Index of first comment in the query
# num_inc: Cumulative count of the number of incongruity comments
# num_sup:  Cumulative count of the number of superiority comments
# num_both: Cumulative count of the number of comments categorized in both theories
# num_none: Cumulative count of the number of comments categorized in neither theory
# Return ===========
# List containing updated values of startIdx, num_inc, num_sup, num_both, num_none

def write_data(data::dict, startIdx::int, num_inc::int, num_sup::int, num_both::int, num_none::int):
    incog = ["surprising", "surprised", "unexpected", "underrated",
            "actually"]

    superior = ["fever dream", "surreal", "so bad"]

    num_items = len(data["items"])

    with open("comments.csv", "a", newline="\n") as csvfile:
        dwriter = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)

        for i in range(num_items):
            content = data["items"][i]["snippet"]["topLevelComment"]["snippet"]["textOriginal"]
            inc = 0
            sup = 0

            for ic in incog:
                if ic in content.lower():
                    inc += 1
                    num_inc += 1
                    break
            for sp in superior:
                if sp in content.lower():
                    sup += 1
                    num_sup += 1
                    break

            if inc == 1 or sup == 1:
                if inc == 1 and sup == 1:
                    num_both += 1
                
                dwriter.writerow([str(i + startIdx), content, str(inc), str(sup)])

            else:
                num_none += 1

    return [startIdx + num_items, int(num_inc), int(num_sup), int(num_both), int(num_none)] 

# Get comment data from a YouTube video using the YouTube Data v3 API.

def get_comments(videoId::str):
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = KEY

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = DEVELOPER_KEY)

    request = youtube.commentThreads().list(
        part="snippet,replies",
        videoId=videoId,
        maxResults=100
    )

    startIdx = 0
    num_inc = 0
    num_sup = 0
    num_both = 0
    num_none = 0
    
    with open("comments.csv", "w", newline="\n") as csvfile:
        dwriter = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        dwriter.writerow(["Comment ID", "Comment Text", "Incongruity", "Superiority"])


    while request:

        response = request.execute()
        new_vals = write_data(response, startIdx, num_inc, num_sup, num_both, num_none)

        startIdx = new_vals[0]
        num_inc = new_vals[1]
        num_sup  = new_vals[2]
        num_both = new_vals[3]
        num_none = new_vals[4]

        try: 
            nextPageToken = response["nextPageToken"]

            request = youtube.commentThreads().list(
                part="snippet,replies",
                videoId=videoId,
                maxResults=100,
                pageToken=nextPageToken
            )
        except:

            print("Number of Incongruity Comments are: " + str(num_inc)
                + "\nNumber of Superiority Comments are: " + str(num_sup) 
                + "\nNumber of both are: " + str(num_both)
                + "\nNumber of none are: " + str(num_none))
            return

def main():
    commentData = get_comments("nH_bEtbfB9U");

if __name__ == "__main__":
    main()
