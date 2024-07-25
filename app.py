################################ IMPORT ####################################
############################################################################
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import zipfile
import os 
import dask.dataframe as dd
from pathlib import Path
import customtkinter as cutk
from tkinterdnd2 import DND_FILES , TkinterDnD 
from tkinter import messagebox, filedialog
from tkinter import *
import time
from threading import Thread

############################### FUNCTIONS ##################################
############################################################################

# function to unzip the file.zip
def unzipfile(file, extrat_to_folder):
    # create the destination folder
    os.makedirs(extrat_to_folder, exist_ok=True)

    try:
        with zipfile.ZipFile(file, 'r') as zip_ref:
            zip_ref.extractall(extrat_to_folder)
    except FileNotFoundError:
        print("error : file not found ")
    except zipfile.BadZipFile:
        print("error : can't unzip this file ") 
    except PermissionError: 
        print("error : can't access to the file ")
    except Exception as e: 
        print(f"an unexpected error {e}")

# function to handle dropping file in the entry 
# def on_file_drop(event):
#     file_path = event.data.strip('{}')
#     add_file_entry.configure(state='normal')
#     add_file_entry.delete(0, cutk.END)
#     add_file_entry.insert(0, file_path)
#     add_file_entry.configure(state='readonly')

# function to get columns 
def get_columns_and_filters(folder_path):
    column_set = set() # to store the columns
    values_dict = {} # to store the values 

    # get a list of CSV files in the folder
    files = list(Path(folder_path).glob('*.csv'))

    # check if there are no CSV files
    if not files: 
        messagebox.showerror("Error !", "No CSV files in the directory ")
        return column_set, values_dict

    # iterate for each CSV file
    for file in files:
        try:
            # read the CSV file into a dataframe
            df = pd.read_csv(file)

            # Iterate over columns in the dataframe
            for column in df.columns: 
                # Add column to the set of columns
                column_set.add(column)

                # Initialize the column in the dictionary if not already present
                if column not in values_dict:
                    values_dict[column] = set()

                # Add unique values from this column to the dictionary
                unique_values = df[column].dropna().unique() # drop NANS and get unique values 
                unique_values_set = set(unique_values)

                # Update the dictionary with the new unique values
                values_dict[column].update(unique_values_set)
        except Exception as e:
            messagebox.showerror("Error !", f"Error reading file {e}")
        
    values_dict = {col: list(vals) for col, vals in values_dict.items()}
    columns_list = list(column_set)

    return values_dict, columns_list

def next():
    main_frame.pack_forget()
    start_loading()
    file_path = add_file_entry.get()
    files_destination = files_destination_entry.get()
    # Unzip the file
    unzipfile(file_path, files_destination)
    directory_path = Path(files_destination)

    pdf_file_name = pdf_name_entry.get() + '.pdf'

    def update_second_combobox(*args):
        values2, columns = get_columns_and_filters(str(files_destination))
        selected_option = column_combobox.get()
        if selected_option in values2:
            filter_combobox.configure(values=values2[selected_option])
            filter_combobox.set(' ')

    # process function 
    def process_file():
        column_to_filter = column_combobox.get().replace(" ", "").lower()
        filter_element = filter_combobox.get()
        date_column = date_combobox.get().replace(" ", "").lower()

        filter_counts = {}
        all_date_counts = pd.Series(dtype='int')

        for file in directory_path.iterdir():
            if file.is_file() and file.suffix == '.csv':
                df = dd.read_csv(file)
                df.columns = df.columns.str.replace(" ", "").str.lower()

                if column_to_filter not in df.columns:
                    continue

                filtered_df = df[df[column_to_filter] == filter_element]

                if date_column not in df.columns:
                    continue

                date_counts = filtered_df[date_column].value_counts().compute()

                all_date_counts = all_date_counts.add(date_counts, fill_value=0)

                for date, count in date_counts.items():
                    if date not in filter_counts:
                        filter_counts[date] = 0
                    filter_counts[date] += count

        filter_counts = {k: v for k, v in filter_counts.items() if not pd.isna(k)}

        with PdfPages(pdf_file_name) as pdf:    
            fig, ax = plt.subplots(figsize=(20, 14
                                            ))

            ax.plot(all_date_counts.index, all_date_counts.values, marker='o')
            ax.set_xlabel('Date')
            ax.set_ylabel('Count')
            ax.set_title('Figure 1: Time Series Plot')
            ax.tick_params(axis='x', rotation=90)

            pdf.savefig(fig)
            plt.close()
            
            pdf_preview_label.configure(text=f"PDF preview : {pdf_file_name}")
            download_button.configure(state=cutk.NORMAL, command=lambda: download_pdfs([pdf_file_name]))

    def process():
        second_frame.pack_forget()      
        process_file()
        download_pdf_frame.pack(fill='both', expand=True)

    # Choose column label/comboBox
    column_label = cutk.CTkLabel(second_frame, text="Choose the column : ", font=font1)
    column_label.place(x=50, y=50)

    # Create a StringVar for the first combobox
    column_combobox_var = cutk.StringVar()

    # Create and place the first combobox
    values2, columns = get_columns_and_filters(str(files_destination))

    column_combobox = cutk.CTkComboBox(second_frame, width=400, values=columns, variable=column_combobox_var)
    column_combobox.set(" ")
    column_combobox.place(x=50, y=100)

    # Trace the variable to call update_second_combobox when the value changes
    column_combobox_var.trace_add('write', update_second_combobox)

    # Choose filter label/comboBox
    filter_label = cutk.CTkLabel(second_frame, text="Choose the filter : ", font=font1)
    filter_label.place(x=550, y=50)

    filter_combobox = cutk.CTkComboBox(second_frame, width=400, values=[" "])
    filter_combobox.set(" ")
    filter_combobox.place(x=550, y=100)

    # date label/comboBox
    date_label = cutk.CTkLabel(second_frame, text="Choose the column contain date : ", font=font1)
    date_label.place(x=50, y=200)
    date_combobox = cutk.CTkComboBox(second_frame, values=columns, width=400)
    date_combobox.set(" ")
    date_combobox.place(x=50, y=250)

    # process button
    process_button = cutk.CTkButton(second_frame, text="Process Files ⚙️", command=process, font=font1, text_color="white", height=50, fg_color=color2, bg_color=color1)
    process_button.place(x=805, y=500)

def download_pdfs(pdf_files):
    for pdf_file in pdf_files:
        destination = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")], initialfile=pdf_file)
        if destination:
            os.rename(pdf_file, destination)
            messagebox.showinfo("Success", f"PDF saved to {destination}")

def start_loading():
    loading_frame.pack(fill="both", expand=True)
    progress_bar.start()
    Thread(target=background_task).start()

def background_task():
    # Simulate a long-running task
    time.sleep(5)
    # Hide the loading frame when the task is done
    progress_bar.stop()
    loading_frame.pack_forget()
    second_frame.pack(fill='both', expand=True)

############################## APPLICATION #################################
############################################################################

# the application window
# app = TkinterDnD.Tk()
app = Tk()
app.geometry("1000x600") 
app.title("Analyzer")
app.resizable(False, False)
font1 = ('Arial', 20, 'bold')
font2 = ('Arial', 30, 'bold')
color1 = "#D6EFD8"  # light green   
color2 = "#1A5319"  # dark green 

# setting (appearance mode) and (color theme)
cutk.set_appearance_mode("light")
cutk.set_default_color_theme("green")

############################## FRAMES ###################################
############################################################################

# main frame
main_frame = cutk.CTkFrame(app, bg_color=color1, fg_color=color1)
main_frame.pack(fill="both", expand=True)

# Loading frame 
loading_frame = cutk.CTkFrame(app, bg_color=color1, fg_color=color1)

# second frame
second_frame = cutk.CTkFrame(app, bg_color=color1, fg_color=color1)

# download frame
download_pdf_frame = cutk.CTkFrame(app, bg_color=color1, fg_color=color1)

########################## WIDGETS ##########################################
#############################################################################

# title 
title = cutk.CTkLabel(main_frame, text="Analyzer ", font=font2, text_color=color2)
title.pack(pady=(50,50))

# (add file) entry and button
add_file_entry = cutk.CTkEntry(main_frame, placeholder_text="Drop Your Files Here or Click on the button to Add Files", width=600, height=50, font=font1)
add_file_entry.pack(pady=(20,20))

add_file_button = cutk.CTkButton(main_frame, text="Add Files ", font=font1, width=200, height=50, text_color="white", fg_color=color2, bg_color=color1, command=lambda: add_file_entry.configure(state='normal') or add_file_entry.delete(0, cutk.END) or add_file_entry.insert(0, filedialog.askopenfilename()) or add_file_entry.configure(state='readonly'))
add_file_button.pack(pady=(10,10))

# add_file_entry.drop_target_register(DND_FILES)
# add_file_entry.dnd_bind('<<Drop>>', on_file_drop)

# (file destination) entry
files_destination_label = cutk.CTkLabel(main_frame, text="Destination path : ", font=font1, text_color=color2)
files_destination_label.pack(pady=(20,5))

files_destination_entry = cutk.CTkEntry(main_frame, width=600, height=50, font=font1)
files_destination_entry.pack(pady=(0,20))

# (add pdf name) entry
pdf_name_label = cutk.CTkLabel(main_frame, text="PDF name : ", font=font1, text_color=color2)
pdf_name_label.pack(pady=(20,5))

pdf_name_entry = cutk.CTkEntry(main_frame, width=600, height=50, font=font1)
pdf_name_entry.pack(pady=(0,20))

# next button 
next_button = cutk.CTkButton(main_frame, text="Next ▶", font=font1, width=200, height=50, text_color="white", fg_color=color2, bg_color=color1, command=next)
next_button.pack(pady=(20,10))

# Loading frame widgets
progress_bar = cutk.CTkProgressBar(loading_frame, mode='indeterminate', width=400, height=30, fg_color=color2)
progress_bar.place(relx=0.5, rely=0.5, anchor='center')

# Download frame widgets
pdf_preview_label = cutk.CTkLabel(download_pdf_frame, text="PDF preview : ", font=font1)
pdf_preview_label.pack(pady=(20, 10))

download_button = cutk.CTkButton(download_pdf_frame, text="Download PDF", font=font1, text_color="white", height=50, fg_color=color2, bg_color=color1, state=cutk.DISABLED)
download_button.pack(pady=(20, 10))

# start the application 
app.mainloop()
