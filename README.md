# Wikipedia Histories

A simple tool to pull the complete edit history of a Wikipedia page in a variety of formats, including JSON, DataFrame, or directly as an object.

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

  # Generate a JSON with text and metadata from the list of versions
  >>> jsonified = wikipedia_histories.build_json(golden_swallow)
```


## Installation

To install Wikipedia Histories, simply run:

```
$ pip install wikipedia-histories
```

Wikipedia Histories is compatible with Python 3.6+.