# Description
Welcome to my personal website project! This is a Django site that contains info about me and my resume.

# How to Run
1. Navigate to the top level directory
2. Create a virtual environment
3. Use the requirements.txt file to install all necessary packages and dependencies
4. Use "python3 manage.py runserver" to run the site on your local machine
5. Use the link provided to open the site in your browser

**Note**: The "contact" functionality requires AWS Simple Email Service and is configured for production use with my personal domain.

# What's Included
Below are a few of the files that I've added for this project specifically. This does not account for the standard files generated when creating a Django project.

1. **requirements.txt**: this file tracks all packages and software versions for my project and can be used to set up another virtual environment to correctly run the app.
2. **capstone/settings.py**: this is a standard Django settings file, with configuration for AWS Simple Email Service for the contact functionality.
3. **mysite folder**:
   1. **views.py**: contains the view functions for the site (index, login, logout, resume).
   2. **static folder**: contains visuals, javascript, and CSS files used across the site.
   3. **templates folder**: contains HTML templates for each page of the website.
   4. **models.py**: contains a model for resume entries (Job).

# Deployment
This site is deployed to AWS Elastic Beanstalk and uses CI/CD via GitHub Actions. Pushes to the `main` branch automatically trigger a deployment.
