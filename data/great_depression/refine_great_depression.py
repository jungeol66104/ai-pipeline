import re
from tools import txt_space_remover, read_data_txt, check_text_tokens, write_data_txt


# great_depression
def refine_great_depression_1():
    txt_space_remover('great_depression','great_depression_1.txt')
    text = read_data_txt('great_depression','great_depression_1.txt')

    section_pattern = re.compile(r'(19\d{2}:)')
    section_matches = section_pattern.split(text)
    sections = [section_matches[i] + section_matches[i + 1].strip() for i in range(1, len(section_matches), 2) if section_matches[i + 1].strip()]

    result_text = ''
    for section in sections:
        year_pattern = re.compile(r'(19\d{2}):')
        year = year_pattern.search(section).group(1)
        event_pattern = re.compile(r'((January|Feburary|March|April|May|June|July|August|September|October|November|December)\s{0,5}(:|\d{1,2}\s{0,5}:))')

        section = re.sub(
            event_pattern,
            fr'\n\n{year} \1',
            section
        )

        result_text = result_text + section + "\n\n\n"
    check_text_tokens(result_text)
    write_data_txt('great_depression','great_depression_1.txt', result_text)
    return


def refine_great_depression_2():
    txt_space_remover('great_depression','great_depression_2.txt')
    text = read_data_txt('great_depression','great_depression_2.txt')

    section_pattern = re.compile(r'(19\d{1,2}\s{0,5}Year\s{0,5}:)')
    section_matches = section_pattern.split(text)

    sections = [section_matches[i] + section_matches[i + 1].strip() for i in range(1, len(section_matches), 2) if section_matches[i + 1].strip()]


    result_text = ''
    for section in sections:
        year_pattern = re.compile(r'(19\d{2})Year:')
        year = year_pattern.search(section).group(1)
        event_pattern = re.compile(r'((January|Feburary|March|April|May|June|July|August|September|October|November|December)\s{0,5}([-–]\s{0,5}(January|Feburary|March|April|May|June|July|August|September|October|November|December)|\d{1,2}|)\s{0,5}:)')

        section = re.sub(
            event_pattern,
            fr'\n\n{year} \1',
            section
        )
    #
        result_text = result_text + section + "\n\n\n"
    check_text_tokens(result_text)
    write_data_txt('great_depression','great_depression_2.txt', result_text)
    return


def refine_great_depression_3():
    txt_space_remover('great_depression','great_depression_3.txt')
    text = read_data_txt('great_depression','great_depression_3.txt')

    section_pattern = re.compile(r'(19\d{2}\s{0,5}:)')
    section_matches = section_pattern.split(text)

    sections = [section_matches[i] + section_matches[i + 1].strip() for i in range(1, len(section_matches), 2) if section_matches[i + 1].strip()]

    result_text = ''
    for section in sections:
        year_pattern = re.compile(r'(19\d{2}):')
        year = year_pattern.search(section).group(1)
        event_pattern = re.compile(r'((Jan(uary)?|Feb(urary)?|Mar(ch)?|Apr(il)?|May|Jun(e)?|Jul(y)?|Aug(ust)?|Sept(ember)?|Oct(ober)?|Nov(ember)?|Dec(ember)?)\s{0,5}.?\s{0,5}(\d{1,2}|\d{1,2}):)')

        section = re.sub(
            event_pattern,
            fr'\n\n{year} \1',
            section
        )

        result_text = result_text + section + "\n\n\n"
    check_text_tokens(result_text)
    write_data_txt('great_depression','great_depression_3.txt', result_text)
    return


def refine_great_depression_4():
    txt_space_remover('great_depression','great_depression_4.txt')
    text = read_data_txt('great_depression','great_depression_4.txt')

    section_pattern = re.compile(r'(19\d{2}\s{0,5}:)')
    section_matches = section_pattern.split(text)

    sections = [section_matches[i] + section_matches[i + 1].strip() for i in range(1, len(section_matches), 2) if section_matches[i + 1].strip()]

    result_text = ''
    for section in sections:
        year_pattern = re.compile(r'(19\d{2}):')
        year = year_pattern.search(section).group(1)
        event_pattern = re.compile(r'((Jan(uary)?|Feb(urary)?|Mar(ch)?|Apr(il)?|May|Jun(e)?|Jul(y)?|Aug(ust)?|Sept(ember)?|Oct(ober)?|Nov(ember)?|Dec(ember)?)\s{0,5}.?\s{0,5}(\d{1,2}|\d{1,2}):)')

        section = re.sub(
            event_pattern,
            fr'\n\n{year} \1',
            section
        )

        result_text = result_text + section + "\n\n\n"
    check_text_tokens(result_text)
    write_data_txt('great_depression','great_depression_4.txt', result_text)
    return


def refine_great_depression_5():
    txt_space_remover('great_depression','great_depression_5.txt')
    text = read_data_txt('great_depression','great_depression_5.txt')

    event_pattern = re.compile(
        r'(((January|Feburary|March|April|May|June|July|August|September|October|November|December)?\s{0,5}\d{1,2}?\s{0,5},?\s{0,5}19\d{2}))')

    text = re.sub(
        event_pattern,
        fr'\n\n\1: ',
        text
    )

    check_text_tokens(text)
    write_data_txt('great_depression','great_depression_5.txt', text)
    return


def refine_great_depression_6():
    txt_space_remover('great_depression','great_depression_6.txt')
    text = read_data_txt('great_depression','great_depression_6.txt')

    event_pattern = re.compile(
        r'((Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s{0,5}\d{1,2}\s{0,5},\s{0,5}\d{4})')

    text = re.sub(
        event_pattern,
        fr'\n\n\1: ',
        text
    )

    check_text_tokens(text)
    write_data_txt('great_depression','great_depression_6.txt', text)
    return

# refine_great_depression_1()
# refine_great_depression_2()
# refine_great_depression_3()
# refine_great_depression_4()
# refine_great_depression_5()
# refine_great_depression_6()

