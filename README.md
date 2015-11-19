# Technical Assessment - Take Home Code Test

This project is build on Python 2.7.10 and requires flask installation.

To install flask:
```sh
$ sudo pip install flask
```

To run the application:

```sh
$ python app.py
```
This will run the application on below default localhost unless any port changes have been made for flask settings:

```sh
http://localhost:5000
```

For running tests, you'll need to install pyresttest module:
```sh
$ sudo pip install pyresttest
```

There exists two different test files, one for 'users' and other for 'groups'. In order for all tests to pass, you'll have to restart the application for before running either tests as it's an in memory implementation.

The run a test:
```sh
$ pyresttest http://localhost:5000 users_tests.yaml
```
You can change the address of your application accordingly.
