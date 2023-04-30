import pandas as pd
import tkinter as tk
from tkinter import ttk
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("netflixViewingHistory.csv")
df['Date'] = pd.to_datetime(df['Date'], format='mixed')


class App:
    def __init__(self, master):
        self.master = master
        master.title("Netflix Viewing History")

        # Add a style to make the widgets look more modern
        self.style = ttk.Style()
        self.style.theme_use('clam')

        # Add a frame for the main content
        self.content_frame = ttk.Frame(self.master, padding="40 20")
        self.content_frame.pack()

        # Add a label for the title
        self.title_label = ttk.Label(
            self.content_frame, text="Netflix Viewing History", font=("Helvetica", 20))
        self.title_label.pack()

        # Add a separator for visual hierarchy
        self.separator = ttk.Separator(self.content_frame, orient='horizontal')
        self.separator.pack(fill='x', pady=20)

        # Add a label and entry for selecting the month
        self.month_label = ttk.Label(
            self.content_frame, text="Enter the month (MM): ")
        self.month_label.pack(side='left', padx=(0, 10))
        self.month_entry = ttk.Entry(self.content_frame, width=10)
        self.month_entry.pack(side='left')

        # Add a label and entry for selecting the year
        self.year_label = ttk.Label(
            self.content_frame, text="Enter the year (YYYY): ")
        self.year_label.pack(side='left', padx=(20, 10))
        self.year_entry = ttk.Entry(self.content_frame, width=10)
        self.year_entry.pack(side='left')

        # Add a separator for visual hierarchy
        self.separator2 = ttk.Separator(
            self.content_frame, orient='horizontal')
        self.separator2.pack(fill='x', pady=20)

        # Add radio buttons for selecting the type of graph
        self.graph_type_label = ttk.Label(
            self.content_frame, text="Select the type of graph: ")
        self.graph_type_label.pack()

        self.graph_type_var = tk.StringVar()
        self.graph_type_var.set("unique_titles")

        self.unique_titles_radio = ttk.Radiobutton(self.content_frame, text="Number of Unique Titles Watched Per Month",
                                                   variable=self.graph_type_var, value="unique_titles")
        self.unique_titles_radio.pack()

        self.most_viewed_radio = ttk.Radiobutton(self.content_frame, text="Top 5 Most Viewed Shows in a Month",
                                                 variable=self.graph_type_var, value="most_viewed")
        self.most_viewed_radio.pack()

        # Add a button for selecting the graph type
        self.select_button = ttk.Button(
            self.content_frame, text="Select", command=self.show_graph)
        self.select_button.pack()

    def show_graph(self):
        month = int(self.month_entry.get())
        year = int(self.year_entry.get())

        # Filter the data by the selected month and year
        df_filtered = df[(df['Date'].dt.month == month)
                         & (df['Date'].dt.year == year)]
        if len(df_filtered) == 0:
            self.error_label = ttk.Label(
                self.content_frame, text="No data available for the selected month and year.")
            self.error_label.pack(pady=20)
            return

        # Clear any previous error messages and graphs
        for widget in self.content_frame.winfo_children():
            if isinstance(widget, ttk.Label) and widget['foreground'] == 'red':
                widget.destroy()
            elif isinstance(widget, plt.FigureCanvasTkAgg):
                widget.get_tk_widget().destroy()

        # Get the selected graph type and show the corresponding graph
        graph_type = self.graph_type_var.get()

        if graph_type == "unique_titles":
            self.plot_unique_titles(df_filtered)
        elif graph_type == "most_viewed":
            self.plot_most_viewed(df_filtered)

    def plot_unique_titles(self, df_filtered):
        # Group the data by day and count the unique titles
        daily_unique_titles = df_filtered.groupby(
            df_filtered['Date'].dt.day)['Title'].nunique()

        # Plot a line graph
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.lineplot(data=daily_unique_titles, ax=ax)
        ax.set_xlabel('Day of Month')
        ax.set_ylabel('Number of Unique Titles')
        ax.set_title(
            'Number of Unique Titles Watched Per Day in Selected Month and Year')

        # Embed the graph in the UI
        canvas = FigureCanvasTkAgg(fig, master=self.content_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def plot_most_viewed(self, df_filtered):
        # Group the data by show and count the number of episodes watched
        show_episodes_watched = df_filtered.groupby(
            'Title')['Episode'].nunique().reset_index()
        show_episodes_watched.columns = ['Title', 'Episodes Watched']

        # Sort the data by number of episodes watched and select the top 5 shows
        most_viewed = show_episodes_watched.sort_values(
            'Episodes Watched', ascending=False).head(5)

        # Plot a pie chart
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.pie(most_viewed['Episodes Watched'],
               labels=most_viewed['Title'], autopct='%1.1f%%', startangle=90)
        ax.set_title('Top 5 Most Viewed Shows in Selected Month and Year')

        # Embed the graph in the UI
        canvas = FigureCanvasTkAgg(fig, master=self.content_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()


if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.mainloop()
