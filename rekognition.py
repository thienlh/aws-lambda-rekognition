import os

import boto3

MAX_NUM_LABELS = 10

rek = boto3.client('rek')
# Confidence interval for image moderation
MIN_CONFIDENCE = float(os.environ['MIN_CONFIDENCE'])


def recognize_celebrity(image_bytes):
    try:
        response = rek.recognize_celebrities(
            Image={
                'Bytes': image_bytes,
            }
        )
    except Exception as e:
        print(e)
        print('Unable to recognize celebrity.')
        raise e

    celebrities = response['CelebrityFaces']
    print(celebrities)
    return celebrities


def detect_explicit_content(image_bytes):
    """ Checks image for explicit or suggestive content using Amazon Rekognition Image Moderation.

    Args:
        image_bytes (bytes): Blob of image bytes.

    Returns:
        (boolean)
        True if Image Moderation detects explicit or suggestive content in blob of image bytes.
        False otherwise.

    """
    try:
        response = rek.detect_moderation_labels(
            Image={
                'Bytes': image_bytes,
            },
            MinConfidence=MIN_CONFIDENCE
        )
    except Exception as e:
        print(e)
        print('Unable to detect labels for image.')
        raise e

    labels = response['ModerationLabels']

    if not labels:
        return False
    return True


def detect_labels(image_bytes):
    """ Checks image for explicit or suggestive content using Amazon Rekognition Image Moderation.

    Args:
        image_bytes (bytes): Blob of image bytes.

    Returns:
        (boolean)
        True if Image Moderation detects explicit or suggestive content in blob of image bytes.
        False otherwise.

    """
    try:
        response = rek.detect_labels(
            Image={
                'Bytes': image_bytes,
            },
            MinConfidence=MIN_CONFIDENCE,
            MaxLabels=MAX_NUM_LABELS,
        )
    except Exception as e:
        print(e)
        print('Unable to detect labels for image.')
        raise e

    return response['Labels']
