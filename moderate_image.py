import gsheet
import rekognition
from slack import verify_token, verify_event, download_image, post_message, delete_file


def lambda_handler(event, context):
    print('Validating message...')
    # Verify token
    if not verify_token(event):
        return

    # Respond to Slack event subscription URL verification challenge
    if event.get('challenge') is not None:
        print(
            'Presented with URL verification challenge - responding accordingly...')
        challenge = event['challenge']
        return {'challenge': challenge}

    # Ignore event if Slack message doesn't contain any supported images
    if not verify_event(event):
        return

    # Gather event details
    event_details = event['event']
    file_details = event_details['file']
    channel = event_details['channel']
    url = file_details['url_private']
    file_id = file_details['id']
    print('Downloading image...')
    image_bytes = download_image(url)

    # Detect
    detect_explicit(channel, file_id, image_bytes)
    detect_image_labels(channel, image_bytes)
    detect_celebrities(channel, image_bytes)

    print('Done')
    return


def detect_celebrities(channel, image_bytes):
    print('Checking image to detect celebrity...')
    celebrities = rekognition.recognize_celebrity(image_bytes)
    gsheet.write_celebrities(celebrities)
    celeb_names = []
    for celeb in celebrities:
        celeb_names.append(
            celeb.get('Name') + ' (' + str(celeb.get('MatchConfidence')) + '%)')
    post_message(channel, 'Celebrities', celeb_names)


def detect_image_labels(channel, image_bytes):
    print('Checking image to detect content...')
    labels = rekognition.detect_labels(image_bytes)
    gsheet.write_labels(labels)
    names = []
    for label in labels:
        names.append(label.get('Name'))
    post_message(channel, 'Labels', names)


def detect_explicit(channel, file_id, image_bytes):
    print('Checking image for explicit content...')
    if rekognition.detect_explicit_content(image_bytes):
        print(
            'Image displays explicit content- deleting from Slack Shared Files...')
        delete_file(file_id)
        print('Posting message to channel to notify users of file deletion...')
        post_message(
            channel, 'Admin',
            'File removed due to displaying explicit or suggestive adult content.')
    else:
        print('No explicit content found.')
