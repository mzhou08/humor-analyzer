import os
import csv
import googleapiclient.discovery
from key import KEY

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
        videoId="nH_bEtbfB9U"
    )

    response = request.execute()

    return response


def write_data(data):
    with open("comments.csv", "w", newline="\n") as csvfile:
        dwriter = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        dwriter.writerow(["Comment ID", "Comment Text", "Incongruity", "Superiority"])

        for i in range(len(data["items"])):
            dwriter.writerow([str(i), data["items"][i]["snippet"]["topLevelComment"]["snippet"]["textDisplay"], "0", "0"])

def main():
    commentData = get_comments();
    write_data(commentData);

if __name__ == "__main__":
    main()
