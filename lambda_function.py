import json
import torch
import zipfile
import torchaudio
import urllib
from glob import glob
import boto3

device = torch.device('cpu')  # gpu also works, but our models are fast enough for CPU

model, decoder, utils = torch.hub.load(repo_or_dir='snakers4/silero-models',
                                       model='silero_stt',
                                       language='en', # also available 'de', 'es'
                                       device=device)
print("hello")

(read_batch, split_into_batches,
 read_audio, prepare_model_input) = utils

s3 = boto3.client("s3")



def lambda_handler(event, context):
    # TODO implement
    print("inside lambda_handler")
    print("Received event: " + json.dumps(event, indent=2))
    print(event)
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    print(bucket,key)
    
    # key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')

    tmp_filename = '/tmp/' + str(key)
    print(tmp_filename)
    s3.download_file(bucket, key, tmp_filename)


    test_files = glob(tmp_filename)
    batches = split_into_batches(test_files, batch_size=1)
    input = prepare_model_input(read_batch(batches[0]),
                                device=device)

    output = model(input)
    for example in output:
        print(decoder(example.cpu()))
    
