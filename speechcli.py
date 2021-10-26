import argparse
import sys, os
import pathlib

from transcriber import WAVTranscriber

parser = argparse.ArgumentParser(description="Convert speech audio files to text with Google Speech To Text")
parser.add_argument("key", help="The API Key")
parser.add_argument("input", help="The input audio file")
parser.add_argument("language", help="The language of the audio")
parser.add_argument("-o", "--output", help="The output file where text will be saved", default="output.txt")

#Language choice
LANGUAGES = ['en-US', 'hi-IN', 'en-IN']
SUPPORTED = ['.wav']

def speechconvert_file(language, inputf, outputf, keyf):
    ext = inputf[inputf.rfind("."):]
    if ext not in SUPPORTED:
        print("Error: Input file format is not supported")
        sys.exit(0)
    transcriber = WAVTranscriber(inputf, language)
    with open(outputf, "w", encoding="utf-8") as op:
        for transcribed in transcriber:
            op.write(transcribed)
            op.write("\n\n")
            percent = transcriber.getelapsedpercentage()
            print("Completed {:0.2f}%".format(percent))

args = parser.parse_args()

if args.language not in LANGUAGES:
    print("Error: Unsupported language provided")
    sys.exit(0)
elif os.path.isdir(args.input) == False:
    speechconvert_file(args.language, args.input, args.output, args.key)
else:
    print("Error: Input file is a directory. Please provide an audio file")
    sys.exit(0)