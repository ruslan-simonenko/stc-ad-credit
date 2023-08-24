# Server
## Development Environment Setup
1. Create [virtualenv](https://virtualenv.pypa.io/en/latest/user_guide.html): `virtualenv venv`
2. Install dependencies: `pip3 install -r requirements.txt`
3. Create `.env.local` in the project root, and put configuration properties there   
4. Setup dev database:
   1. `docker pull mysql`
   2. Run database:

          docker run --name stc-mysql -p 3306:3306 -e MYSQL_ROOT_PASSWORD=stc -v $(readlink -f instance)/mysql:/var/lib/mysql -d mysql:latest
   3. Connect to MySQL `root:stc@localhost` and create database and user: 
         
          CREATE DATABASE stc;
          CREATE USER 'stc'@'%' IDENTIFIED BY 'stc';
          GRANT ALL PRIVILEGES ON stc.* TO 'stc'@'%';
          FLUSH PRIVILEGES;
   4. Create schema: 
      1. `cd db_migration`
      2. `export APP_ENV=dev && alembic upgrade head`
   5. Afterwards:
      1. To stop database: `docker stop stc-mysql`
      2. To start database: `docker start stc-mysql`
5. Run Flask Server: `docker start stc-mysql && export APP_ENV=dev && flask --debug run`
## Hosting deployment
1. Go to [hosting](https://krystal.uk/client/clientarea.php)
2. Launch cPanel
3. Go to Software -> Setup Python App
4. Stop the app
5. Copy virtual environment script from the top of the page. E.g. 

        `source /home/afeedbff/virtualenv/stc-ad-credit/server/3.11/bin/activate && cd /home/afeedbff/stc-ad-credit/server`
6. SSH to hosting: `../ssh-krystal.bash`
7. Run virtual env script.
8. Update local repository: `git checkout main && git pull`
9. Update packages: 

        python -m pip freeze | sort > requirements-current.txt 
        comm -23 requirements-current.txt requirements.txt > requirements-to-remove.txt
        python -m pip uninstall -r requirements-to-remove.txt
        python -m pip install -r requirements.txt
10. Go to cPanel: Software -> Setup Python App 
11. Start the app