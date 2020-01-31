import wikipedia_histories

golden_swallow = wikipedia_histories.get_history('Golden swallow')

ratings = [revision.time for revision in golden_swallow]
print(ratings)

df = wikipedia_histories.build_df(golden_swallow)

print(df.head())