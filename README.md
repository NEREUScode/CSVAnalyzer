# CSVAnalyzer

CSVAnalyzer is a graphical user interface (GUI) application that processes CSV files, filters data based on user inputs, and generates a PDF report with a time series plot. It provides an intuitive and user-friendly way to analyze and visualize data. (make sure that the zip contains files not folders ,and the files are .csv)

## Features

- **Drag-and-Drop Functionality**: Easily add ZIP files containing CSV files by dragging and dropping or using a file selection dialog.
- **Dynamic Filtering**: Filter data based on user-selected columns and filter values.
- **Date Handling**: Generate time series plots using date columns from the CSV files.
- **PDF Report Generation**: Create and download detailed PDF reports with visualizations.
- **Modern Interface**: A clean and customizable GUI for an enhanced user experience.

## Installation

To set up CSVAnalyzer, follow these steps:

1. **Clone the Repository**

   ```sh
   git clone https://github.com/your-username/csvanalyzer.git
   cd csvanalyzer
2. **Install Dependencies**

   Ensure you have Python 3 installed. Install the required libraries with pip:
   ```sh
   pip install pandas matplotlib customtkinter tkinterdnd2 dask
3. **Run the Application**

   Start the application with the following command:
   ```sh
   python app.py
## Usage

1. **Launch the Application**

   Run the application using the command above. The main window will appear.

2. **Add Files**

   - **Drag and Drop**: Drag and drop your ZIP file containing CSV files into the "Drop Your Files Here" entry field.
   - **File Selection**: Click the "Add Files" button to open a file dialog and select your ZIP file.

3. **Configure Settings**

   - **Destination Path**: Enter the path where the ZIP file will be extracted.
   - **PDF Name**: Enter the desired name for the PDF report.

4. **Proceed to Filtering**

   Click the "Next" button to transition to the filtering and processing screen.

5. **Filter Data**

   - **Choose Column**: Select the column to filter from the dropdown menu.
   - **Filter Value**: Choose the filter value from the available options.
   - **Date Column**: Select the column containing date values.

6. **Generate Report**

   Click the "Process Files" button to generate the PDF report. The application will process the CSV files and create a time series plot.

7. **Download PDF**

   After processing is complete, the download button will be enabled.

   Click the "Download PDF" button to save the generated report to your preferred location.
 ## Functions

- **`unzipfile(file, extract_to_folder)`**  
  Unzips the provided ZIP file to the specified destination folder.

- **`on_file_drop(event)`**  
  Handles the event of dropping a file into the entry field.

- **`get_columns_and_filters(folder_path)`**  
  Retrieves columns and unique values from the CSV files in the specified folder.

- **`next()`**  
  Transitions to the next frame, processes the files, and generates the PDF report.

- **`download_pdfs(pdf_files)`**  
  Prompts the user to save the generated PDF files to a chosen location.

- **`start_loading()`**  
  Displays the loading frame and starts the progress bar.

- **`background_task()`**  
  Simulates a long-running task and hides the loading frame upon completion.
## Libraries and Frameworks Used

- **pandas**: For data manipulation and analysis.
- **dask**: For parallel computing and efficient handling of large datasets.
- **matplotlib**: For creating plots and visualizations.
- **customtkinter**: For a modern and customizable GUI.
- **tkinterdnd2**: For drag-and-drop functionality.
- **zipfile**: For extracting files from ZIP archives.
- **os, pathlib**: For file and directory operations.
- **threading**: For running background tasks.
## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contact

For questions or feedback, please contact the project maintainer:

- **Name**: Ben yamna Mohammed
- **Email**: medbenyamnacontact@gmail.com
- **GitHub**: NEREUScode

   
   




