# HOW MUCH TIME?
#### Video Demo:  <(https://youtu.be/nX9xEF3N9Fg)>
#### Description:
HowMuchTime is a desktop application developed in Python with the main purpose of tracking how much time I spend using different applications on my computer. The idea of the project started from something quite simple: sometimes I use the computer for many hours, with the social media apps and their infinite scroll, I have taken seriously the time management in those apps. When thinking about a idea for the final project, It occurred to me to do something based on that.

The application runs in the background and checks which application is currently active on the computer. It uses Windows information to detect the active window and identify the process that is running. When I change from one application to another, the previous session is finished and a new one starts. For example, if I am using Visual Studio Code for ten minutes and then I open a browser, the program saves the Code session and starts tracking the browser.

Each session contains different information, like the application name, the start time, the end time, the duration and the date. This information is saved in a SQLite database called usage.db. I decided to use SQLite because it is simple to use and it does not require having a separate database server. Everything is stored locally on the computer, which also makes the application easier to use.

One of the important parts of the project is that the information is not only displayed while the tracker is running. The data is saved so I can close the program and check it later. This makes the application more useful because I can collect information during the day and then analyse it when I have more time.

The project also has a graphical interface made with Tkinter. I wanted the interface to be simple but also look modern enough, instead of having only a terminal with text. The main window contains a sidebar where the user can select different periods of time. There are options for Today, This Week and This Month.

The Today section shows the information from the current day. It includes the total amount of time tracked, the number of sessions and the application that has been used the most. Below this information there is a list called Time by Application, where the applications are ordered according to the amount of time they have been used. Each application also has a percentage and a progress bar, which makes it easier to compare them visually.

For the weekly and monthly sections, the application can show a usage overview with a graph. The graph represents the amount of time used on each day, so it is possible to see if there are days where the computer was used much more than others. At the moment, this part is still quite basic, but the idea is to improve the reports in the future.

Another part of the interface is the tracking status. It shows if the tracker is currently active or inactive. This is useful because the graphical interface and the tracker are separate parts of the project. The tracker can run in the background while the user uses the computer normally, and the GUI can be opened later to check the collected information.

During the development of HowMuchTime I have also had to solve some problems related to detecting the active application on Windows. Some Windows processes, like explorer.exe, should not be counted because they are part of the system and are not really applications that the user is working with. Because of this, the tracker ignores some system processes.

The project is divided into different Python files to keep the code more organized. The tracker is responsible for detecting applications and creating sessions, while the database file manages the SQLite database and the queries. The GUI is responsible for displaying the information to the user. This separation makes it easier to modify one part without breaking all the other parts.

The main technologies used in the project are Python, Tkinter, SQLite, psutil and pywin32. Python is used for the main logic, Tkinter for the graphical interface and SQLite for storing the data. psutil helps to obtain information about running processes, while pywin32 is used to interact with Windows and detect the currently active window. Also I used help of ChatGPT with the Tkinter library, because I didn't have any idea of how a windows interface is created.

The main objective of HowMuchTime is not to create a very complicated application, but to build something useful while learning how different parts of software development work together. It combines a database, background tracking, Windows processes and a graphical interface in the same project.

In the future, I would like to add more features to the application. For example, I could add better reports, more detailed statistics, filters for applications and maybe a way to see the usage history for previous weeks or months. I could also improve the graphs and make the interface more customizable.

For now, HowMuchTime is a functional first version of the idea. It can track application usage, save the sessions in a database and display the collected information in a graphical interface. The project is still not completely finished, but it already has the main functionality that I wanted when I started developing it.