from flask import Flask
from flask import jsonify
from google.cloud import storage
from google.oauth2 import service_account
from PIL import Image
import os
import mimetypes

GOOGLE_STORAGE_PROJECT = os.environ['GOOGLE_STORAGE_PROJECT']
GOOGLE_STORAGE_BUCKET = os.environ['GOOGLE_STORAGE_BUCKET']

app = Flask(__name__)

BASES = ['20B2AA', 'F0E68C', 'A52A2A', 'F08080', '4682B4', '9932CC', '2F4F4F', 'FFDAB9', '00FFFF', '6B8E23', 'FF4500', 'FFD700', '87CEEB', '0000CD', 'F0FFFF', 'FFE4B5', '8B008B', 'DC143C', '7FFF00', 'CD853F']


@app.route('/api/sponsored-pool/<token_id>')
def sponsored_pool(token_id):
    token_id = int(token_id)
    
    # base = BASES[token_id % len(BASES)]
    # image_url = _compose_image(['images/bases/base-%s.png' % base,
    #                             'images/blocklytics-cool.png'],
    #                            token_id)

    # attributes = []
    # _add_attribute(attributes, 'base', BASES, token_id)
    # _add_attribute(attributes, 'eyes', EYES, token_id)
    # _add_attribute(attributes, 'mouth', MOUTH, token_id)
    # _add_attribute(attributes, 'level', INT_ATTRIBUTES, token_id)
    # _add_attribute(attributes, 'stamina', FLOAT_ATTRIBUTES, token_id)
    # _add_attribute(attributes, 'personality', STR_ATTRIBUTES, token_id)
    # _add_attribute(attributes, 'aqua_power', BOOST_ATTRIBUTES, token_id, display_type="boost_number")
    # _add_attribute(attributes, 'stamina_increase', PERCENT_BOOST_ATTRIBUTES, token_id, display_type="boost_percentage")
    # _add_attribute(attributes, 'generation', NUMBER_ATTRIBUTES, token_id, display_type="number")

    return jsonify({'name': "Pools.fyi Sponsored Pool", 'token' : token_id })
    # return jsonify({
    #     'name': "Pools.fyi Sponsored Pool",
    #     'description': "Sponsored listing on Pools.fyi.",
    #     'image': image_url,
    #     'external_url': 'https://pools.fyi'
    # })

def _add_attribute(existing, attribute_name, options, token_id, display_type=None):
    trait = {
        'trait_type': attribute_name,
        'value': options[token_id % len(options)]
    }
    if display_type:
        trait['display_type'] = display_type
    existing.append(trait)


def _compose_image(image_files, token_id, path="meta"):
    composite = None
    for image_file in image_files:
        foreground = Image.open(image_file).convert("RGBA")

        if composite:
            composite = Image.alpha_composite(composite, foreground)
        else:
            composite = foreground

    output_path = "images/output/%s.png" % token_id
    composite.save(output_path)

    blob = _get_bucket().blob(f"{path}/{token_id}/blocky.png")
    blob.upload_from_filename(filename=output_path)
    return blob.public_url


def _get_bucket():
    credentials = service_account.Credentials.from_service_account_file('credentials/google-storage-credentials.json')
    if credentials.requires_scopes:
        credentials = credentials.with_scopes(['https://www.googleapis.com/auth/devstorage.read_write'])
    client = storage.Client(project=GOOGLE_STORAGE_PROJECT, credentials=credentials)
    return client.get_bucket(GOOGLE_STORAGE_BUCKET)


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)