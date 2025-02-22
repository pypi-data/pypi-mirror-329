import os
import re
import stanza

from Levenshtein import distance
from stanza.models.common.doc import Document
from huggingface_hub import hf_hub_download

from .lexicon import lexicon
from .cltk import normalize_grc  # For normalizing texts


def lemmatize(
        text, use_lexicon=True,
        lemma_model_or_pt_file='prhbrt/ancient-greek-inscriptions-lematizer-base',
        return_type='document'):
    """
    Lemmatizes (and tokenizes) Ancient Greek inscriptions given custom rules,
    a custom trained model in Stanza and a lexicon lookup.

    :param text str: inscription text to be lemmatized
    :param use_lexicon bool: enable or disable the correction by the lexicon lookup
    :param lemma_model_or_pt_file str: huggingface tag for lemmatizer, should contain
                                       `grc_agile_lemmatizer.pt` or pytorch filename,
                                       should end with `.pt` and exist.
    :param return_type: `"dict"` or `"document"`
    :return: Stanza Document containing id, text, lemma, start_char and end_char annotations,
             or list of dictionaries of the same if return_type == `dict`
    """

    if return_type not in {'dict', 'document'}:
        raise ValueError(f"Unknown `return_type`, should be `'dict'` or `'document'`: {return_type}")

    # Handle extra-alphabetical characters
    original_text = normalize_grc(text)
    original_text = re.sub('[|∣·∙∶:,.⁝⋮⁞⁙“”]+', ' \g<0> ', original_text)  # Pre-tokenize
    original_text = re.sub(' +', ' ', original_text)
    original_text = re.sub('\n+', '\n', original_text)  # Sentence tokenization not supported

    # Add custom rules (chars have been normalized)
    processed_text = re.sub('(?<!\s)[Ϝϝh](?!\s)', '', original_text)  # [Ϝϝh] within token
    processed_text = re.sub('(?<=\s)[Ϝϝh](?!\s)(?=.)', '', processed_text)  # [Ϝϝh] begin of token
    processed_text = re.sub('(?<=.)(?<!\s)[Ϝϝh](?=\s)', '', processed_text)  # [Ϝϝh] end of token
    processed_text = re.sub('(κς)|(κσ)|(χς)|(χσ)', 'ξ', processed_text)
    processed_text = re.sub('(Κς)|(Κσ)|(Χσ)|(Χς)', 'Ξ', processed_text)
    processed_text = re.sub('(φς)|(φσ)', 'ψ', processed_text)
    processed_text = re.sub('(Φς)|(Φσ)', 'Ψ', processed_text)
    processed_text = re.sub(' [|∣·∙∶:,.⁝⋮⁞⁙“”]+', '', processed_text)

    if lemma_model_or_pt_file.endswith('.pt') and os.path.exists(lemma_model_or_pt_file):
        lemma_model_path = lemma_model_or_pt_file
    else:
        lemma_model_path = hf_hub_download(repo_id=lemma_model_or_pt_file, filename="grc_agile_lemmatizer.pt")

    lemma_nlp = stanza.Pipeline(
        lang='grc', processors='tokenize,lemma', tokenize_pretokenized=True,
        lemma_model_path=lemma_model_path, verbose=False)
    token_nlp = stanza.Pipeline(lang='grc', processors='tokenize', tokenize_pretokenized=True, verbose=False)
    token_dict = token_nlp(original_text).to_dict()[0]  # Dict for all tokens (lemmas to be inserted)
    lemma_dict = lemma_nlp(processed_text).to_dict()[0]  # Dict for lemmas given by model
    

    # Add lemmas to token dict
    lemma_i = 0
    for token_i, token in enumerate(token_dict):
        if re.search('[|∣·∙∶:,.⁝⋮⁞⁙“”]+', token['text']):  # Custom lemmatization
            token_dict[token_i]['lemma'] = token['text']
        else:
            try:
                predicted = lemma_dict[lemma_i]['lemma']  # Lemmatization by model
            except KeyError:  # No lemma
                predicted = ""
            # Handle lexicon correction
            if use_lexicon:
                if predicted != "" and predicted not in lexicon:
                    lowest = distance(lexicon[0], predicted)
                    closest = lexicon[0]
                    for entry in lexicon[1:]:
                        dist = distance(entry, predicted)
                        if dist == 1:  # Speed optimisation
                            closest = entry
                            break
                        elif dist < lowest:
                            lowest = dist
                            closest = entry
                    token_dict[token_i]['lemma'] = closest
                    if return_type == 'dict':
                        token_dict[token_i]['lemma_pred'] = predicted
                else:
                    token_dict[token_i]['lemma'] = predicted
                    if return_type == 'dict':
                        token_dict[token_i]['lemma_pred'] = predicted
            else:
                token_dict[token_i]['lemma'] = predicted
                if return_type == 'dict':
                    token_dict[token_i]['lemma_pred'] = predicted
            lemma_i += 1
    if return_type == 'dict':
        return token_dict
    return Document([token_dict])
