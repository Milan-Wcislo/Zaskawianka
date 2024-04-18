# Zaskawianka Football Club Website

## Local Football Club Website Built with Flask and MySQL

This website showcases information about your favorite local club, Zaskawianka! It utilizes Flask for the backend and MySQL for the database.

**[Zaskawianka Website](https://www.zaskawianka.pl)**

### Features

#### User Management
  * User registration allows creating new user accounts
  * User login enables authenticated access to specific functionalities.
  * User logout functionality ends the authenticated session.

#### Sponsor Management
  * Create new sponsors with associated logos.
  * Edit existing sponsor details and logos.
  * Delete sponsors and their uploaded logos.

#### Club Members Management:

  * Maintain a list of club management members and their positions.
  * Add new members to the management board.
  * Edit existing management member details.
  * Delete members from the management board.

#### Team Management:

  * Showcase a list of teams associated with the club.
  * Create new teams with logos and details.
  * Edit existing team details and logos.
  * Delete teams and their uploaded logos.

#### Project Management:

  * Showcase a list of club projects.
  * Create new projects with descriptions and logos.
  * Edit existing project details and logos.
  * Delete projects and their uploaded logos.


### Getting Started

**Target Audience:** This guide is intended for developers familiar with Python and Flask.

**Prerequisites:**

* Python 3
* pip

**Installation:**

1. **Clone** the repository or download the project files.
2. **Install Dependencies:** Navigate to the project directory in your terminal and run the following command:
   
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Variables:**  Create a `.env` file in the project root directory. This file should contain the following environment variables:
     * `SECRET_KEY`: A secret key used for generating cryptographic tokens.
     * `DB_URI`: A secret key used for connecting to **MySQL** database.
  
4. Database Setup:
    * The project utilizes SQLAlchemy as an ORM. The database tables are created automatically within the app.context_processor decorator.

5. Run the Application: Execute the following command in your terminal:
   
   ```bash
   python app.py
   ```

### Find a bug?
  Please submit the issue using issues tab. I would be greateful!
   

