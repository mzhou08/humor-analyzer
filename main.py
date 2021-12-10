import os
import csv
import googleapiclient.discovery
from key import KEY

def write_data(data, startIdx):
    with open("comments.csv", "a", newline="\n") as csvfile:
        dwriter = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        dwriter.writerow(["Comment ID", "Comment Text", "Incongruity", "Superiority"])

        for i in range(len(data["items"])):
            dwriter.writerow([str(i + startIdx), data["items"][i]["snippet"]["topLevelComment"]["snippet"]["textDisplay"], "0", "0"])

    return 100 + startIdx

def get_comments():
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
        videoId="nH_bEtbfB9U",
        maxResults=100
    )

    startIdx = 0

    while request:

        response = request.execute()
        startIdx = write_data(response, startIdx)

        try: 
            nextPageToken = response["nextPageToken"]

            request = youtube.commentThreads().list(
                part="snippet,replies",
                videoId="nH_bEtbfB9U",
                maxResults=100,
                pageToken=nextPageToken
            )
        except:
            return

def main():
    commentData = get_comments();

if __name__ == "__main__":
    main()
