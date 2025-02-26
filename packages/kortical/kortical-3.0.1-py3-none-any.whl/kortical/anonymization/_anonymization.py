import base64
import xxhash
import random
import re
from sklearn import preprocessing

from kortical.data import get_names
from kortical.spacy_models import load_model

nlp = load_model("en_core_web_sm-3.4.1")
spacy_words_raw = set(nlp.vocab.strings)

special_characters_regex = re.compile(r'[^A-Za-z0-9]+')
postcode_regex = re.compile(r'(^|\s)([A-Za-z]{1,2}[0-9R][0-9A-Za-z]? ?[0-9][A-Za-z]{2})(\s|$)')

NAMES = get_names()
spacy_words_raw.update({'sponsorships', 'impossibly', 'lowkey', 'fyi', 'pager', 'voicemail', 'cc', 'number'})
spacy_words = spacy_words_raw.difference(NAMES)


def hash_text(text):
    x = xxhash.xxh64()
    x.update(text)
    x = x.digest()
    x = base64.b64encode(x)
    x = x.decode('iso-8859-1')
    x = special_characters_regex.sub('', x)
    return x


def process_df(df, tokenize_columns=None, numeric_columns=None, categorical_columns=None, scramble_column_names=False,
               allow_lower_case_names=True, tokenize_organizations=True, tokenize_time=False, tokenize_locations=True,
               tokenize_numbers=True, normalize_numeric_columns=False):
    # Set default values
    if tokenize_columns is None:
        tokenize_columns = []
    if numeric_columns is None:
        numeric_columns = []
    if categorical_columns is None:
        categorical_columns = []

    columns = tokenize_columns + numeric_columns + categorical_columns
    df = tokenize(df, tokenize_columns, allow_lower_case_names=allow_lower_case_names,
                  tokenize_organizations=tokenize_organizations, tokenize_time=tokenize_time,
                  tokenize_locations=tokenize_locations, tokenize_numbers=tokenize_numbers)
    # Don't jitter by default as testing showed this tanked model performance
    #df = jitter(df, numeric_columns)
    df = add_noise(df, numeric_columns + categorical_columns)
    if len(numeric_columns) > 0 and normalize_numeric_columns:
        df = normalize(df, numeric_columns)
    if scramble_column_names:
        df, columns = globals()['scramble_column_names'](df, columns)
    return df, columns


def _tokenize_parse_word(word, allow_lower_case_names, tokenize_numbers):
    if word.isnumeric():
        return f"NUMBER_{hash_text(word)}" if tokenize_numbers else word

    if word.lower() in spacy_words or (word.islower() and allow_lower_case_names and word in spacy_words_raw):
        return word

    if word.lower() in NAMES:
        return f"PERSON_{hash_text(word)}"
    elif word.split('_')[0] not in ['PERSON', 'ORG', 'GPE', 'TIME', 'CARDINAL', 'DATE', 'QUANTITY', 'ORDINAL', 'UNKNOWN', 'LOC', 'FAC', 'GEO', 'MONEY', 'NUMBER', 'LOCATION', 'DATETIME', 'POSTCODE']:
        h = hash_text(word)
        return f"UNKNOWN_{h}"
    return word


def tokenize(df, columns, allow_lower_case_names=True, tokenize_organizations=True, tokenize_time=False, tokenize_locations=True, tokenize_numbers=True):
    for column_name in columns:
        for index, row in df.iterrows():
            text = str(row[column_name])
            new_text = ""

            # Process postcodes
            if tokenize_locations:
                offset = 0
                matches = postcode_regex.finditer(text)
                for m in matches:
                    positions = list(m.span())
                    groups = m.groups()
                    positions[0] += len(groups[0])
                    positions[1] -= len(groups[2])
                    postcode = text[positions[0]:positions[1]]
                    postcode = postcode.upper().replace(' ', '')
                    postcode = f'{postcode[:-1]}_'
                    token = f"POSTCODE_{postcode}"
                    text = "".join((text[:positions[0] + offset], token, text[positions[1] + offset:]))
                    offset += len(token) - (positions[1] - positions[0])

            label_map = {
                'CARDINAL': 'NUMBER',
                'QUANTITY': 'NUMBER',
                'ORDINAL': 'NUMBER',
                'MONEY': 'NUMBER',
                'LOC': 'LOCATION',
                'GEO': 'LOCATION',
                'GPE': 'LOCATION',
                'TIME': 'DATETIME',
                'DATE': 'DATETIME',
            }
            process_entities = ['PERSON', 'UNKNOWN']
            if tokenize_organizations:
                process_entities += ['ORG']
            if tokenize_time:
                process_entities += ['TIME', 'DATE']
            if tokenize_locations:
                process_entities += ['LOC', 'GEO', 'GPE']
            if tokenize_numbers:
                process_entities += ['CARDINAL', 'QUANTITY', 'ORDINAL', 'MONEY']

            offset = 0
            # Spacy
            doc = nlp(text)
            for ent in doc.ents:
                # print(ent.text, ent.label_, spacy.explain(ent.label_))
                if ent.label_ in process_entities:
                    label = label_map.get(ent.label_, ent.label_)
                    token = f"{label}_{hash_text(ent.text)}"
                    text = "".join((text[:ent.start_char + offset], token, text[ent.end_char + offset:]))
                    offset += len(token) - (ent.end_char - ent.start_char)
            # Custom
            word = ""
            has_upper_case = False
            for c in text:
                has_upper_case |= c.isupper()
                if c.isalnum() or c == '_':
                    word += c
                elif len(word) > 0:
                    new_text += _tokenize_parse_word(word, allow_lower_case_names, tokenize_numbers)
                    word = ""
                    new_text += c
                else:
                    new_text += c
            if len(word) > 0:
                if word.lower() in spacy_words:
                    new_text += word
                else:
                    new_text += _tokenize_parse_word(word, allow_lower_case_names, tokenize_numbers)

            df.loc[index, column_name] = new_text

    return df


def add_noise(df, columns, percentage=0.02):
    for column_name in columns:
        num_rows = max(int(len(df) * percentage), 1)
        noise_indices = df.sample(num_rows).index
        sample = df[column_name].sample(num_rows)

        df.loc[noise_indices, column_name] = sample.values

    return df


def normalize(df, columns):
    x = df[columns].values
    min_max_scaler = preprocessing.MinMaxScaler()
    x_scaled = min_max_scaler.fit_transform(x)

    df[columns] = x_scaled

    return df


def jitter(df, columns, percentage_of_population_to_jitter=0.2, percentage_of_standard_deviation=0.1):
    for column_name in columns:
        standard_deviation = df[column_name].std()
        _min = df[column_name].min()
        _max = df[column_name].max()
        df[column_name] = df[column_name].map(lambda x: x + (1 if random.random() < percentage_of_population_to_jitter else 0) * (1 if random.random() < 0.5 else -1) * random.random() * percentage_of_standard_deviation * standard_deviation)

    return df


def scramble_column_names(df, columns):
    new_columns = [hash_text(column_name) for column_name in columns]
    df[new_columns] = df[columns]
    for c in columns:
        del df[c]
    return df, new_columns
