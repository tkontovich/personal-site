# Description
Welcome to my personal website project! This is a Django site that contains info about me, my resume, and a "2024 goals" section that allows me to keep track of my progress towards some of the goals I set for myself for the year.

<!-- CI/CD test update -->


# Distinctiveness and Complexity
I believe my site's use of a **web scraper**, **garminconnect package (to connect to Garmin's API)**, and Django's **caching functionality** satisfy the distinctiveness and complexity requirements of this project. I knew I wanted to be able to track my three goal categories (running, reading, and climbing), and since I already track each of those via separate websites (8a.nu for climbing, goodreads for reading, garmin for running), I knew I wanted to pull that information in to this rather than have to duplicate entries anywhere.

The **web scraper** was the first new technology I had to learn for this project. I could not find where 8a.nu or Goodreads offer APIs, so instead started looking into a web scraper to gather the data I needed instead. This involved looking through the flow of each site to get the relevant information loaded (including having to log in to 8a.nu), and then feeding the scraper commands to navigate through that flow. LOTS of trial and error, especially figuring out how much of a delay to build in at times to allow the websites to load the elements I was trying to find.

The **garminconnect package** was slightly more straightforward to implement than the scraper (and a bit cleaner), but still took a decent amount of trial and error to get the package installed and functioning correctly. There is fairly minimal documentation outside of the github files, but trial and error also got this one working. Once it was actually working correctly, using the documentation to pull the right information was relatively quick.

Once I had the web scraper and garminconnect package working, I encountered a couple of issues. Firstly, the goals page would take several seconds to load to account for the scraper delays that were required. Additionally, each time the goals page was loaded I would be calling the Garmin API again. As you can imagine when testing minor CSS changes and reloading quickly in succession, I angered Garmin several times where they blocked my connection for several hours. To help with both of these issues, I figured out how to use Django's **caching functionality**. The first time the goals page loads now it still takes several seconds, but after this first load the page is cached, and subsequent visits (for the next several hours at least) will load immediately.

# How to Run
1. Navigate to the top level "Capstone" folder
2. Create a virtual environment
3. Use the requirements.txt file to install all necessary packages and dependencies
4. Use "python3 manage.py runserver" to run the site on your local machine
5. Use the link provided to open the site in your browser

***Notes***: there are a couple of caveats to call out:
1. **When loading the "goals" site for the first time, it will take several seconds to load.** I've built in some delays to the functions using the web scraper, as when testing I found that the sites being tested needed small amounts of time for certain elements to load and be found by the scraper. I've gone through and reduced the delays as much as possible, but there is still a delay. To help with this, I've utilized Django's caching functionality to capture the page when it's loaded the first time, so subsequent visits to the goals page load immediately.
2. **The "contact" functionality will not work on a local machine and has thus been hidden.** The AWS simple email service I'm using is hooked up to my personal domain, so won't correctly send emails when it gets the request from a local machine. I've commented out the contact section of my html, but left everything in so you can see the code (this is what I'm using javascript for).


# What's Included
Below are a few of the files that I've added for this project specifically. This does not account for the standard files generated when creating a Django project.
1. **requirements.txt**: this file tracks all packages and software versions for my project and can be used to set up another virtual environment to correctly run the app.
2. **chromedriver**: my app utilizes a webscraper, so there are some files like this one that are created when setting up Chrome and the driver for the webscraper to use.
3. **setting.py**: this is a standard file, but it's worth calling out that there were some lines added to connect the "contact me" functionality to AWS simple email service which will be used when this site is hosted on my personal domain.
4. **mysite folder**:
    1. **view.py**: this contains all my functions. A larger functions to few to callout:
        1. **contact**: the function that sends email and is called from the javascript that runs when the "send" button is clicked.
        2. **goals2024**: this function calls a few other functions to gather and consolidate all data needed to populate the goals page of the site.
        3. **scraperoptions**: this sets up required options for the scraper to function.
        4. **climbing**: this functions scrapes a website that I use to log and track rock climbing ascents and calculates progress towards goal.
        5. **running**: this function uses a package called "garminconnect" to connect to Garmin's API and calculate progress towards goal.
        6. **reading**:  this function scrapes Goodreads to get all of the books I've read this year and calculate progress towards goal.
    2. **static folder**: this folder contains a few visuals used across the site, my javascript file, and css file.
    3. **templates folder**: this folder contains a handful of html templates that are used for each page of my website.
    4. **models.py**: this contains a model for resume entries.


# What's Next?
**Run this site on my personal domain:** my next big step is to get this site running on an EC2 instance and have my personal domain (trentkontovich.com) point there. This has been challenging, particularly getting the web scraper to function correctly, but is the next priority I'm working on! This will also enable the contact functionality so people can send me an email if they want to get in touch.

**Figure out how to get the site to load and cache the goals page asynchronously**. Caching helped with multiple loads of the goals page, but it still takes several seconds the first time it's loaded. Once I have this on an EC2 instance, I'd like to have it load and cache the goals site everynow and then, so when an actual user visits the page it almost always loads a cached version immediately.