# Wikipedia Histories
![PyPI - Downloads](https://img.shields.io/pypi/dw/wikipedia-histories)


A tool to pull the complete revision history of a Wikipedia page.

## Installation

To install Wikipedia Histories, simply run:

```bash
 pip install wikipedia-histories
```

Wikipedia Histories is compatible with Python 3.6+.


## Usage
The module has basic functionality which allows it to be used to collect the revision history and metadata from a Wikipedia page in a convienent list of objects, which can be converted into a DataFrame. This also includes the article quality from every revision.

```python
  >>> import wikipedia_histories
  
  # Generate a list of revisions for a specified page
  >>> golden_swallow = wikipedia_histories.get_history('Golden swallow')
  
  # Show the revision IDs for every edit
  >>> golden_swallow
  # [130805848, 162259515, 167233740, 195388442, ...
  
  # Show the user who made a specific edit
  >>> golden_swallow[16].user
  # u'Snowmanradio'
  
  # Show the text of at the time of a specific edit
  >>> golden_swallow[16].content
  # u'The Golden Swallow (Tachycineta euchrysea) is a swallow.  The Golden Swallow formerly'...
  >>> golden_swallow[200].content
  # u'The golden swallow (Tachycineta euchrysea) is a passerine in the swallow family'...

  # Get the article rating at the time of the edit
  >>> ratings = [revision.rating for revision in golden_swallow]
  >>> ratings
  # ['NA', 'NA', 'NA', 'NA', 'stub', 'stub', ...

  # Get the time of each edit as a datetime object
  >>> times = [revision.time for revision in golden_swallow]
  >>> times
  # [datetime.datetime(2007, 5, 14, 16, 15, 31), datetime.datetime(2007, 10, 4, 15, 36, 29), ...

  # Generate a dataframe with text and metadata from a the list of revisions
  >>> df = wikipedia_histories.build_df(golden_swallow)
```

Additional metadata for the article, including 
An example of this workflow is available in `tests/demo.py`.

## Domain level analysis
This module also contains functionality for advanced analysis of large sets of Wikipedia articles by generation social networks based on the editors who edited an article. 

First, a domain is defined as a dictionary, where keys are domain names and values are lists of categories which represent that domain. For example, a set of domains representing "culture" and "politics":

```python
  culture = [
      "Category:Television_in_the_United_States",
      "Category:American_films",
      "Category:American_novels",
  ]
  politics = [
      "Category:Conservatism",
      "Category:Liberalism",
  ]
  domains = {
      "culture": culture,
      "politics": politics,
  }
```

The articles represented by those domains, up to a certain depth of nested categories, can be collected and saved as a `csv`, with the category and domain attributes attached using `wikipedia_histories.find_articles`. Once this set of articles is collected, the articles themselves can be downloaded using `wikipedia_histories.get_history()` either with revision text or without. This set of articles can be used for analysis on Wikipedia revision behavior across categories or domains. 

Once a set of articles is downloaded using this methodology, it's possible to collect aggregate metadata for those articles, including the number of unique editors, average added words per edit and average deleted words per edit, the article age, and the total number of edits, and save that information into a DataFrame using `wikipedia_histories.get_metadata()`.

An example of this workflow is avaialble in `tests/collect_articles.py`.


## Social network analysis
It is also possible to build and analyze the networks of users who edited those articles, and study how domains relate to one another. For this analysis, first a set of articles representing categorical domains must be downloaded using and saved to folders representing domains and the metadata sheet must be saved. 

Once this is set up, a set of networks representing connections within a domain or between domains can be generated using `wikipedia_histories.generate_networks()`. A `domain` is passed as input to signify which domain should be used to build the networks, if no `domain` is passed as input the networks generated will represent connections between categories from different domains. 

Each domain has a number of nodes input using the attribute `size`, and a certain number of networks is generated using the attribute `count`. Each network has an equal number of nodes from one of two categories selected from the metadata sheet (categories being from whichever domain is passed as input).



