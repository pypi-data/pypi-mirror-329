# pubmed_meta_analyzer/extract_metadata.py
# This script uses functions from the PubMed Data Extraction repository
# Source: https://github.com/TLDWTutorials/PubmedAPI
# Licensed under the MIT License

import pandas as pd  # Importing pandas for data manipulation and DataFrame operations
import json  # Importing json for handling JSON data (though not used in this script)
from Bio import Entrez  # Importing Entrez from Bio for accessing PubMed data

def extract_metadata(authors=None, topics=None, date_range=None, email=None):
    """
    Extracts PubMed metadata based on the provided search parameters.

    This function queries PubMed using the Entrez API to retrieve metadata for articles
    that match the specified authors, topics, and date range. The results are returned
    as a pandas DataFrame containing details such as PMID, title, abstract, journal,
    keywords, URL, and publication year/month.

    Args:
        authors (list): List of authors to search for. Each author is queried in the format 'Author Name[Author]'.
        topics (list): List of topics to search for. Each topic is queried in the format 'Topic[Title/Abstract]'.
        date_range (str): Date range in the format '("YYYY/MM/DD"[Date - Create] : "YYYY/MM/DD"[Date - Create])'.
                         This specifies the publication date range for the articles.
        email (str): Email address for Entrez. Required by the Entrez API to identify the user.

    Returns:
        pd.DataFrame: DataFrame containing the extracted metadata with columns:
                      - PMID: PubMed ID of the article
                      - Title: Title of the article
                      - Abstract: Abstract of the article (if available)
                      - Journal: Journal where the article was published
                      - Keywords: Keywords associated with the article (if available)
                      - URL: URL to the article on PubMed
                      - Year: Publication year
                      - Month: Publication month

    Raises:
        ValueError: If the email or date_range is not provided.
    """
    if not email:
        raise ValueError("Email is required for Entrez.")  # Email is mandatory for Entrez API usage

    Entrez.email = email  # Set the email for Entrez API

    queries = []  # Initialize an empty list to store search query components

    # Construct author queries if authors are provided
    if authors:
        author_queries = ['{}[Author]'.format(author) for author in authors]  # Format each author as 'Author Name[Author]'
        queries.append('(' + ' OR '.join(author_queries) + ')')  # Combine author queries with OR logic

    # Construct topic queries if topics are provided
    if topics:
        topic_queries = ['{}[Title/Abstract]'.format(topic) for topic in topics]  # Format each topic as 'Topic[Title/Abstract]'
        queries.append('(' + ' AND '.join(topic_queries) + ')')  # Combine topic queries with AND logic

    if not date_range:
        raise ValueError("Date range is required.")  # Date range is mandatory for filtering articles

    # Combine all queries with AND logic and append the date range
    full_query = ' AND '.join(queries) + ' AND ' + date_range

    # Perform the PubMed search using the constructed query
    handle = Entrez.esearch(db='pubmed', retmax=300000, term=full_query)  # Search PubMed with the query
    record = Entrez.read(handle)  # Read the search results
    id_list = record['IdList']  # Extract the list of PubMed IDs (PMIDs) from the results

    # Initialize an empty DataFrame to store the extracted metadata
    df = pd.DataFrame(columns=['PMID', 'Title', 'Abstract', 'Journal', 'Keywords', 'URL', 'Year', 'Month'])

    # Iterate over each PMID to fetch detailed metadata
    for pmid in id_list:
        handle = Entrez.efetch(db='pubmed', id=pmid, retmode='xml')  # Fetch detailed metadata for the PMID in XML format
        records = Entrez.read(handle)  # Read the fetched metadata

        # Extract relevant details from the metadata
        for record in records['PubmedArticle']:
            title = record['MedlineCitation']['Article']['ArticleTitle']  # Extract the article title
            # Extract the abstract if available, otherwise set it to an empty string
            abstract = ' '.join(record['MedlineCitation']['Article']['Abstract']['AbstractText']) if 'Abstract' in record['MedlineCitation']['Article'] and 'AbstractText' in record['MedlineCitation']['Article']['Abstract'] else ''
            journal = record['MedlineCitation']['Article']['Journal']['Title']  # Extract the journal title
            # Extract keywords if available, otherwise set it to an empty string
            keywords = ', '.join(keyword['DescriptorName'] for keyword in record['MedlineCitation']['MeshHeadingList']) if 'MeshHeadingList' in record['MedlineCitation'] else ''
            url = f"https://www.ncbi.nlm.nih.gov/pubmed/{pmid}"  # Construct the URL to the article
            pub_date = record['MedlineCitation']['Article']['Journal']['JournalIssue'].get('PubDate', {})  # Extract publication date
            year = pub_date.get('Year', 'Unknown')  # Extract publication year, default to 'Unknown' if not available
            month = pub_date.get('Month', 'Unknown')  # Extract publication month, default to 'Unknown' if not available

            # Create a new row with the extracted metadata
            new_row = pd.DataFrame({
                'PMID': [pmid],
                'Title': [title],
                'Abstract': [abstract],
                'Journal': [journal],
                'Keywords': [keywords],
                'URL': [url],
                'Year': [year],
                'Month': [month]
            })

            # Append the new row to the DataFrame
            df = pd.concat([df, new_row], ignore_index=True)

    return df  # Return the DataFrame containing all extracted metadata