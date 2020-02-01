from flask import Flask
from flask import jsonify
from google.cloud import storage
from google.oauth2 import service_account
from PIL import Image
import os
import mimetypes

GOOGLE_STORAGE_PROJECT = os.environ['GOOGLE_STORAGE_PROJECT']
GOOGLE_STORAGE_BUCKET = os.environ['GOOGLE_STORAGE_BUCKET']
BASE_URL = os.environ['BASE_URL']
METADATA_PATH = os.environ['METADATA_PATH']

app = Flask(__name__)

BASES = ['20B2AA', 'F0E68C', 'A52A2A', 'F08080', '4682B4', '9932CC', '2F4F4F', 'FFDAB9', '00FFFF', '6B8E23', 'FF4500', 'FFD700', '87CEEB', '0000CD', 'F0FFFF', 'FFE4B5', '8B008B', 'DC143C', '7FFF00', 'CD853F']

@app.route('/<token_id>')
def metadata(token_id):
    token_id = int(token_id)
    
    return "{}{}{}/meta.json".format(BASE_URL, METADATA_PATH, token_id)

@app.route('/create/<token_id>', methods=['GET', 'POST'])
def create(token_id):
    token_id = int(token_id)
    
    base = BASES[token_id % len(BASES)]
    image_url = "{}{}{}/blocklytics-cool.png".format(BASE_URL, METADATA_PATH, token_id)
    meta = {
        'name': "Pools.fyi Promoted Pool",
        'description': "The owner of this token is granted the right to promote a pool on https://pools.fyi, subject to the following:\nTERMS AND CONDITIONS\n1. Contact hello@blocklytics.org to initiate the redemption process.\n2. Scheduling will be handled on a first-come, first-served basis. Schedule early to avoid disappointment!\n3. The promoted pool will be displayed for a period of time as determined by the individual token's attributes.\n4. Redemption rights for the token expire as determined by the individual token's attributes.\n5. Where feasible, Blocklytics Ltd will enable an \"Add Liquidity\" feature for the promoted pool\n6. Blocklytics Ltd reserves the right to refuse redemption and/or change the promoted pool.\n7. Blocklytics Ltd will endeavour to refund a token redeemer in case redemption is not possible or the promoted pool was not advertised for the full period.",
        'image': image_url,
        'external_url': 'https://pools.fyi'
    }
    if request.json:
        meta = request.json
    _upload_metadata(meta)
    _upload_image(['images/bases/base-{}.png'.format(base),
                    'images/blocklytics-cool.png'],
                    token_id)

def _upload_metadata(metadata):
    blob = _get_bucket().blob("{}{}/meta.json".format(METADATA_PATH, token_id))
    blob.upload_from_string(filename=output_path)

def _upload_image(image_files, token_id):
    composite = None
    for image_file in image_files:
        foreground = Image.open(image_file).convert("RGBA")

        if composite:
            composite = Image.alpha_composite(composite, foreground)
        else:
            composite = foreground

    output_path = "images/output/{}.png".format(token_id)
    composite.save(output_path)

    blob = _get_bucket().blob("{}{}/blocklytics-cool.png".format(METADATA_PATH, token_id))
    blob.upload_from_filename(filename=output_path)


def _get_bucket():
    credentials = service_account.Credentials.from_service_account_file('credentials/google-storage-credentials.json')
    if credentials.requires_scopes:
        credentials = credentials.with_scopes(['https://www.googleapis.com/auth/devstorage.read_write'])
    client = storage.Client(project=GOOGLE_STORAGE_PROJECT, credentials=credentials)
    return client.get_bucket(GOOGLE_STORAGE_BUCKET)


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)