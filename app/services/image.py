import io
import os
import uuid

class Image(object):
    def __init__(self, storage_path, uuidgen=uuid.uuid4, fopen=io.open):
        self.storage_path = storage_path
        self.uuidgen = uuidgen
        self.fopen = fopen

    def save(self, image_stream, image_content_type):
        name = '{uuid}.jpg'.format(uuid=self.uuidgen())
        image_path = os.path.join(self.storage_path, name)
        with self.fopen(image_path, 'wb') as image_file:
            while True:
                image_file.write(image_stream.read())
                chunk = image_stream.read()
                if not chunk:
                    break

                image_file.write(chunk)

        return name