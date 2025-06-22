# HBnB API Unit Testing

To ensure the proper functioning of the HBnB API, we have implemented comprehensive unit tests by combining two complementary approaches:


## Automated Functional Testing with Postman

We used Postman to automatically test different parts of our API.  
These tests send requests with various data to the API endpoints.  
They verify that the API responds correctly with the right HTTP status codes, accurate data, and proper error handling.  
These functional tests simulate real usage scenarios, helping to ensure the API works correctly in all cases.  
They are automated, making it easy to run them regularly and quickly during development.  
We preferred Postman over Swagger for this purpose.

The Postman script is available for automated testing.
Filename: script_postman in the folder tests


## Unit Testing in Python with unittest

We also created unit tests in Python using the `unittest` module.  
These tests check that each function or method in our application works correctly on its own.  
They help quickly identify issues when code changes are made and ensure the logic is correct.  
With these tests, we can precisely control actions like creating, updating, or deleting data, and verify error handling.  
By combining unit tests and functional tests, we achieve thorough coverage of all parts of the project.


## Test Report

Below is our test log, which records step-by-step the tested endpoints, input data used, as well as the expected results compared to the actual results obtained.  
We also note any problems encountered during testing. This documentation is essential to present our results and demonstrate that the implementation meets all the defined requirements.

📄 [Documentation test (PDF)](../TEST_Units_Places_and_Reviews.pdf)
