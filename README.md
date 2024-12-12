# Spotify Board

**INF133 Final Project**

**Creators:** Alyssa Reyes and Dharren Ursua Agbisit

## Project Overview
Spotify Board is a web application that displays the top tracks of a user from the current month. The user is also able to rate the tracks in the top tracks of the month and this is saved in the backend. It uses the Spotify API to retrieve this information and it also uses Flask for the backend.

## How to Run the Projectin VSCode

### Step 1: Download the Project Folder
Download or clone the repository locally.

### Step 2: Set Up the Virtual Environment
1. Navigate to the backend folder.
2. Create a virtual environment.
    ```sh
    python -m venv venv
    ```
3. Activate the virtual environment.
    - Windows:
      ```sh
      venv\Scripts\activate
      ```
    - macOS/Linux:
      ```sh
      source venv/bin/activate
      ```
4. Install dependencies from requirements.txt
    ```sh
    pip install -r requirements.txt
    ```


### Step 3: Install Dependencies
Install the required dependencies using the `requirements.txt` file:
```sh
pip install -r requirements.txt
```
### Step 4: Run spotify-api.py for the Backend Server
```sh
python spotify-api.py
```

### Step 5: Run main-page.html
1. Download the Live Server extension in VSCode marketplace.
2. Right click on main-page.html and select "Open with Live Server"
