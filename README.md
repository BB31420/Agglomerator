# Agglomerator

Agglomerator is a simple GUI application built with Python's Tkinter library for combining multiple video files into a single file.

![image](https://i.imgur.com/jz7hOE2.png)

## Installation
Agglomerator requires Python 3 and the following dependencies:

- tkinter
- customtkinter
- ffmpy
- packaging

### Clone the Repository
```
git clone git@github.com:BB31420/Agglomerator.git
```

```
cd Agglomerator/
```

### Virtual Environment
You should setup a virtual environment in the project's directory to prevent conflicts between packages. 
* Linux:
```
python3 -m venv .venv
```
then:
```
source .venv/bin/activate
```

You can install the dependencies using pip:
```
pip install -r requirements.txt
```

## Usage
To run Agglomerator, navigate to the directory where the Agglomerator.py file is located and run the following command:
```
python3 Agglomerator.py
```
The Agglomerator GUI will open. To add video files, click the "Add Video File" button and select one or more video files from the file dialog. The supported video file formats are: mp4, mkv, avi, webm, flv, mov, and wmv.

To remove a video file, select it in the list and click the "Remove Video File" button. To change the order of the video files, select a file and click the "Move Up" or "Move Down" buttons.

To combine the video files, click the "Combine Videos" button. You will be prompted to select a location to save the output file. The default output file format is mp4.

The video files will be concatenated in the order they appear in the list, and the output file will be created using the copy codec. After the video files have been combined, a success message will be displayed.

