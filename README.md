# SGX3-Hackathon-Project-2024

## Event Info
SGX3 ADMI24 Hackathon (view their website [here](https://hackhpc.github.io/sgx3admi24/))

## Team NLC^2
### Mentor
**Teniola Oluwaseyitan**       
Mississippi Valley State University

### Teammates
**Christian Johnson**     
Morehouse College

**Nole Stites**      
Southern Oregon University

**Robert Campbell**     
Southern Oregon University

**Lisha Ramon**     
SUNY Oneonta

|  |  |  | 
|-|-|-|
| ![](images/hackathon_logo.png) | ![](images/team_logo.png) | ![](images/sgx3_logo.png) |
     
| image1 | image2 | image3 | 
|--------|--------|--------|
| ![](images/hackathon_logo.png) | ![](images/team_logo.png) | ![](images/sgx3_logo.png) |

## Project Description
There are institutions that don't have easy ways to categorize or present their training resources. Currently, HPC-ED utilizes a command-line interface (CLI) to add data (training material) to and query data from a database which is not at all user friendly or intuitive. Many people don't know how to use a CLI, so they don't get the opportunity to use the training resources.

Furthermore, most people go to Google for their needs which isn't the best way to search. A given Google query might return thousands of results, making it hard to know which ones are worth looking at because the quality of sources vary. By having a database that stores only the institution-quality training materials and resources, you can be sure that all of the results from querying the database will be useful in some manner.

## How to Run
1. Clone the repository.   
Using HTTPS:
```
$ git clone https://github.com/ChristianJohnsonL/SGX3-Hackathon-Project-2024.git
```
Using SSH:
```
$ git clone git@github.com:ChristianJohnsonL/SGX3-Hackathon-Project-2024.git
```
Using GitHub CLI
```
$ gh repo clone ChristianJohnsonL/SGX3-Hackathon-Project-2024
```
2. Enter the cloned repo.
```
$ cd SGX3-Hackathon-Project-2024
```
3. Add the `.env` file. **TODO**
4. Create a virtual environment.
```
$ python3 -m venv env && source env/bin/activate
```
5. Navigate further into the repo.
```
$ cd hpced
```
6. Setup the server.
```
$ python3 manage.py makemigrations && python3 manage.py migrate
```
7. Start the server.
```
$ python3 manage.py runserver
```
8. View the project website in a browser at `localhost:8000`.
9. Login to the server and begin your research!

## Repository Structure

This repository is organized as follows:

- `hpced/`: This directory contains all of the code necessary to run the project.
    - `hpced/`: description of file
        - `templates/hpced/`: This directory contains all of the HTML file templates for the project website.
            - `base.html`: Contains the base HTML to be inherited by all other pages.
            - `index.html`: Contains the HTML for the home page.
            - `metadata.html`: Contains the HTML for the new entry creation page.
            - `search.html`: Contains the HTML for the search/query page.
            - `thanks.html`: Contains the HTML for the response page after creating a new resource.
        - `asgi.py`: Contains the ASGI configuration for the project.
        - `forms.py`: Contains the contents of the HTML forms rendered on the project website.
        - `globus_api.py`: Contains the functions for authenticating with Globus and performing queries.
        - `settings.py`: Contains the Django settings for the project. Mostly generated by Django.
        - `urls.py`: Contains the URL configuration for the project.
        - `view.py`: Contains the logic for rendering website pages and accepting form POST requests.
        - `wsgi.py`: Contains the WSGI configuration for the project.
    - `manage.py`: Contains Django's command-line utility for administrative tasks.
- `.gitignore`: Contains a list of files and directories to ignore when pushing local changes to the repository.
- `README.md`: Contains the overview of the project and repository, including the authors, project description, and how to run the code.
- `requirements.txt`: Contains a list of Python libraries to be installed before running the code. Refer to README.md for instructions.
