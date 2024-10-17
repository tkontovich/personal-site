from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.core.mail import send_mail

from .models import Job

from datetime import datetime, date, timedelta

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from getpass import getpass

from email.message import EmailMessage

import time
import garminconnect
import os
import json
import smtplib


### Set up global variables 
start = date(2024, 1, 1)
end = date(2024, 12, 31)
today = date.today()

# from .models import modelsgohere


# Create your views here.

def index(request):
    return render(request, "mysite/index.html")
    

@csrf_exempt
def contact(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        receiverEmail = settings.NOTIFY_EMAIL

        senderEmail = data.get('email')
        senderName = data.get('name')
        senderMessage = data.get('message')

        send_mail(
            subject=f"Hello from {senderName}!", 
            message = senderMessage, 
            from_email = senderEmail, 
            recipient_list=[receiverEmail]
        )

        print("Email sent successfully.")

        return JsonResponse({"message": "Success."}, status=201)


def login(request):
    return render(request, "mysite/login.html")


def logout(request):
    return render(request, "mysite/index.html")


def resume(request):
    jobs = Job.objects.all()

    return render(request, "mysite/resume.html", {
        "jobs": jobs
    })


def goals2024(request):
    ##################################
    ### Make fake data for testing ###
    ##################################

    """ fake_running_results = {  
        "running_goal": 365, 
        "running_expected_progress": 266, 
        "running_progress_percentage": 60, 
        "running_status": "bg-warning",
        "running_current_miles": 260,
        "running_current_runs": 70,
        "running_current_avg_distance": 3.5, 
        "running_current_avg_pace": timedelta(seconds=10000), 
        "running_current_total_calories": 30000 
    }

    fake_climbing_list = [
        {
            "date": "Sep 20 2024", 
            "route": "Groovin' in the woods", 
            "grade": "5.13b", 
            "location": "Equinox"
        }
    ]

    fake_climbing_results = {
        "climbed_8a": True, 
        "climbed_7c": False, 
        "climbing_ascents_list": fake_climbing_list
    }
    
    fake_reading_list = [
        {
        "author": "Myself", 
        "title": "My biography"
        }]
    
    fake_reading_results = {
        "reading_goal": 24, 
        "reading_expected_progress": 18, 
        "reading_progress_percentage": 90, 
        "reading_current_books": 22, 
        "reading_status": "bg-success", 
        "reading_books_list": fake_reading_list
    }

    fake_total_results = {
        "total_expected_progress": 75, 
        "total_current_progress": 76, 
        "total_status": "bg-success", 
    } """


    ################
    ### Get data ###
    ################

    running_results = running()
    climbing_results = climbing()
    reading_results = reading()

    # Calculate total progress
    total_expected_progress = ((((date.today()-start).days) / 365) * 100)

    total_current_progress = running_results["running_progress_percentage"]
    total_current_progress += reading_results["reading_progress_percentage"]
    if climbing_results["climbed_8a"] == True:
        total_current_progress += 50
    if climbing_results["climbed_7c"] == True:
        total_current_progress += 50

    total_current_progress = (total_current_progress / 300) * 100

    # Get status for progress bar color
    if total_current_progress < (total_expected_progress * .90):
        total_status = 'bg-danger'
    elif total_current_progress >= total_expected_progress:
        total_status = 'bg-success'
    else:
        total_status = 'bg-warning'

    total_results = {
        "total_expected_progress": total_expected_progress, 
        "total_current_progress": total_current_progress, 
        "total_status": total_status
    }



    return render(request, "mysite/goals.html", {
        #"climbing_results": fake_climbing_results,     # For testing without triggering scraper/API calls
        #"running_results": fake_running_results,       # For testing without triggering scraper/API calls
        #"reading_results": fake_reading_results,       # For testing without triggering scraper/API calls
        #"total_results": fake_total_results,                    # For testing without triggering scraper/API calls
        "climbing_results": climbing_results,        # Real data
        "running_results": running_results,          # Real data
        "reading_results": reading_results,          # Real data
        "total_results": total_results               # Real data
        
    })


def scraper_options():
    options = Options()
    options.add_argument('--headless=new')
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
    options.add_argument(f'user-agent={user_agent}')
    options.add_argument("window-size=1400,600")

    return options


def climbing():  
    climbing_url = 'https://www.8a.nu/user/pepperoni-papi/sportclimbing'
    climbing_username = 'tkontovich@gmail.com'
    climbing_pw = '[BVsi2p[#6aN8E+CY%]k'
    driver = Chrome(options=scraper_options())

    # Navigate to non-auth page
    driver.get(climbing_url)

    time.sleep(1)

    # Navigate to login page
    login_btn = driver.find_element(By.CSS_SELECTOR, '.not-auth-placeholder > button')
    time.sleep(.1)
    login_btn.click()

    # Fill in login info and submit
    climbing_username_input = driver.find_element(By.CSS_SELECTOR, '#username')
    climbing_pw_input = driver.find_element(By.CSS_SELECTOR, '#password')
    climbing_login_btn_2 = driver.find_element(By.CSS_SELECTOR, '#kc-login')
    climbing_username_input.send_keys(climbing_username)
    climbing_pw_input.send_keys(climbing_pw)
    climbing_login_btn_2.click()
    time.sleep(.5)

    # Navigate to ascents section and filter by date
    climbing_filter = driver.find_element(By.CSS_SELECTOR, '#dropdown-id-7')
    time.sleep(1)
    climbing_filter.click()
    climbing_dropdown_by_date = driver.find_element(By.CSS_SELECTOR, '#popover-7 > div:nth-child(2)')
    climbing_dropdown_by_date.click()
    time.sleep(.5)

    # Find ascents table and get all ascent elements
    climbing_ascents = driver.find_elements(By.CSS_SELECTOR, '.big-ascent-row')

    # Loop through ascent elements to build dict of data
    climbing_ascents_list = []
    for ascent in climbing_ascents:
        str_date = ascent.find_element(By.CSS_SELECTOR, '.col-date > div').get_attribute('innerHTML').strip()
        ascent_date = datetime.strptime(str_date, "%d %b %Y").date()

        # If ascent was from this year, add to dict
        if ascent_date > start:
            ascent_dict = {
                "date": ascent_date, 
                "route": ascent.find_element(By.CSS_SELECTOR, '.col-route > a').get_attribute('innerHTML').strip(), 
                "grade": ascent.find_element(By.CSS_SELECTOR, '.col-grade').get_attribute('innerHTML').strip(), 
                "location": ascent.find_element(By.CSS_SELECTOR, '.col-route > div > a:nth-child(3)').get_attribute('innerHTML').strip()
            }
            climbing_ascents_list.append(ascent_dict)

    driver.quit()

    climbed_8a = False
    climbed_7c = False

    for ascent in climbing_ascents_list:
        if ascent["grade"] == '8a':
            climbed_8a = True
        elif ascent["grade"] == '7c+':
            climbed_7c = True

    climbing_results = {
        "climbed_8a": climbed_8a, 
        "climbed_7c": climbed_7c, 
        "climbing_ascents_list": climbing_ascents_list
        }
    
    return climbing_results


def running():
    # Baselines for running goal
    running_goal = 365 # Total 365 miles for the year
    running_expected_progress = (date.today()-start).days * (running_goal / (end-start).days)
    
    # Connect to garmin
    running_username = 'tkontovich@gmail.com'
    running_pw = 'men9a6D6'

    garmin = garminconnect.Garmin(running_username, running_pw)
    garmin.login()

    GARTH_HOME = os.getenv("GARTH_HOME", "~/.garth")
    garmin.garth.dump(GARTH_HOME)

    # Get activities
    activities = garmin.get_activities_by_date(start, end)

    # Populate data variables
    running_current_runs = len(activities)
    running_current_miles = 0
    running_current_total_time = 0
    running_current_total_calories = 0
    for item in activities:
        running_current_miles += item['distance']/1609.34
        running_current_total_time += item['duration']
        running_current_total_calories += item['calories']

    # Make calculations
    running_progress_percentage = (running_current_miles / running_goal) * 100
    running_current_avg_pace = round(running_current_total_time / running_current_miles)
    running_current_avg_distance = running_current_miles / running_current_runs

    # Get status for progress bar color
    if running_current_miles < (running_expected_progress * .90):
        running_status = 'bg-danger'
    elif running_current_miles >= running_expected_progress:
        running_status = 'bg-success'
    else:
        running_status = 'bg-warning'

    running_results = {
        "running_goal": running_goal, 
        "running_expected_progress": running_expected_progress, 
        "running_progress_percentage": running_progress_percentage, 
        "running_status": running_status,
        "running_current_miles": running_current_miles,
        "running_current_runs": running_current_runs,
        "running_current_avg_distance": running_current_avg_distance, 
        "running_current_avg_pace": timedelta(seconds=running_current_avg_pace), 
        "running_current_total_calories": running_current_total_calories
    } 

    return running_results


def reading():
    # Baselines for reading goal
    reading_goal = 24 # Total number of books for the year
    reading_expected_progress = (date.today()-start).days * (reading_goal / (end-start).days)

    reading_url = 'https://www.goodreads.com/user_challenges/49474907'
    driver = Chrome(options=scraper_options())

    # Get page and list of book items
    driver.get(reading_url)
    driver.find_element(By.CSS_SELECTOR, '.loadMoreButton').click()     # Click load more button to populate full list of books
    time.sleep(.5)                                                      # Wait for remaining book items to load
    books = driver.find_elements(By.CSS_SELECTOR, ".bookCoverContainer")
    reading_books_list = []

    # Loop through book item elements, saving title to list
    for book in books:
        book_item = book.find_element(By.CSS_SELECTOR, "div > a > img")
        title = book_item.get_attribute("alt")
        book_dict = {
            'title': title.split(" by ")[0],
            'author': title.split(" by ")[1]
        }
        reading_books_list.append(book_dict)

    # Get current progress + percentage done
    reading_current_books = len(reading_books_list)
    reading_progress_percentage = (reading_current_books / reading_goal) * 100
 
    # Get status for progress bar color
    if reading_current_books < (reading_expected_progress * .9):
        reading_status = 'bg-danger'
    elif reading_current_books >= reading_expected_progress:
        reading_status = 'bg-success'
    else:
        reading_status = 'bg-warning'

    driver.quit()

    reading_results = {
        "reading_goal": reading_goal, 
        "reading_expected_progress": reading_expected_progress, 
        "reading_progress_percentage": reading_progress_percentage, 
        "reading_current_books": reading_current_books, 
        "reading_status": reading_status, 
        "reading_books_list": reading_books_list
    }

    return reading_results
