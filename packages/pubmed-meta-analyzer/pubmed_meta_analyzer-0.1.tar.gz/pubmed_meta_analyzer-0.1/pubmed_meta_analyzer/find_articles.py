import pandas as pd
import re

def find_matching_sentences(abstract, terms):
    """
    Finds sentences in an abstract that contain any of the search terms.

    Args:
        abstract (str): The abstract text.
        terms (list): List of search terms.

    Returns:
        list: List of matching sentences.
    """
    sentences = re.split(r'(?<=[.!?]) +', abstract)
    matching_sentences = []
    for sentence in sentences:
        if any(re.search(r'\b' + re.escape(term) + r'\b', sentence, re.IGNORECASE) for term in terms):
            matching_sentences.append(sentence)
    return matching_sentences

def find_articles(terms_file_path, excel_file_path, output_file_path):
    """
    Finds articles containing the search terms and saves the results to a file.

    Args:
        terms_file_path (str): Path to the text file containing search terms.
        excel_file_path (str): Path to the Excel file containing metadata.
        output_file_path (str): Path to save the output results.
    """
    with open(terms_file_path, 'r') as file:
        search_terms = [line.strip() for line in file.readlines()]

    df = pd.read_excel(excel_file_path)

    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        total_articles = len(df)
        term_percentages = {}

        for term in search_terms:
            articles_with_keyword = 0

            for index, row in df.iterrows():
                abstract = row['Abstract']
                if pd.isna(abstract):
                    continue

                matching_sentences = find_matching_sentences(abstract, [term])
                if matching_sentences:
                    articles_with_keyword += 1

            percentage = (articles_with_keyword / total_articles) * 100
            term_percentages[term] = percentage

        sorted_terms = sorted(term_percentages.keys(), key=lambda x: term_percentages[x], reverse=True)

        for term in sorted_terms:
            output_file.write(f"Search Term: {term}\n")
            output_file.write("=" * 50 + "\n")

            for index, row in df.iterrows():
                abstract = row['Abstract']
                if pd.isna(abstract):
                    continue

                matching_sentences = find_matching_sentences(abstract, [term])
                if matching_sentences:
                    output_file.write(f"PMID: {row['PMID']}\n")
                    output_file.write(f"Title: {row['Title']}\n")
                    output_file.write(f"URL: {row['URL']}\n")
                    output_file.write("Matching Sentences:\n")
                    for sentence in matching_sentences:
                        output_file.write(f" - {sentence}\n")
                    output_file.write("-" * 50 + "\n")

            output_file.write(f"\nPercentage of articles containing '{term}': {term_percentages[term]:.2f}%\n")
            output_file.write("\n\n")