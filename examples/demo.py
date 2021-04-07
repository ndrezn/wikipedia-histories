import wikipedia_histories

golden_swallow = wikipedia_histories.get_history("Golden swallow", include_text=False)

df = wikipedia_histories.to_df(golden_swallow)

print(df)
