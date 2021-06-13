## My thought process while building the solution 

### Approach:

- Made use of sqlite which doesn't require any external dependencies or servers set up. 
- Used seperate preprocessing methods and made sure the given data is loaded in a standard format.
- Used pytest to easily test out the api with minimal fixtures to get the job done.
- Documented and added comments how much ever I can.
- Kept in mind the reusability of the code in this appoach
- The database schema is normalised to handle

## Future scope

- Add more tests with increasing functionalities and code coverage
- Use more scalable databases and maybe maintain seperate cache like redis when needed.
- Add security to the handle data via encryption, or de-duplication, if the use cases require it
- Introduce retries for failures.
- Add extensive error handling, monitoring (like latency of processing) for failures
