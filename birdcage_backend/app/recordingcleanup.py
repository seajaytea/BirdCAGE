from config import DETECTION_DIR_NAME
from app.models.detections import Detection
from peewee import fn
import os
import datetime




def recordingcleanup(numdays):

    # 0 means keep forever
    if numdays <= 0:
        return

    # Calculate the timestamp limit
    timestamp_limit = datetime.datetime.now() - datetime.timedelta(days=numdays)

    # Set the value of DETECTION_DIR
    basedir = os.path.dirname(os.path.abspath(__file__))
    DETECTION_DIR = os.path.join(basedir, '..', DETECTION_DIR_NAME)
    THUMB_DIR = os.path.join(DETECTION_DIR, 'thumb')
    FULL_DIR = os.path.join(DETECTION_DIR, 'full')


    #get max confidence detections per scientfic name
    highest_confidence_per_species = (Detection
                .select(Detection.id, Detection.filename, fn.MAX(Detection.confidence).alias('max_confidence'))
                .where(fn.LENGTH(Detection.filename) > 0)
                .group_by(Detection.scientific_name)
    )
    ids_to_keep = [record.id for record in highest_confidence_per_species]
    to_delete = (Detection
                .select(Detection.id, Detection.filename)
                .where((Detection.timestamp < timestamp_limit) & 
                       (Detection.id.not_in(ids_to_keep)))
    )




    # Iterate through records
    for record in to_delete:

        # Delete the file
        try:
            file_path = os.path.join(DETECTION_DIR, record.filename)
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"Deleted file: {file_path}")
            else:
                print(f"File not found: {file_path}")

            # delete spectrograms if they exist
            file_path = os.path.join(THUMB_DIR, record.filename + ".png")
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"Deleted thumbnail: {file_path}")
            else:
                print(f"Thumbnail not found: {file_path}")

            file_path = os.path.join(FULL_DIR, record.filename + ".png")
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"Deleted spectrogram: {file_path}")
            else:
                print(f"Spectrogram not found: {file_path}")

                # Update the record in the database
            Detection.update(filename='').where(Detection.id == record.id).execute()
            print(f"Updated record id: {record.id}")

        except Exception as e:
            print(f"Error processing record id {record.id}: {e}")

if __name__ == '__main__':
    recordingcleanup(3)