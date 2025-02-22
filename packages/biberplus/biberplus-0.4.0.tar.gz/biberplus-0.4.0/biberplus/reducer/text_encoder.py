from biberplus.tagger import calculate_tag_frequencies
from biberplus.tagger.constants import BIBER_PLUS_TAGS, DOC_TAGS


def encode_text(config, text, round_to=10):
    frequencies_df = calculate_tag_frequencies(text, config=config)
    encodings = {}

    biber_tags = BIBER_PLUS_TAGS + DOC_TAGS
    binary_tags = ['BIN_' + tag for tag in biber_tags]

    # Split the counts by type
    if config['binary_tags']:
        binary_frequencies = frequencies_df[frequencies_df['tag'].isin(binary_tags)]
        encodings['binary'] = binary_frequencies[['mean', 'std']].to_numpy().flatten().round(round_to).tolist()

    if config['function_words']:
        fw_frequencies = frequencies_df[~frequencies_df['tag'].isin(biber_tags + binary_tags)]
        encodings['function_words'] = fw_frequencies.drop('tag', axis=1).to_numpy().flatten().round(round_to).tolist()

    frequencies_df = frequencies_df[frequencies_df['tag'].isin(biber_tags)]
    encodings['biber'] = frequencies_df.drop('tag', axis=1).to_numpy().flatten().round(round_to).tolist()

    return encodings
