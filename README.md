# Wikipedia Histories

A simple tool to pull the complete edit history of a Wikipedia page in a variety of formats, including JSON, DataFrame, or directly as an object.

```python
  >>> import wikipedia_histories
  
  # Generate a list of revisions for a specified page
  >>> golden_swallow = get_history('Golden swallow')
  
  # Show the revision IDs for every edit
  >>> golden_swallow
  # [130805848, 162259515, 167233740, 195388442, ...
  
  # Show the user who made a specific edit
  >>> golden_swallow[16].user
  # u'Snowmanradio'
  
  # Show the text of at the time of a specific edit
  >>> golden_swallow[16].text
  # u'The Golden Swallow (Tachycineta euchrysea) is a swallow.  The Golden Swallow formerly'...
  >>> golden_swallow[200].text
  # u'The golden swallow (Tachycineta euchrysea) is a passerine in the swallow family'...

  # Generate a dataframe with text and metadata from a the list of revisions
  >>> build_df(golden_swallow)

  # Generate a JSON with text and metadata from the list of versions
  >>> build_json(golden_swallow)
```


## Installation

To install Wikipedia Histories, simply run:

``$ pip install wikipedia-histories``

Wikipedia Histories is compatible with Python 3.6+.