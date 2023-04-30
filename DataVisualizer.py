import tkinter as tk
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Read data from CSV file
df = pd.read_csv('netflixViewingHistory.csv')

# Convert the 'Date' column to datetime format
df['Date'] = pd.to_datetime(df['Date'], format="mixed")

# Merge different episodes and seasons of the same title into one
df['Title'] = df['Title'].str.split(':', expand=True)[0]
df['Title'] = df['Title'].str.split('(', expand=True)[0]
df['Title'] = df['Title'].str.strip()

# Count the number of unique titles in the dataset
num_titles = len(df['Title'].unique())


class App:
    def __init__(self, master):
        self.master = master
        master.title("Netflix Viewing History Analysis")

        self.label = tk.Label(
            master, text="Select the type of graph/chart to display:")
        self.label.pack()

        self.var = tk.StringVar(value="1")

        self.radio_button_1 = tk.Radiobutton(
            master, text="Number of unique titles watched per month", variable=self.var, value="1")
        self.radio_button_1.pack()

        self.radio_button_2 = tk.Radiobutton(
            master, text="Pie chart of top 5 most viewed shows in a selected month and year", variable=self.var, value="2")
        self.radio_button_2.pack()

        self.select_button = tk.Button(
            master, text="Select", command=self.select)
        self.select_button.pack()

    def select(self):
        choice = int(self.var.get())

        if choice == 1:
            self.show_bar_chart()
        elif choice == 2:
            self.show_pie_chart()

    def show_bar_chart(self):
        # Get user input for the month and year to display
        self.top_label = tk.Label(self.master, text="Enter the month (1-12): ")
        self.top_label.pack()
        self.month_entry = tk.Entry(self.master)
        self.month_entry.pack()

        self.bottom_label = tk.Label(
            self.master, text="Enter the year (YYYY): ")
        self.bottom_label.pack()
        self.year_entry = tk.Entry(self.master)
        self.year_entry.pack()

        self.ok_button = tk.Button(
            self.master, text="OK", command=self.show_bar_chart_graph)
        self.ok_button.pack()

    def show_bar_chart_graph(self):
        month = int(self.month_entry.get())
        year = int(self.year_entry.get())

        # Filter the data by the selected month and year
        df_filtered = df[(df['Date'].dt.month == month)
                         & (df['Date'].dt.year == year)]
        if len(df_filtered) == 0:
            self.error_label = tk.Label(
                self.master, text="No data available for the selected month and year.")
            self.error_label.pack()
            return

        # Group the filtered data by title and count the number of unique titles in each group
        counts = df_filtered.groupby('Title')['Title'].count()

        # Create a bar plot of viewing counts
        sns.set_style("darkgrid")
        counts.sort_values(ascending=False)[:20].plot(kind='bar')
        plt.title('Top 20 Most Viewed Shows')
        plt.xlabel('Title')
        plt.ylabel('Number of Viewings')
        plt.show()

    def show_pie_chart(self):
        # Get user input for the month and year to display
        self.top_label = tk.Label(self.master, text="Enter the month (1-12): ")
        self.top_label.pack()
        self.month_entry = tk.Entry(self.master)
        self.month_entry.pack()

        self.bottom_label = tk.Label(
            self.master, text="Enter the year (YYYY): ")
        self.bottom_label.pack()
        self.year_entry = tk.Entry(self.master)
        self.year_entry.pack()

        self.ok_button = tk.Button(
            self.master, text="OK", command=self.show_pie_chart_graph)
        self.ok_button.pack()

    def show_pie_chart_graph(self):
        month = int(self.month_entry.get())
        year = int(self.year_entry.get())

        # Filter the data by the selected month and year
        df_filtered = df[(df['Date'].dt.month == month)
                         & (df['Date'].dt.year == year)]
        if len(df_filtered) == 0:
            self.error_label = tk.Label(
                self.master, text="No data available for the selected month and year.")
            self.error_label.pack()
            return

        # Count the number of viewings for each title
        counts = df_filtered['Title'].value_counts()

        # Create a pie chart of the top 5 most viewed shows
        sns.set_style("whitegrid")
        counts.sort_values(ascending=False)[:5].plot(kind='pie')
        plt.title('Top 5 Most Viewed Shows')
        plt.show()


root = tk.Tk()
app = App(root)
root.mainloop()
