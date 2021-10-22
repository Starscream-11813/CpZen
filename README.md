# CpZen
CpZen is an Online Integrated Development Environment (IDE) for competitive programmers made as the Lab project for CSE 4510: Software Development Lab.

![Build](https://img.shields.io/badge/build-passing-lightgreen.svg)
![Status](https://img.shields.io/badge/Status-Complete-brightgreen)
![License](https://img.shields.io/badge/license-MIT-orange.svg)
![Grade](https://img.shields.io/badge/Grade-Not%20Yet%20Graded-lightgrey)

## Built With:
### Frameworks and Dependencies: 
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white) 
![Bootstrap](https://img.shields.io/badge/bootstrap-%23563D7C.svg?style=for-the-badge&logo=bootstrap&logoColor=white) 
![jQuery](https://img.shields.io/badge/jquery-%230769AD.svg?style=for-the-badge&logo=jquery&logoColor=white)
![Jinja](https://img.shields.io/badge/Jinja-%230259B.svg?style=for-the-badge&logo=Jinja&logoColor=white)
![Beautiful Soup](https://img.shields.io/badge/Beautiful%20Soup-7957D5.svg?style=for-the-badge&logo=beautifulsoup&logoColor=white)
![HightlightJS](https://img.shields.io/badge/HighlightJS-F54A2A.svg?style=for-the-badge&logo=highlightjs&logoColor=white)
![ChartJS](https://img.shields.io/badge/Chart.JS-60B5CC.svg?style=for-the-badge&logo=chartdotjs&logoColor=white)
![Codemirror](https://img.shields.io/badge/Codemirror-%23FF0000.svg?style=for-the-badge&logo=codemirror&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)
![SQLite](https://img.shields.io/badge/sqlite-%23AC6E2F.svg?style=for-the-badge&logo=sqlite&logoColor=white)
### APIs:
* [JDoodle](https://www.jdoodle.com/compiler-api/)
* [CLIST](https://clist.by/api/v1/doc/)
* [Codeforces API](https://codeforces.com/apiHelp)
* [uHunt API](https://uhunt.onlinejudge.org/api)
* [Kenkoooo's API for AtCoder](https://github.com/kenkoooo/AtCoderProblems/blob/master/doc/api.md)
### IDE: 
![Visual Studio Code](https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white)
### Testing Tool: 
![Postman](https://img.shields.io/badge/Postman-FF6C37?style=for-the-badge&logo=postman&logoColor=white)
## Team Members:
* Syed Rifat Raiyan- 180041205
* Ishrak Hossain- 180041218
* Md. Maksudul Haque- 180041222

## Foreword:
The main goal of this application is to alleviate some of the tedious jobs a competitive programmer has to do on a regular basis by integrating them in a single place.

## Installation:
* Step-1: Make sure Python 3.7+ 64-bit is configured in your PC.
* Step-2: Open powershell, and install the required packages and dependencies by running: 
```shell
pip install -r requirements.txt
```
* Step-3: Run run.py with the command: 
```shell
python run.py
```
* Step-4: The application will be up and running on ```http://127.0.0.1:5000/```

## Features:
### Landing Page (pre-Login):
![Landing Page](featuresDemo/demo images/Landing page.PNG)

### Login/Signup:
Users can create a new account or login to an already existing account. If they forget their password, then a "Reset Password" link will be sent to their email.
![Login](featuresDemo/demo images/Login.PNG)
![Signup](featuresDemo/demo images/Signup.PNG)
![Reset Password](featuresDemo/demo images/resetpassword.PNG)

### Landing Page (post-Login):
Text editor area with Syntax Highlighting, Auto-Indentation, Auto-Brackets Matching, Auto-Brackets Highlighting and Line Highlighting. Supports a total of 20 programming languages.\
![C](https://img.shields.io/badge/c-%2300599C.svg?style=for-the-badge&logo=c&logoColor=white)
![C++](https://img.shields.io/badge/c++-%2300599C.svg?style=for-the-badge&logo=c%2B%2B&logoColor=white)
![C#](https://img.shields.io/badge/c%23-%23239120.svg?style=for-the-badge&logo=c-sharp&logoColor=white)
![Clojure](https://img.shields.io/badge/Clojure-%23Clojure.svg?style=for-the-badge&logo=Clojure&logoColor=Clojure)
![Dart](https://img.shields.io/badge/dart-%230175C2.svg?style=for-the-badge&logo=dart&logoColor=white)
![Go](https://img.shields.io/badge/go-%2300ADD8.svg?style=for-the-badge&logo=go&logoColor=white)
![Haskell](https://img.shields.io/badge/Haskell-5e5086?style=for-the-badge&logo=haskell&logoColor=white)
![Java](https://img.shields.io/badge/java-%23ED8B00.svg?style=for-the-badge&logo=java&logoColor=white)
![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)
![Kotlin](https://img.shields.io/badge/kotlin-%230095D5.svg?style=for-the-badge&logo=kotlin&logoColor=white)
![Lua](https://img.shields.io/badge/lua-%232C2D72.svg?style=for-the-badge&logo=lua&logoColor=white)
![PHP](https://img.shields.io/badge/php-%23777BB4.svg?style=for-the-badge&logo=php&logoColor=white)
![Perl](https://img.shields.io/badge/perl-%2339457E.svg?style=for-the-badge&logo=perl&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Ruby](https://img.shields.io/badge/ruby-%23CC342D.svg?style=for-the-badge&logo=ruby&logoColor=white)
![Rust](https://img.shields.io/badge/rust-%23000000.svg?style=for-the-badge&logo=rust&logoColor=white)
![Scala](https://img.shields.io/badge/scala-%23DC322F.svg?style=for-the-badge&logo=scala&logoColor=white)
![Shell Script](https://img.shields.io/badge/shell_script-%23121011.svg?style=for-the-badge&logo=gnu-bash&logoColor=white)
![Brainf**k](https://img.shields.io/badge/brain%20f**k-%13131011.svg?style=for-the-badge&logo=brainfuck&logoColor=white)
![Objective-C](https://img.shields.io/badge/objective%20C-256513.svg?style=for-the-badge&logo=brainfuck&logoColor=white)
\
![IDE](featuresDemo/demo images/IDE.PNG)
![Languages](featuresDemo/demo images/languageslist.png)

### Compile/Run Code:
Users can click on Compile(Alt+C) to compile their code and on Run(Alt+R) to run their code. The source code, Standard Input and Standard Output (along with Build Log, Time taken and Memory usage) will be shown.
![Run](featuresDemo/demo images/runSourceCode.PNG)
![StdIO](featuresDemo/demo images/StdIO.PNG)

### Save Codes:
Users can save their code by clicking on Save(Alt+S) after providing a name for the file. They can click on "Copy" to copy the contents to clipboard or on "Download" to download the file to the local machine.
![SaveName](featuresDemo/demo images/savecode1.PNG)
![SaveCodes](featuresDemo/demo images/savecode2.PNG)

### Save Templates:
Ditto.
![SaveTemplates](featuresDemo/demo images/savetemplates.PNG)

### Upcoming Contests:
Users can view a list of upcoming contests on 12 of the most popular online judges. The contests are categorized based on topics and difficulty levels and each list consists of the Contest Title, Contest Link, Start Time, End Time and Duration.
![Upcoming1](featuresDemo/demo images/upcoming1.PNG)
![Upcoming2](featuresDemo/demo images/upcoming2.PNG)
![Upcoming3](featuresDemo/demo images/upcoming3.PNG)
![Upcoming4](featuresDemo/demo images/upcoming4.PNG)
![Upcoming5](featuresDemo/demo images/upcoming5.PNG)
![Upcoming6](featuresDemo/demo images/upcoming6.PNG)

### Profile Statistics:
Users can view profile stats from 5 of the most popular online judges after selecting one of them and providing a judge handle/username. Stats include Contest Rating Line-graph, Submission Verdicts Doughnut-graph, Submission Activity Heatmap/Matrix-chart and list of Unsolved problems for up-solving.
![ProfileStatistics1](featuresDemo/demo images/profilestats1.PNG)
![ProfileStatistics2](featuresDemo/demo images/profilestats2.PNG)
![ProfileStatistics3](featuresDemo/demo images/profilestats3.PNG)
![ProfileStatistics4](featuresDemo/demo images/profilestats4.PNG)
![ProfileStatistics5](featuresDemo/demo images/profilestats5.PNG)

### Algorithms:
Users can keep track of the algorithms they learn throughout their competitive programming journey by saving any good resources/problems pertaining to an algorithm they can find along with their subjective proficiency in the algorithm. They can choose to update any entry if they come across any new resource/problem or if they feel their proficiency in the algorithm has improved. They can also delete any algorithm entry. Users can have a slght idea about the algorithmic topics they have/don't have a grasp over by viewing the Proficiency Radar-chart and practise accordingly.
![Algorithms1](featuresDemo/demo images/algorithms1.PNG)
![Algorithms2](featuresDemo/demo images/algorithms2.PNG)
![Algorithms3](featuresDemo/demo images/algorithms3.PNG)
![Algorithms4](featuresDemo/demo images/algorithms4.PNG)
![Algorithms5](featuresDemo/demo images/algorithms5.PNG)
![Algorithms6](featuresDemo/demo images/algorithms6.PNG)

## Resources:
### Tutorials:
* [Chart.js Tutorial](https://www.youtube.com/watch?v=NySBh_DIRlg)
* [Highlight.js Tutorial](https://www.youtube.com/watch?v=y-0jqM9EeVM)
* [Flask Tutorial](https://www.youtube.com/watch?v=dam0GPOAvVI)

### Inspirations:
We were inspired by similar projects like:
* [StopStalk](https://www.stopstalk.com/)
* [Codeforces Visualizer](https://cfviz.netlify.app/)
* [clist.by](https://clist.by/)
* [OnlineGDB IDE](https://www.onlinegdb.com/)


![test](featuresDemo/demo images/algorithms1.PNG)
