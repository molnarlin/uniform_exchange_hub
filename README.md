# Milestone project 3
## uniform_exchange_hub
[](/static/images/Mock-up-for-mp3.png)
Welcome to the third milestone project for Runshaw College and Code Institute. Our platform, Uniform Exchange Hub, is dedicated to making school uniforms accessible and affordable for everyone. This website allows users to find pre-loved school uniforms, exchange them, donate to a uniform bank, or acquire second-hand uniforms for their children.

Built using MongoDB and Flask, the application offers a comprehensive CRUD (Create, Read, Update, Delete) functionality along with robust user authentication. Users can easily register, log in, log out, edit profiles, view profiles, search for uniforms, and even delete their accounts.

## 1. Purpose of the project
  ### 1.1. Business Goals
Uniform Exchange Hub aims to:

- Promote sustainable fashion by encouraging the reuse of school uniforms.

- Make school uniforms accessible and affordable for every family.

- Build a supportive community where people can help one another.

- Reduce textile waste by offering a platform for uniform donations and exchanges.

### 1.2. Developer's Goals
As developers, our objectives are to:

- Create a user-friendly, intuitive interface that simplifies the process of exchanging uniforms.

- Create security for all user data with comprehensive user authentication mechanisms.

- Optimize the performance of the website for seamless user experience.
## 2. User stories
- As a parent, I want to easily search for available school uniforms in my child's age so that I can find what I need quickly.

- As a donor, I want to donate uniforms my child has outgrown so that other families can benefit from them.

- As a registered user, I want to exchange my uniforms for different sizes so that my children can have well-fitting uniforms throughout the school year.

- As a user, I want to see a detailed profile page so that I can manage my personal information and donations.

- As an admin, I want to manage user accounts and listings so that the platform remains organized and user-friendly.

- As a new user, I want to register easily so that I can quickly start using the platform.

- As a user, I want to log in and log out securely so that my personal data is protected.

## 3. Features
   ### 3.1. Existing features
   * Navigation bar on the top helps to navigate between different pages.
   * User registration and authentication. 
   * Profile display, and management.
   * Uniform search.
   * Intorduction to this charity website.
   * Footer with some additional information.
   ### 3.2. Future features
   * Making possible for Organizations to register more users.
   * Basis chat function to answer some questions or if AI can't answer the question, send an email to Support.
   * Connecting TrustPilot or other website, and asking people for reviews.
## 4. Typography and color scheme
* Google Fonts
* Colour palette
* Images were created with Microsoft Copilot
## 5. Wireframes
I used Balsamiq to create my wireframes. There are more pages, you can chack them here: 
* [Home Page](static/images/Home%20Page.pdf)
* [Search Page](static/images/Search%20Page.pdf)
* [Log In Page](static/images/Log%20In%20Page.pdf)
* [Register Page](static/images/Register%20Page.pdf)
* [Profile Page](static/images/Profile%20Page.pdf)
* [Edit Profile Page]()

I modified my wireframe a couple of times; this is the latest version. This wireframe helped me to position things and organize my content.
## 6. Technologies used
* I used HTML to create the layout and the basic structure for the website.
* Materialize CSS to style the website.
* Flask micro framework to build the functionality of this website.
* JavaScript to help with modals, date picker, and collapsibles.
* MongoDB to store user's data.
* Jinja to help with the interactivity for dynamic website. Works really well with Flask.
* I used Balsamiq for my wireframe, so I could think about the structure of my website, size the features, and see how things can work/function.
* I used git for version control.
* I used GitHub to save my repository and deploy my project online.
* I used Microsoft Copilot and Blackbox AI to check my code, create pictures and advise improvement.
* I used [www.canva.com](https://www.canva.com) to create mockups for different screen sizes.
## 7. Testing
   ### 7.1 Code validation
   * I used the official W3C validatorW3C validator link for testing HTML, and there were no errors.
   * Official (jigsaw) CSS validator link validator for testing CSS, and my code had no errors.
   * Lighthouse report in Google Chrome. I checked the accessibility, performance, and best practices here.
   ### 7.2 Test Plan Tables

## 8. Fixed bugs
I came across a couple of bugs and I briefly explained how I fixed them here.
- I couldn't display user's profile.
- I had problem connacting to Heroku. I had to update requirements.txt to make it work.
- Search wasn't working.
## 9. Supported screens and browsers
I used Google Chrome's Inspect tool to test my webpage on various devices with different screen sizes, please see picture below. I found that it rendered well without any issues. I checked the website in Microsoft Edge, Samsung Internet Browser and Google Chrome as well, but I could not find any problems. The site looked responsive and performed as expected.
## 10. Deployment
   ### 10.1. via VS Code
   If you want to open the file locally, first type python3 -m http.server, open a new terminal, type `python3 run.py` in terminal. There will be 2 ports, open 5000 in Browser.
   ### 10.2. via Heroku
   I deployed it on [Heroku](https://uniform-exchange-hub-9de6578280cd.herokuapp.com/)
## 11. Credits
- I must say a big thank you to Runshaw College and Code Institute for guiding me and helping me with this project. I used Code Institute's Task Manager walk through project as a starting point for this.
- I needed to learn about Mongo DB, so I bought an Udemy course, what I used to understand, how to communicate with Mongo DB.
