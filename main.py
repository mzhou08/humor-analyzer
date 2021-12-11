import os
import csv
import googleapiclient.discovery
from key import KEY

def write_data(data, startIdx, num_inc, num_sup, num_both, num_none):
    incog = ["surprisingly", "surprising", 
            "unexpectedly", "unexpected", 
            "disturbingly", "legit", "legitimately", 
            "really", "genuinely"]

    superior = ["fever dream", "surreal", "underrated", "actually"]


    with open("comments.csv", "a", newline="\n") as csvfile:
        dwriter = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        dwriter.writerow(["Comment ID", "Comment Text", "Incongruity", "Superiority"])

        for i in range(len(data["items"])):
            content = data["items"][i]["snippet"]["topLevelComment"]["snippet"]["textOriginal"]
            inc = 0
            sup = 0

            for ic in incog:
                if ic in content.lower():
                    inc = 1
                    num_inc += 1
            for sp in superior:
                if sp in content.lower():
                    sup = 1
                    num_sup += 1
            
            if inc == 1 or sup == 1:
                if inc == 1 and sup == 1: num_both += 1
                dwriter.writerow([str(i + startIdx), content, str(inc), str(sup)])

            else:
                num_none += 1

    return [num_inc, num_sup, num_both, num_none] 

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
    num_inc = 0
    num_sup = 0
    num_both = 0
    num_none = 0

    while request:

        response = request.execute()
        add_inc, add_sup, add_both, add_none = write_data(response, startIdx, num_inc, num_sup, num_both, num_none)
        startIdx += 100

        num_inc += add_inc
        num_sup += add_sup
        num_both += add_both
        num_none += add_none

        try: 
            nextPageToken = response["nextPageToken"]

            request = youtube.commentThreads().list(
                part="snippet,replies",
                videoId="nH_bEtbfB9U",
                maxResults=100,
                pageToken=nextPageToken
            )
        except:

            print("Number of Incongruity Comments are: " + str(num_inc)
                + "\nNumber of Superiority Comments are: " + str(num_sup) 
                + "\nNumber of both are: " + str(num_both)
                + "\nNumber of none are: " + str(num_none))
            return

def analyze_comments():
    with open("comments.csv", "r", newline="\n") as csvfile:

        with open("analysis.csv", "w", newline="\n") as csv_towrite:
            dwriter = csv.writer(csv_towrite, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            lines = csvfile.readlines()




def main():
    commentData = get_comments();
    analyze_comments()

if __name__ == "__main__":
    main()
