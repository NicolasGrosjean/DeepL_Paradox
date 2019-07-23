import argparse
import requests
from tqdm import tqdm


def get_args():
    parser = argparse.ArgumentParser(description='Translate a yml Paradox file from English to French')
    parser.add_argument('basename', type=str, help='Path and basename of the file to translate')
    return parser.parse_args()


def read_paradox_file(file_path):
    res = []

    with open(file_path, 'r') as f:
        lines = f.readlines()

    first_line = True
    for line in lines:
        if first_line:
            first_line = False
            continue
        uncommented = line
        if '#' in line and ( not '"' in line or (line.find('#') < line.find('"'))):
            splitted_comments = line.split("#")
            if len(splitted_comments) == 0:
                continue
            uncommented = splitted_comments[0]
        if ':' not in uncommented:
            continue
        splitted = uncommented.split(':')
        key = splitted[0]
        text = splitted[1][2:]
        if len(splitted) > 2:
            for i in range(2, len(splitted)):
                text += ':' + splitted[1]
        start = text.find('"') + 1
        end = text.rfind('"')
        if start > end:
            print('Incorrect localisation text (ex: missing double quote at the end)')
            continue
        text = text[start:end]
        res.append({'key': key, 'text':text})
    return res


def read_api_key():
    with open('DeepL_key', 'r') as f:
        return f.readlines()[0].replace('\n', '')


def translate(text, api_key):
    api_endpoint = 'https://api.deepl.com/v2/translate'
    data = {'auth_key': api_key,
            'text': text,
            'source_lang': 'EN',
            'target_lang': 'FR'}
    r = requests.post(url=api_endpoint, data=data)
    if r.status_code == 200:
        return r.json()['translations'][0]['text']
    else:
        return text


if __name__ == '__main__':
    api_key_deepL = read_api_key()

    args = get_args()
    basename = args.basename
    source_file = basename + '_l_english.yml'
    dest_file = basename + '_l_french.yml'
    l = read_paradox_file(source_file)
    with open(dest_file, 'w', encoding='utf-8-sig') as f:
        f.write('l_french:\n\n')
        for line in tqdm(l):
            paragraphs = line['text'].split('\\n')
            translated_line = translate(paragraphs[0], api_key_deepL)
            if len(paragraphs) > 1:
                for paragraph in paragraphs[1:]:
                    translated_line += '\\n'
                    if len(paragraph) > 0:
                        translated_line += translate(paragraph, api_key_deepL)
            f.write(line['key'] + ':0 "' + translated_line + '"\n')
