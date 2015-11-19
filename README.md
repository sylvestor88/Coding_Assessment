# Technical Assessment - Take Home Code Test

It took me about 4-5 hours to finish this assignment along with the test cases. I have used in-memory implementation as the requirement didn't mention any database. However, I have another respository in which I have implemented REST Endpoints that uses Cassandra database for storing data. The application is build using Spring Framework and in JAVA.

```sh
https://github.com/sylvestor88/WebVoteServer.git
```

# Instructions to run code

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

There exists two different test files, one for 'users' and other for 'groups'. For all tests to pass, you'll have to restart the application before running either tests as it's an in memory implementation.

The run a test:
```sh
$ pyresttest http://localhost:5000 users_tests.yaml
```
You can change the address of your application accordingly.
