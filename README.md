# Cook Book

The purpose of this web app is to provide users with an online recipes book where they can add, update or delete their recipes so that it generates a wide variety of recipes from around the world to be referred.
Users can get recipes using a search box by entering a recipe name or ingredient as well as through a filter where the recipes are sorted by category, cuisine and difficulty.

The web app shows a home page with the filter, a general view of all the recipes added by the users to the cook book; a detail view per recipe displaying the name of the recipe, a picture, the category, the cuisine, the serves, the preparation time, the difficulty, the ingredients, the instructions and tips to prepare the recipe. Also there is a general view of all recipes from where the user can edit, delete and view the recipes.

## UX

The web app was created to allow users to add and easily access cooking recipes from any device with internet connexion.
It was designed following ‘mobile first’ approach, making use of Materialize framework for the look and feel.
And built using Python for the logic and Flask to run the application.

The recipes can be filtered by category, cuisine or difficulty, which results quick and easy to find a recipe. 
The webapp has also a search box for this purpose, where a keyword can be typed to get a result page with the recipes.
A link for adding a recipe is available widesite making possible to insert a recipe through a form filling the fields required.
Edit or delete a recipe is also available for each recipe in the recipe detail view and in a general view.

### Assets
User stories >  https://github.com/pazcm/cook-book/pre-dev/user-stories.png

Wireframes >  https://github.com/pazcm/cook-book/pre-dev/wireframes

Database Schemas examples > https://github.com/pazcm/cook-book/pre-dev/db schemas


## Features
#### Main Navigation widesite.-
Allows user to navigate through the site.
#### Search box .- 
Allows user to search recipes by name and/or ingredient.
#### Filter .- 
Allows user filter by category, cuisine and difficulty to find a recipe.
#### Add recipe Form .- 
Allows user to add a new recipe to the webapp.
#### Edit recipe Form .- 
Allows user to modify a recipe in the webapp.
#### Delete recipe .- 
Allows user to delete a recipe from the webapp.
#### Follow Social networks .- 
Allows user to follow the webapp.

## Left to implement
#### Sign up/in .- Registration functionality to allow users create an author profile and be able to save, like and share recipes.
Secure user authentication was not required for this project, is something that I would like to implement in the future together with the following funtionalities remained:
#### Like recipe .- 
Like function which will allow users give feedback to other users and track the recipes they like.
#### Share recipe .- 
Share funciton which will allow users share a recipe in their social networks.
#### Save recipe .- 
Save function which will allow users to save their favourites recipes.
#### Load more .- 
Load more button in all recipes view to load more recipes if they exists.

## Technologies Used
### [IDE Cloud9](console.aws.amazon.com/cloud9/ide)
#### The project uses an online IDE for development.

### [Git/GitHub](https://github.com)
#### The project uses **Git** version control to manage and track the changes in the code.

### [Balsamiq Cloud](https://balsamiq.com/wireframes/cloud/)
#### The wireframes for the project were created using Balsamiq GUI wireframe builder cloud application.

### [HTML5](https://html.spec.whatwg.org/multipage/)
#### The project uses semantic **HTML5** elements to structure and present the content in a consistent way following the W3C standards.

### [Materialize](https://materializecss.com)
#### The project uses Materialize as a responsive FE framework taking default stylings and components.

### [JQuery](https://jquery.com)
#### The project uses **JQuery** to initialize some site elements and components.

### [CSS3](https://www.w3.org/Style/CSS/)
#### The project uses **CSS3** to create custom style.

### [Google Icon font](https://material.io/resources/icons/)
#### The project uses **Google Icon font** to provide the font icons for the app.

### [Font Awesome](https://fontawesome.com/)
#### The project uses Fontawesome javascript to get the Social Icons widesite.

### [MongoDB Atlas](https://cloud.mongodb.com)
#### The project uses **MongoDB Atlas** to create the Data Base and connect with the app to carry out CRUD operations.

### [Flask](https://palletsprojects.com/p/flask/)
#### The project uses **Flask**, Python BE framework to create the web app alongs with the Python templates' engine **[Jinja2]**(http://jinja.pocoo.org/)

### [Heroku](https://www.heroku.com/home)
#### the project uses the hosting platform **Heroku** to deploy and run the app.

## Testing
During development Manual testing for checking work functionalities and behaviours as well as responsive design was conducted continuously using Chrome browser. Chrome and Chrome Developer Tools were the main browser and tool used for testing. Moreover, the site was tested using Firefox and Safari browsers.
All features and each modification was checked in Chrome, Firefox and Safari browsers and tested using developer tools at full width resolution. As well as using several devices emulators with different screen sizes for Responsive testing; such as Nexus 5X, Nexus 10, Galaxy S5, iPhone 6/7/8, iPhone 6/7/8 Plus, iPhone X, iPad and iPad Pro.
#### HTML was validated using the Markup Validation Service provided by The World Wide Web Consortium: https://validator.w3.org/
#### CSS was validated using the CSS Validation Service provided by The World Wide Web Consortium: https://jigsaw.w3.org/css-validator/

##### Test cases:
Add recipe:
1. From the main menu or from the second link in the footer, go to ‘Add recipe’ link.
2. Try to submit a new recipe and verify that an error message about the required fields appears
3. Fill up all fields required and try to submit the recipe and verify that it was added to the database and showed in ‘All Recipes’ view.
4. From there or from the recipe detail view try to ‘Edit / Delete the recipe’ and verify that this is accomplished.


Results page:
1. From the navigation bar enter a recipe name in the search box and verify that you are redirect to a results page.
2. Try to enter an ingredient and verify that you are redirect to a results page.
3. Try to enter an invalid word and verify that some options/tips are given.


### Issues

- Category radio buttons in form. After adding raido buttons in the app form (for add and edit recipe) using Materialize framework, had no selection when clicking in a category.
Fixed by including the <label> tags for each input.
- Path Image broken in recipe detail view, getting a few 404 error for images.
Fixed by using jinja's url_root method `<img src="{{url_for('static' filename='images/example.jpg')}}">` instead of hardcode the filepath, with `<img src="static/images/example.jpg">`


## Deployment

0. [I created a git repository in GitHub for this project (enter address]
1. From my browser, I went to heroku hosting platform and log in
2. From the Heroku Dashboard, I ‘create new app’ => with the app name: online-cook-book-app
3. In my Cloud9 IDE, I opened a console and installed the Heroku CLI =>
4. Then I went to log in to my Heroku account and follow the prompts to create a new SSH public key =>  heroku login —interactive ( to create a connexion between my Cloud9 IDE and Heroku which will allow me to push my code using Git)
5. After that I made some changes in my initial Flask application (app.py file) and README.md file and deploy them to Heroku using Git:
$ git add .
$ git commit -m “first commit"
$ git push heroku master

6. Next I add the requirements file to the project, to install the Python modules that are required for Heroku to build the app =>
pseudo pip3 freeze --local > requirements.txt >> and push to heroku
7. After that I added the Proctfile file to the project required for heroku to call the application >> and push to heroku
8. From heroku platform / settings tab => I set the variables for the server instance to run the app >> Config Vars - IP: 0.0.0.0 / PORT: 5000
9. Finally is deployed and I go to 'Open app' from Heroku GUI

My app lives here: https://online-cook-book-app.herokuapp.com/

## Credits
http://stackoverflow.com/
https://codepen.io/j_holtslander/pen/wXEWqe
https://flask.palletsprojects.com/en/1.0.x/quickstart/
https://www.fullstackpython.com/flask.html
https://dzone.com/articles/flask-101-how-to-add-a-search-form
https://www.mongodb.com/blog

### Content / Media
The images and some content was extracted around the web, from different pages such us https://www.tasteatlas.com/ for testing/studying purpose, no for production or comercial uses.

#### Note:
There was some changes/variations from the initial wireframes, such as the placement of the Logo or the kind of Filter election which was modified for a better user experience.

### Acknowledgements
Thanks to my Mentor for the feedback and help during the development and many Thanks too to the Tutor support from Code Institute for their help with several issues.