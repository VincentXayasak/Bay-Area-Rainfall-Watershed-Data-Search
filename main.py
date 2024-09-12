import tkinter as tk
from tkinter import ttk, messagebox
from search import Search

class WatershedApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Watershed Precipitation Data")
        self.geometry("600x400")
        
        try:
            self.search = Search()
        except requests.exceptions.HTTPError:
            messagebox.showerror("Error", "Status Unavailable Right Now.")
            self.destroy()
            return
        
        self.create_widgets()

    def create_widgets(self):
        # Dropdown for selecting a watershed
        self.watershed_label = ttk.Label(self, text="Select a Watershed:")
        self.watershed_label.pack(pady=10)

        self.wsList = list(self.search.getWatersheds())
        self.watershed_var = tk.StringVar()
        self.watershed_dropdown = ttk.Combobox(self, textvariable=self.watershed_var, values=self.wsList)
        self.watershed_dropdown.pack()

        # Dropdown for selecting a time range
        self.range_label = ttk.Label(self, text="Select a Time Range:")
        self.range_label.pack(pady=10)

        self.range_options = {
            "1 Hour Ago": 1,
            "3 Hours Ago": 2,
            "6 Hours Ago": 3,
            "12 Hours Ago": 4,
            "24 Hours Ago": 5,
            "Year To Date": 6
        }
        self.range_var = tk.StringVar()
        self.range_dropdown = ttk.Combobox(self, textvariable=self.range_var, values=list(self.range_options.keys()))
        self.range_dropdown.pack()

        # Buttons for different actions
        self.precipitation_button = ttk.Button(self, text="Show Precipitation", command=self.displayWatershedPrecipitation)
        self.precipitation_button.pack(pady=10)

        self.data_button = ttk.Button(self, text="Show Full Data", command=self.displayWatershedData)
        self.data_button.pack(pady=10)

        self.ranked_ws_button = ttk.Button(self, text="Rank Watersheds", command=self.displayRankedWatersheds)
        self.ranked_ws_button.pack(pady=10)

        self.ranked_sensors_button = ttk.Button(self, text="Rank Sensors", command=self.displayRankedSensors)
        self.ranked_sensors_button.pack(pady=10)

        self.quit_button = ttk.Button(self, text="Quit", command=self.quit)
        self.quit_button.pack(pady=10)

    def displayWatershedPrecipitation(self):
        ws = self.watershed_var.get()
        range_name = self.range_var.get()
        
        if ws and range_name:
            range_val = self.range_options[range_name]
            precipitation = self.search.getWatershedPrecipitation(ws, range_val)
            messagebox.showinfo("Precipitation", f"{ws} has had a total precipitation of {precipitation} inches from {range_name}.")
        else:
            messagebox.showerror("Input Error", "Please select both a watershed and a time range.")

    def displayWatershedData(self):
        ws = self.watershed_var.get()
        
        if ws:
            data = self.search.getWatershedData(ws)
            data_string = "\n".join([f"{sensor}: {dataList}" for sensor, dataList in data.items()])
            messagebox.showinfo(f"{ws} Data", data_string)
        else:
            messagebox.showerror("Input Error", "Please select a watershed.")

    def displayRankedWatersheds(self):
        range_name = self.range_var.get()
        
        if range_name:
            range_val = self.range_options[range_name]
            ranked_ws = self.search.rankPrecipitation(range_val)
            rank_string = "\n".join([f"{count + 1}. {ws}: {precipitation}" for count, (ws, precipitation) in enumerate(ranked_ws.items())])
            messagebox.showinfo(f"Ranked Watersheds ({range_name})", rank_string)
        else:
            messagebox.showerror("Input Error", "Please select a time range.")

    def displayRankedSensors(self):
        range_name = self.range_var.get()
        
        if range_name:
            range_val = self.range_options[range_name]
            ranked_sensors = self.search.rankSensors(range_val)
            rank_string = "\n".join([f"{count + 1}. {sensor}: {precipitation}" for count, (sensor, precipitation) in enumerate(ranked_sensors)])
            messagebox.showinfo(f"Ranked Sensors ({range_name})", rank_string)
        else:
            messagebox.showerror("Input Error", "Please select a time range.")

if __name__ == "__main__":
    app = WatershedApp()
    app.mainloop()
