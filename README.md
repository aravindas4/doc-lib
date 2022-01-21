# DocLib

The Backend APIs for Document Management.

## Getting Started

1. Need to make sure [python3.8+](https://www.python.org/downloads/release/python-380/) is installed on the machine
2. Need to create and activate a [virtualenv](https://docs.python.org/3/library/venv.html)
```bash
virtualenv -p python3 doc-lib
source ./doc-lib/bin/activate
```
3. Installed the dependencies
```bash
pip3 install requiremnets.txt
```
4. Move into environemnt and clone the [repo](https://github.com/aravindas4/doc-lib)
5. Duplicate `.env.example` file into `.env` and replace the dummy values with genuine
6. Run the migration command
```bash
python manage.py migrate
```

7. Run the local server
```bash
python manage runserver
```
8. Create a user using command
```bash 
   python manage.py createsuperuser
```

## Local Links:
1. Admin: `http://127.0.0.1:8000/admin/`
Default user:` admin` 
password: `something`
2. Swagger: `http://127.0.0.1:8000/swagger/`
3. Redoc: `http://127.0.0.1:8000/redoc/`

## Tech Stack
Python 3.8, Django, Django Rest Framework, Sqlite

## Assumptions and Conventions
1. Instead of uploading a file document, we create one when user initiates and log the various activities inside it
2. Authentication mechanism used is [TokenAuthentication](https://www.django-rest-framework.org/api-guide/authentication/#tokenauthentication) (only one per user)
3. [Pre-commit](https://pre-commit.com/) framework is used to do auto formatting using black 
4. [FacyoryBoy](https://factoryboy.readthedocs.io/en/stable/) package is used for testing purposes
5. All the secrets are kept in gitignored file `.env` supported by [decouple](https://pypi.org/project/python-decouple/)
6. All the documents are create at `project-root/media/documents` folder
7. API versioning is added. Ex: 
 `{{host}}/api/v1/store/document/AFE30101A3/download/`. 
8. All apps are place in `apps` folder and all apis in `apis` subfolder of apps.
9. All list APIs are [paginated](https://www.django-rest-framework.org/api-guide/pagination/)
10. Second app is `utils` which houses various utils in the code
11. [pytest](https://docs.pytest.org/en/6.2.x/) is used as testing framework

## Database Design
There are 3 models
1. User - Represents the user or human [Abstract fields provided by django]
2. Document -Represents the document of an user
`Fields: Owner: User, File, Shared users: User`
3. UserDocument - Associates Documents and Collaborators
`Fields: user: User, document: Document`

## API Structures

### Document Resource:
1. Create - By any User and there is logging
2. Delete - Only by Owner, logging
3. Edit (Patch) - Owner and Shared Users, Logging
4. Edit (Put) - Represents Reupload action, By Owner, Logging
5. List and Detail - By Owner and Shared Users
6. Download - By Owner and Shared Users, logging
8. Share - By Owner and UserDocuments are created.

### User
1. List and Detail - Any user

# Testing
```bash
pytest
```