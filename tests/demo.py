import wikipedia_histories

golden_swallow = wikipedia_histories.get_history('Golden swallow')

df = build_df(golden_swallow)

df.head