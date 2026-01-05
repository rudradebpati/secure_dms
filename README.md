# Global Storage

This is a Django project that provides a RESTful API for managing files and folders in a global storage system. It includes the following components:

## User Management

Users can register and log in to the system using the `/auth/` endpoints.

## Folder Management

Users can create, update, and delete folders. Folders can be nested and contain files and other folders.

## File Management

Users can upload, download, and delete files. Files are stored in the global storage system and can be accessed through their URLs.

## Access Control

Access to folders and files is controlled using permissions. Only the owner of a folder or file can access it.

## Installation

1. Clone the repository: `git clone https://github.com/rudradebpati/secure_dms.git`
2. Install the dependencies: `pip install -r requirements.txt`
    -- Check FIXTURES dir to get a skeleton of dot env
3. Create a `.env` file in the project root directory and add the following line: 
`SECRET_KEY=<your-secret-key>`
4. Run the migrations: `python manage.py migrate`
5. Start the development server: `python manage.py runserver`

## Usage

### User Management

- Register a new user: `POST /auth/register/`
- Log in a user: `POST /auth/login/`

### Folder Management

- Create a new folder: `POST /folders/` with the `name` field in the request body
- Update a folder: `PUT /folders/<folder-id>/` with the updated `name` field in the request body
- List all folders: `GET /folders/`
- Get a folder by ID: `GET /folders/<folder-id>/`

### File Management

- Upload a file: `POST /files/` with the `file` field in the request body as form-data
- Download a file: `GET /files/<file-id>/download/`
- Delete a file: `DELETE /files/<file-id>/`
- List all files: `GET /files/`
- Get a file by ID: `GET /files/<file-id>/`

## API Reference

For more information on the available endpoints and request/response formats, please refer to the API documentation.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.
