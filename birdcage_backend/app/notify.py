from  app.models.notifications import NotificationAssignment, NotificationService
import apprise


def geturls(detectionaction):
    # Connect to the database
    

    # Execute the SQL query to get the URLs
    urls = (NotificationService
                .select(
                    NotificationService.service_url
                )
                .join(NotificationAssignment)
                .where(NotificationAssignment.detectionaction == detectionaction)
                .dicts())

    # Extract the URLs from the results
    urls = [url.service_url for url in urls]

    return urls


def notify(detectionaction, timestamp, stream_id, streamname, scientific_name, common_name,
                           confidence_score, mp3path):

    urls = geturls(detectionaction)

    # Create an Apprise instance
    apobj = apprise.Apprise()

    # Add each URL to the Apprise object
    for url in urls:
        apobj.add(url)

    title = detectionaction + " level bird: " + common_name
    body = "Common Name: " + common_name + "\n" + \
           "Scientific Name: " + scientific_name + "\n" + \
           "Confidence Score: " + str(confidence_score) + "\n" + \
           "Stream Name: " + streamname + "\n" + \
           "Time: " + timestamp

    #print(title, flush=True)
    #print(body, flush=True)
    print("Notifying", flush=True)

    if mp3path == '':
        apobj.notify(title=title, body=body)
    else:
        apobj.notify(title=title, body=body, attach=mp3path)
