Grants Project

Website URLs:
--------------------------------------------------

https://techiefolk.com/recruitphd/public/

https://techiefolk.com/grantize/public/

https://techiefolk.com/sisterlab/public/


Database Credentials: 
--------------------------------------------------

database: getebhxz_sl_laravel
database user : getebhxz_sl
pwd: B%se,K]Y?,GY 



How to Setup: 
--------------------------------------------------

1. Download and Install Anaconda from and follow the instructions: https://docs.anaconda.com/free/anaconda/install/windows/
2. Download and Install Git From: https://git-scm.com/downloads. Add the corresponding Git path in the Systems variable (OPTIONAL).
3. Create the project directory at any location in your system. Move into that directory and open Git Bash there.
4. Execute the command to clone the Grant repository: git clone https://github.com/Neelansh01/Grant.git. Move into the Prjoect Git Folder.
5. As the Anaconda is installed, in the search bar, search: Anaconda Prompt and click to open the Anaconda shell. Move in to the directory of the Project it Folder using: cd <__path_to_the_project_git_directory__>
6. In the shell install the required libraries for this project using the command: pip install -r requirements.txt
7. Now import the file grant.sql in the phpMyAdmin setup (already present with XAMPP. If XAMPP is not available, install the XAMPP from insternet and start Apache and SQL servers). Note that the username is root and there is no password in the current database setup. We will update this later.
8. Now run this command in the Anaconda Shell to run or host the application: python app.py
