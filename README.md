# README

### Environment
- Docker
- Python : 3.9

- Requirements:
  - Flask==1.1.4
  - marshmallow==3.15.0
  - markupsafe==2.0.1
  
### Docker
``` sh
docker build -t flask .

docker run -d -p 5000:5000 flask:latest

docker ps -a

docker logs <container ID>
``` 

### Unittest
``` sh
pytest tests/test_tasks.py 
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