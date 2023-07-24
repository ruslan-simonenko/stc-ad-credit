# Server
## Development Environment Setup
1. Create [virtualenv](https://virtualenv.pypa.io/en/latest/user_guide.html): `virtualenv venv`
2. Install dependencies: `pip3 install -r requirements.txt`
3. Link database - configure *database* project first: `mkdir -p instance && ln -s ../../database/dev.db instance/dev.db`
4. Run Flask Server: `flask --debug run`
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