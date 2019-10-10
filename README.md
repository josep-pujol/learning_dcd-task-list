
# Work Force Management (Part 1)

[![Build Status](https://travis-ci.com/josep-pujol/learning_dcd-workforce-management.svg?token=mpvYNnPLPqbCpUvpUExD&branch=master)](https://travis-ci.com/josep-pujol/learning_dcd-workforce-management)

This repo contains a solution code for the milestone project of the *Data Centric Development* module at Code Institute.

Consists on a "Tasks List" application in which users can store and manage tasks. This is the first part of a bigger project which will use this app for multiple users, groups of users etc. that will be the final project at Code Institute.

A demo of the app can be viewed [HERE](https://dcd-workforce-management.herokuapp.com/)




## UX

The app will consist on three main pages: 

- Main page to display all Tasks to be done

    ![Main page or Tasks page](https://github.com/josep-pujol/learning_dcd-workforce-management/blob/master/wireframes/tasks_mockup.png)

- Pages to add and edit a single Task

    ![Add Task](https://github.com/josep-pujol/learning_dcd-workforce-management/blob/master/wireframes/add_task_mockup.png)

- Page to display completed Tasks

    ![Completed Tasks](https://github.com/josep-pujol/learning_dcd-workforce-management/blob/master/wireframes/completed_tasks_mockup.png)


Additionally some modals/popup windows are used to perform actions like:
- Edit the Status of a Task
- Add an Issue or Alert sign on the Task
- Update any of the fields of the Task

These actions can be activated by clicking on the menu-dots item on the right hand side of each Task.




## Features

### Existing Features

- Main Page
    - Navigation links on top
    - Display tasks that are not completed
    - Pagination, including dropdown menu to select number of rows per page
    - Search and Sorting functionality for all fields in the Table
    - Fixed floating button with tooltip, to add tasks
    - Menu-dots per Task which opens a window to:
        - Edit the Status of a Task
        - Edit any of the fields of a Task
        - Add or Remove the "Issues" sign

- Completed Tasks Page
    - Navigation links on top
    - Display tasks that are not completed
    - Pagination, including dropdown menu to select number of rows per page
    - Search and Sorting functionality for all fields in the Table
    
- Add and Edit Task Pages
    - Navigation links on top
    - Button to Cancel and go back to the Main Page
    - Button to Add and Store the Task
    - Insert the "Task Name" field; with validation
    - Select a "Task Category" from the dropdown menu or leave default option
    - Select a "Task Status" from the dropdown menu or leave default option
    - Add a text description
    - Select the "Due Date" of the Task from a Calendar popup window; with validation
    - Select the "Task Importance" from the dropdown menu or leave default option 



### Features Left to Implement
In the future, and as part of the final project of the course, user authentication, groups and premium functionality will be added.




## Technologies Used

### The main technologies used are:

- [Python](https://www.python.org/)
    - Base language used for the application
- [Flask](https://palletsprojects.com/p/flask/)
    - Lightweight WSGI web application framework for **Python**
- **HTML**, **CSS** and **Javascript**
    - Base languages used to create the site templates
- [Materialize](https://materializecss.com)
    - Used **Materialize 1.0.0** for a responsive layout and styling
- [DataTables](https://datatables.net)
    - Plugin for **jQuery** that adds interactive features to data stored in **HTML** tables
- [JQuery](https://jquery.com)
    - **JQuery** as a dependency for **DataTables**
- [Github](https://github.com)
    - Used as repository of the project 
- [Heroku](https://heroku.com)
    - To deploy the project
- [Travis](https://travis-ci.org/)
    - Continuous integration and testing




## Testing
- Python Unit tests with over 90% coverage, including:
    - Page rendering
    - CRUD operations
   
- All code used on this site has been manually tested to ensure everything is working as expected. Some tests include:
    - Site responsiveness from small mobile up to 17" desktop screens
    - Content is displayed correctly for screens of small mobiles to 17" desktop screens
    - Functionality:
        - Loading all pages
        - Links and buttons are working
        - Popup windows and its contents are opening correctly
        - Popup windows are performing the intended actions
        - Datatables functionality like Search, Sort, Pagination and Table wrapping is working correctly
    - Data entry and editing
        - Added several tasks using major browsers
        - Added tasks with empty fields for validation
        - Added tasks with empty fields to test default values
- Site viewed and tested in the following browsers:
  - Google Chrome
  - Microsoft Edge
  - Mozilla Firefox




## Deployment
 
### Getting the code up and running
0. The following instructions are meant for a Linux System running Python3
1. First it is recommended to create a virtual environment for the application
2. Download or clone this repository by running the ```git clone <project's Github URL>``` command
3. Create your own repository
4. Install Python packages from ```requirements.txt``` file. From Terminal type ```pip install -r requirements.txt```
5. Install the MongoDB client. From Terminal type ```wget -q https://git.io/fh7vV -O /tmp/setupmongodb.sh && source /tmp/setupmongodb.sh```
6. Create a MongoDB Atlas account, get the URI connection string to connect to Mongo Shell and test the connection
7. Add the connection string as enviroment variable in file ```.bashrc``` with the name ```MONGO_URI```
8. Create the following Collections in the MongoDB Atlas
    - ```task_category``` with a single field name ```category```. 
        - Add any categoy names you like plus the default value ```Undefined```
    - ```task_importance``` with two fields named ```importance``` and ```order```. 
        - Add any levels of task importance you like with their associated order 
        - Make sure you add the default value ```Low``` with order ```1```, which will be the lowest level of importance
    - ```task_status``` with two fields named ```status``` and ```order```. 
        - Add any status you like plus their associated order
        - Make sure you add the default values ```Not started``` with order ```0```, and ```Completed``` which show have the highest order
    - ```tasks``` collection just need to be created, and then populated through the application
9. To ensure all is working properly, run the Unit tests from Terminal, type ```python3 -m unittest discover```



### Deploy in Heroku
0. If previous steps ran successfully, to deploy the app in Heroku do the following
1. Create an account in heroku
2. Create an app
3. In the Settings section of the app set the following environmental variables:
    - ```IP``` set to ```0.0.0.0```
    - ```PORT``` set to ```5000```
    - ```MONGO_URI``` set to the value from previous section
4. Install Heroku in your system. From Terminal type ```sudo snap install --classic heroku```
4. Back in the Heroku website go to the Deploy section and connect your repository with Heroku
5. Select the option "Manual Deploy"
6. Load the url to test the application is up and running. Notice that there won't be any tasks.
7. If issues, please have a look at the deployment logs in Heroku




## Credits
Inspired by the [Materialize](https://materializecss.com) admin dashboards built by [Pixinvent.com](https://pixinvent.com/materialize-material-design-admin-template/html/ltr/vertical-modern-menu-template/)


