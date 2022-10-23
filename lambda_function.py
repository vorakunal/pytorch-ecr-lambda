import json
import torch
import zipfile
import torchaudio
import urllib
from glob import glob

device = torch.device('cpu')  # gpu also works, but our models are fast enough for CPU

model, decoder, utils = torch.hub.load(repo_or_dir='snakers4/silero-models',
                                       model='silero_stt',
                                       language='en', # also available 'de', 'es'
                                       device=device)
print("hello")

(read_batch, split_into_batches,
 read_audio, prepare_model_input) = utils



def lambda_handler(event, context):
    # TODO implement
    print("inside lambda_handler")
    print("Received event: " + json.dumps(event, indent=2))
    print(event)
    bucket = event['Records'][0]['s3']['bucket']['name']
    
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')

    test_files = glob(key)
    batches = split_into_batches(test_files, batch_size=1)
    input = prepare_model_input(read_batch(batches[0]),
                                device=device)

    output = model(input)
    for example in output:
        print(decoder(example.cpu()))
    
    print(bucket,key)
