from datetime import datetime

def get_todays_date() -> str:
    return datetime.now().strftime("%Y-%m-%d")

def clean_results_string(results_string : str) -> str:
    return '\n'.join([line.strip() for line in results_string.split('\n')])

def capitalise_first_letter(word : str) -> str:
    return word[0].upper() + word[1:]
