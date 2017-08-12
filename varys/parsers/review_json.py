import re


def create_cleaned_text(text):
    return [x.strip() for x in  text.split('\n') if x.strip()]

def date_index(cleaned_text_list):
    return cleaned_text_list.index(extract_date(cleaned_text_list))

def extract_date(cleaned_text_list):
    match_list = [element
                  for element in cleaned_text_list
                  if re.fullmatch('- \d\d.\d\d.\d\d', element)]
    return match_list[0]

def extract_helpful_count(cleaned_text_list):
    helpful_word_list = cleaned_text_list[-1].split()
    yes_index = helpful_word_list.index('Yes')
    return int(helpful_word_list[yes_index + 2])

def extract_not_helpful_count(cleaned_text_list):
    helpful_word_list = cleaned_text_list[-1].split()
    no_index = helpful_word_list.index('No')
    return int(helpful_word_list[no_index + 2])

def extract_out_of(cleaned_text_list):
    out_of_index = cleaned_text_list.index('out of')
    return cleaned_text_list[out_of_index + 1]

def extract_quick_take(cleaned_text_list):
    starts_with = extract_starts_with(cleaned_text_list, 'Quick Take:')
    return list(map(str.strip, starts_with.split(','))) if starts_with else None

def extract_rating(cleaned_text_list):
    out_of_index = cleaned_text_list.index('out of')
    return cleaned_text_list[out_of_index - 1]

def extract_review_text(cleaned_text_list):
    review_begin_index = date_index(cleaned_text_list) + 1
    review_end_index = len(cleaned_text_list) - 1
    review_text_list = cleaned_text_list[review_begin_index : review_end_index]
    return '\n'.join([text.strip() 
                      for text in review_text_list
                      if not text.startswith('Quick Take:')])

def extract_starts_with(cleaned_text_list, text):
    extract_list = [x.replace(text, '').strip() 
                    for x in cleaned_text_list 
                    if x.startswith(text)]

    return extract_list[0] if extract_list else None

def extract_title(cleaned_text_list):
    out_of_index = cleaned_text_list.index('out of')

    if cleaned_text_list[out_of_index + 2].startswith('- '):
        return None
    else:
        return cleaned_text_list[out_of_index + 2]

def from_review(review):
    cleaned_text_list = create_cleaned_text(review)

    return {
        'user_name': cleaned_text_list[0].replace('(read all my reviews)', '').strip(),
        'location': extract_starts_with(cleaned_text_list, 'Location:'),
        'age': extract_starts_with(cleaned_text_list, 'Age:'),
        'rating': extract_rating(cleaned_text_list),
        'rating_out_of': extract_out_of(cleaned_text_list),
        'title': extract_title(cleaned_text_list),
        'date': extract_date(cleaned_text_list).split()[1],
        'quick_take': extract_quick_take(cleaned_text_list),
        'review_text': extract_review_text(cleaned_text_list), #currently this only pulls the last paragraph, you need to change this to pull the entire review
        'others_thought_helpful_count': extract_helpful_count(cleaned_text_list), 
        'others_thought_not_helpful_count': extract_not_helpful_count(cleaned_text_list)
    }
