
# SecureSummit

SecureSummit is a software solution created by Mountain Peak software (MTN) to provide casinos a secure way to transfer, track and manage their inventory of assets.

This guide contains the details of running the GUI locally.


## Prerequisites

#### Please ensure the backend is running locally.


## Deployment

- Clone the main branch of the repository
- Create a python virtual environment
```
python -m venv {environment name}
```
- Install the required packages
```
python -m pip install -r requirements.txt
```
- Run the admin application
```bash
  python -u adminApp.py
```
- Run the guard application
```bash
  python -u guardApp.py
```


## Running Tests

To run tests, run the following command

```bash
  pytest
```


## Authors

- [@Matthew Bordonaro](z5354286@ad.unsw.edu.au)
- [@Tristan Nast](z5354277@ad.unsw.edu.au)
- [@Nahum Ferguson](z5364396@ad.unsw.edu.au)


![Logo](https://i.imgur.com/7m4CB5w.png)

