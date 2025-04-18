# My Portfolio Website

   This repository contains the code for my personal portfolio website, showcasing my projects, skills, and experience.

   ## Table of Contents

   * [Project Overview](#project-overview)
   * [Features](#features)
   * [Technologies Used](#technologies-used)
   * [Setup Instructions](#setup-instructions)
   * [Usage](#usage)
   * [Directory Structure](#directory-structure)
   * [Contributing](#contributing)
   * [License](#license)
   * [Contact](#contact)

   ## Project Overview

   This portfolio website serves as a central hub for my professional profile. It provides detailed information about my data science projects, related tools I've developed, and other relevant information. The goal is to create an engaging and informative platform for potential employers, collaborators, and anyone interested in my work.

   ## Features

   The website includes the following key features:

   * **About Me:** A section detailing my background, skills, and experience.
   * **Portfolio:** In-depth descriptions of my data science projects, highlighting my contributions and the technologies used.
   * **Tools:** A collection of web-based tools I've developed, such as a resume checker, job description matcher, and more.
   * **Blog:** A space for me to share articles and insights on data science and related topics.
   * **Side Projects:** Showcases personal projects and experiments.
   * **Contact Me:** A form for visitors to get in touch with me.

   ## Technologies Used

   The website is built using the following technologies:

   * **Backend:** Django (Python web framework)
   * **Frontend:** HTML, CSS, JavaScript
   * **Database:** PostgreSQL
   * **LLM Integration:** Google Gemini API
   * **Other Libraries:** (List any other Python libraries you use, e.g., `psycopg2`, `dotenv`, etc.)

   ## Setup Instructions

   To run this website locally, follow these steps:

   1.  **Clone the Repository:**
       ```bash
       git clone <your-repository-url>
       cd <your-repository-name>
       ```

   2.  **Create a Virtual Environment (Recommended):**
       ```bash
       python -m venv venv
       venv\Scripts\activate  # On Windows
       source venv/bin/activate # On macOS/Linux
       ```

   3.  **Install Dependencies:**
       ```bash
       pip install -r requirements.txt  # If you have a requirements.txt file
       #  Or install individually:
       pip install Django psycopg2 python-dotenv google-generativeai PyPDF2 
       ```

   4.  **Database Setup:**
       * Ensure you have PostgreSQL installed and running.
       * Create a database for the project.
       * Create a `.env` file in the root directory of the project and add your database connection details:
           ```
           DB_NAME=your_database_name
           DB_USER=your_database_user
           DB_PASSWORD=your_database_password
           DB_HOST=your_database_host (e.g., localhost)
           DB_PORT=your_database_port (e.g., 5432)
           GOOGLE_GEMINI_API_KEY=YOUR_GEMINI_API_KEY
           ```
       * **Important:** Never commit your `.env` file with sensitive information to your repository! Add it to your `.gitignore` file.

   5.  **Run Migrations:**
       ```bash
       python manage.py migrate
       ```

   6.  **Create a Superuser (Admin):**
       ```bash
       python manage.py createsuperuser
       ```

   7.  **Run the Development Server:**
       ```bash
       python manage.py runserver
       ```
       * The website should be accessible at `http://127.0.0.1:8000/`.

   ## Usage

   * **Navigation:** Use the navigation bar to explore the different sections of the website.
   * **Tools:** The "Tools" section provides interactive tools. Follow the instructions on each tool's page to use it.
   * **Contact Form:** Use the contact form to send me a message.

   ## Directory Structure
