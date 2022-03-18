# README

### Environment
- Docker
- Python version: 3.9

### Docker
``` sh
docker build -t flask .

docker run -d -p 5000:5000 flask:latest

docker ps -a

docker logs <container ID>

``` 


### Project Structure Explanation
``` sh
|   .coverage
|   README.md
|   requirements.txt  # python requirements package
|   run.py  # main function
|   __init__.py
|   Dockerfile
|
+---.idea
|
+---.pytest_cache
|
+---app
|   |   tasks.py  # service
|   |   __init__.py
|   |
|   \---__pycache__
|
+---tests
|   |   .coverage
|   |   test_tasks_bak.py  # unittest
|   |   __init__.py
|   |
|   +---htmlcov
|   |       test_tasks_py.html  # pytest report
|   |
|   \---__pycache__
|
\---__pycache__

```