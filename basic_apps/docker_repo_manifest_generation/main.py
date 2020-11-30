import os
import json
import requests
import boto3
from types import SimpleNamespace

DOCKER_DIRECTORY = '/var/lib/docker/image/overlay2'
REPO_NAME = os.getenv('REPO_NAME')
IMAGE_TAG = os.getenv('IMAGE_TAG')
REGISTRY_URL = os.getenv('REGISTRY_URL')

def main():
  ecr_client = boto3.client('ecr')

  # Downloads the repository image manifest which has the compressed layer digests and the image config manifest digest which are used to get the download links for each.
  repository_manifest = ecr_client.batch_get_image(
    repositoryName=REPO_NAME,
    imageIds=[
        {
            'imageTag': IMAGE_TAG,
        },
    ],
  )
  repository_manifest_json = json.loads(repository_manifest['images'][0]['imageManifest'], object_hook=lambda d: SimpleNamespace(**d))

  # Downloads the image manifest with the non-compressed layers sha256sums, these are the sum's docker normal reports, such as on a push.
  image_manifest_response = ecr_client.get_download_url_for_layer(
    repositoryName=REPO_NAME,
    layerDigest=repository_manifest_json.config.digest,
  )
  image_manifest = requests.get(image_manifest_response['downloadUrl'])
  image_manifest_json = json.loads(image_manifest.text, object_hook=lambda d: SimpleNamespace(**d))

  # Makes the required directories in case they don't exist already from docker. Such as first startup and not pushes/pulls have been made yet.
  os.makedirs(DOCKER_DIRECTORY+'/distribution/diffid-by-digest/sha256/', exist_ok=True)
  os.makedirs(DOCKER_DIRECTORY+'/distribution/v2metadata-by-diffid/sha256/', exist_ok=True)

  # TODO add additional checking for when layer counts dont match or empty, etc.

  # FIXME currently the below two file creations just write over any files if they exist already which isn't helpful if the machine will need to push the same layer to multiple repositories. The fix is to update any existing json in the file rather than overwriting.
  for image_layer, repo_layer in zip(image_manifest_json.rootfs.diff_ids, repository_manifest_json.layers):
    print(f'diffid-by-digest: {repo_layer.digest} ---- v2metadata-by-diffid: {image_layer}')

    with open(DOCKER_DIRECTORY+'/distribution/diffid-by-digest/sha256/'+repo_layer.digest[7:], 'w') as f:
      f.write(image_layer)

    with open(DOCKER_DIRECTORY+'/distribution/v2metadata-by-diffid/sha256/'+image_layer[7:], 'w') as f:
      jsdata = [{
        'Digest': repo_layer.digest,
        'SourceRepository': f'{REGISTRY_URL}/{REPO_NAME}',
        # While not required for generating the cache the below should be a calculation of auth details.
        'HMAC': 'PendingImprovements',
      }]
      f.write(json.dumps(jsdata))

if __name__ == '__main__':
  main()
