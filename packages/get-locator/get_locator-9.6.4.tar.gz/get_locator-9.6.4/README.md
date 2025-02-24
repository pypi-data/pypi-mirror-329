# Interesting library

This project helps to generate locators for a web project. The project is based on 
selenium. It can be used in Python + Pytest + Selenium(Selene) bundle
P.S.: Sometimes after moving to another page when clicking on elements that redirect 
somewhere or open something, the locator is not generated, but a click occurs, 
this problem has not been solved yet. Therefore, I advise you to run the project 
through the terminal and opens each page (if you need several pages) in a new terminal. 
Then locators will be generated for all elements. 

1. Run via command line using default test arguments:
   - run-inspector --url "https://demoqa.com/automation-practice-form"
2. Run project with web_inspector.py file 
- You can also add your tags to priority if your team uses its own specific tags.
- File will be created at the root of the project after first run this command:
  - create-setup --run
3. To exit, click the Q button.
4. 