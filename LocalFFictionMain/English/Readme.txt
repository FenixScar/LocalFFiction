>>> LocalFFiction - Web interface for your Fimfiction archive <<<
>> Created with DeepSeek and published by FenixScar <<




*** INFORMATION ***


Programming languages: Python and Batch
External libraries: TQDM, Streamlit, Pandas
Supported OS: Windows
Interface languages: English and Russian
Version: 1.0
Developer: FenixScar [Code written by DeepSeek]
License: Public domain. Modify and reupload as you wish and where you wish. But if you credit me as the author, I'll be happy :)

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT ANY WARRANTIES. THE DEVELOPER IS NOT RESPONSIBLE FOR ANYTHING.


*** DESCRIPTION ***


This program is designed for convenient navigation of your local copy of Fimarchive with an intuitive web interface, remotely similar to the original site. It will be very useful if you will not have access to the Internet in the near future or if you are simply paranoid and prefer a local archive to the Internet. The program consists of several Python scripts and several .bat files that run them. The program was 99% written by the DeepSeek AI in 3 days, so I myself hardly understand most of what it consists of. For this reason, there may be bugs and flaws in the program. If you know what you're doing, you can fix or change anything you want. The program is 120% OpenSource.

Fimfiction archive: https://www.fimfiction.net/user/116950/Fimfarchive
Fimfiction itself: https://www.fimfiction.net/


*** COMPLETE GUIDE TO INSTALLING, CONFIGURING, AND USING LocalFFiction ***


1. Place the LocalFFictionMain folder anywhere on your disk. 
   1.1. It is strongly recommended to use an SSD if you have one. This will significantly speed up the program.

2. Install the latest version of Python from the official website “https://www.python.org/downloads/”, following the internal instructions during installation. Be sure to click “Add python.exe to PATH” at the bottom of the window.
   2.1. If you are not sure whether it is installed or not, press the Win + R keys, type “cmd” and enter “python” in the window that opens. If the console responds with “Python...”, everything is fine, it is already installed.
   2.2. If you already have Python installed, check which version you have. The program is guaranteed to work on 3.10.6. If your version is too old compared to this one, it is better to update it through the official website.
        2.2.1. DeepSeek believes that Python 3.6 and below will most likely not work. Versions 3.7 and above should work correctly.

3. Additional libraries are required for the program to work. Restart CMD and, without entering “python”, enter the command “pip install tqdm streamlit pandas”. This will install all the necessary libraries.
   3.1. If the download freezes, restart CMD again and re-enter the above command.

4. Place index.json from your Fimfiction archive in the Converter folder.
   4.1. If you do not have index.json, download the latest version of Fimarchive here: “https://www.fimfiction.net/user/116950/Fimfarchive”.
   4.2. If you already have a .csv file, you can try skipping the conversion section and uploading it directly to LocalFFiction, but I cannot guarantee that it will work correctly.

5. Run JSON-to-CSV Converter.bat. The program will do everything automatically.

6. After conversion, check fimfiction_result_errors.log. If there are only 2 lines there, everything went well. You can delete this file.
   6.1. If there are more lines in this file, the conversion failed. Try again. If that doesn't help, download index.json again. 
        6.1.1. You can also continue with the following steps, ignoring the errors, if everything looks fine in LocalFFiction — it may be a minor bug.

7. Move the fimfiction_result.csv file to the LocalFFiction folder.

8. Run LocalFFiction.bat.
   8.1. Please note that the converter could also be launched using a .py file, but here .bat launches the .py script directly from the library, which is necessary for it to work properly.

9. At this stage, a tab with the address “http://localhost:8501/” should have opened in your browser. This is a local address that is not connected to the Internet and works directly with local files on your PC.
   9.1. If, during startup, you are asked to enter an email address for the streamlit library mailing list in the console window, you can simply leave the field blank and press Enter. This request will not appear again.
   9.2  If a Firewall window appears during startup asking for permission to use the network for Python, click “Allow access”. It is unlikely to affect anything, but it is better to be safe than sorry.
   9.3. If the tab does not open after that, enter the above address manually in the address bar of your preferred browser.
   9.4. IMPORTANT! Do not close the console window that opened. Nothing will work without it! Just minimize it to the taskbar.

10. In the LocalFFiction tab in the left pane, click Browse files, then find the fimfiction_result.csv file on your disk and select it.
   10.1. If it is more convenient for you, you can simply drag this file from the folder directly into the window with "Browse files" button. This will also work.

11. Now the file is loaded. In the left pane, there is a search, filter, and sort window. On the right side, there is a list of stories with tags, descriptions, etc. The interface is intuitive, so I think you'll figure it out.
    11.1. To close the program, simply close the tab and the console window. To start it again, open LocalFFiction.bat again and follow the steps starting from 8.

12. Done. Enjoy :)


*** END OF GUIDE ***



June 2025.