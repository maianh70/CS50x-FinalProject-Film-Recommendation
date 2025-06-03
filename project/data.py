import pandas as pd




class Data():
    def __init__(self, filepath):
        self.df = pd.read_csv(filepath)

    def drop_dup(self):
        return self.df.drop_duplicates(subset=["plot_synopsis"])[["imdb_id", "plot_synopsis"]].reset_index(drop=True)


    def matching(self, chosen_plots):
        return self.drop_dup()[self.drop_dup()["plot_synopsis"].isin(chosen_plots)]["imdb_id"].tolist()

    def id_return(self, genre):
        id_list = self.df[self.df["genres"].str.contains(genre, case=False, na=False)]["imdb_id"].tolist()
        if len(id_list) > 21:
            return id_list[:21]
        return id_list







