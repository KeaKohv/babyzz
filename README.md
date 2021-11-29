# BabyZz
#### Video Demo:  https://youtu.be/zLkSkPi9510
#### Description:
[BabyZz](https://babyzz.herokuapp.com/) is a web application that gives advice on baby's sleep needs.

###### How to use
Registration is required to use BabyZz. After registering, you can add children (first name, date of birth). After adding children you are able to see general sleep suggestions on the index page and detailed suggestions under a separate page.
The app gives suggestions on, e.g. your children's waketime length, total sleep need in 24h, night and daily sleep need, advice on naps etc.
Additionally, you can edit your child's data and delete their data from the database. User can also change their password.

###### All pages
**Sign in** - Enables users to sign in by provideing their username and password.

**Register** - Enables to register by providing their First Name, username, password, and password confirmation. Password has to be at least 8 characters long, contain one uppercase and one lowercase letter, and one number.
The user is logged in automatically after registering.

**Add and see children** - Displays a list of children (their first name and data of birth). Below is a possibility to add a child.

**Edit child's data** - Enables to change the first name or date of birth of a child.

**Delete child's data** - Enables to delete child's data from the database.

**Index** - At the top of the page is a greeting using the user's first name. The page displays general suggestions on children's sleep needs that are based on available scientific studies.

**Detailed suggestions** - Displays detailed suggestions on children's sleep needs, including waketime length, total sleep need in 24h, total night sleep need, total daily sleep need, number of naps, advice on naps, number of feeds at night etc.

**Waketime schedule** - Displays suggestions on children's waketime length and schedule.

**Change password* - Enables the user to change their password by providing their current password, new password and confirmation of the password.

Additionally, the index page, detailed suggestions page and the waketime schedules page display a list of reminders. These remind the user that the sleep advice is only suggestions, and to always consult with their child's pediatrician in matters related to their child's health.



###### Languages, IDE and design
The application was created using Python, and its module Flask, PostgreSQL, HTML and CSS. VSCode was used as IDE.
The application is responsive thanks to Bootstrap.
The logo (half moon with stars on blue background) was designed in Canva.
The app is deployed on Heroku: [BabyZz](https://babyzz.herokuapp.com/).
