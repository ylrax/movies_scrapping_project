import pandas as pd

from imdb.imdb_bot_scrapper import BASE_FILE, RELATED_LINKS_DATA


# Insert the scrapped links on the links visited into the main base file.
dfd = pd.read_csv(BASE_FILE, sep=',')
# Append new ones
new_df = pd.read_csv(RELATED_LINKS_DATA, names=["titleId"])
newcols = list(dfd.columns)[1:]
updated = new_df.reindex([*new_df.columns, *newcols], axis=1)
updated["captured"] = 0

complete = pd.concat([dfd, updated])
complete.drop_duplicated(subset=["titleId"], keep="first", inplace=True)
complete.to_csv(path_or_buf="/home/pi/repos/fa_scrapper/final_movies_extra.csv",
                sep=',', encoding='UTF8', index=False)
