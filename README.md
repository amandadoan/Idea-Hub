# Idea Hub - COMP 346 Final Project - Fall 2018

This is a web application for the final project of the Internet Computing course in Fall 2018. The website acts as a place for users to share their own ideas about any type of project such as open source projects, DIY, hobby, voluntary work, charity, etc..., and gather team members to work on the idea.

Team member: Duc Le, Julia Romare, Amanda Doan

## How to use the app

The application is pretty straight forward to use. In order to access the app, the user needs to create an account and login with that credential. There are 3 different main views that the user should pay attention: home page, user profile page, and project profile page.

### Home page

On the home page of this application, the user will see all projects that are currently in the database. User can click on the project name to go to the project profile page. If there are too many projects, the user can use the given filters to query all projects in their interested category. The search item on the navigation bar can also give user all projects that contain the input keywords.

### User profile page

Anywhere in the app, the user can click on their name on the left of the navigation bar to go to their profile page. This page contains all the posts from projects that the user is interested in (owner/member/subscriber). The posts are listed in the posted-time descending order, so the latest post will be display at the top. User can click on the respond button to respond to particular post. On the left column, there will be pending member requests for project that the user is the owner, and the user can choose to accept or decline the request.

### Project profile page

The project profile page is structured similarly to the user profile page. However, it only displays posts related to the one specific project. A normal user will see the option to ask to join, make post, or subscribe to this project, whereas the owner will have the option to delete the project, and members will have the option to leave. Based on the role, a normal user can make a post of type **Question** or  **Comment"**, whereas the member of a project can also post an **Update**.

### Navigation bar

The navigation bar allows user to navigate through the app with ease. There is a dropdown menu contains all the project the this user is a member/owner/subscriber. Projects that the current user is the owner/member will be display first. On the right, user will find a button let them create a new project or log out of the application.

## How to clone and run the app

This is a standard Django application, therefore, the cloning and running process is simple. We are using Python 3.6.5 for this development, any version higher than that should be fine.

Clone the project by the following command:

```{bash}
git clone https://github.com/nguyen-amanda/Idea-Hub.git
```

cd to the cloned folder in the Terminal, and run the following command to create a new virtual environment, activate it, as well as install required packages:

```{bash}
python3 -m ./venv
source venv/bin/activate
python -m pip install -r IdeaHub/requirements.txt
```

Now, you need to do the migration process for the app to create new database:

```{bash}
cd IdeaHub
python manage.py makemigrations
python manage.py migrate
```

Create the first super user so you can login and manage the app

```{bash}
python manage.py createsuperuser
```

Run the app and ENJOY:
```{bash}
python manage.py runserver
```

## TODOs:

The app still misses some features to be called perfect, such as easier editting and updating for projects, third party applications support, etc... We would love to open this project for anyone who is interested in working on it, so, please make pull requests as you wish.


