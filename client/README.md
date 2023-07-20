# Client
## Development Environment Setup
1. Install [Node](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm#using-a-node-version-manager-to-install-nodejs-and-npm)
2. Install [Yarn](https://yarnpkg.com/getting-started/install)
3. Install yarn dependencies: `yarn install`
4. Run locally: `yarn dev`
## Hosting deployment
1. Go to [hosting](https://krystal.uk/client/clientarea.php)
2. Launch cPanel
3. Go to Software -> Setup Node.js App
4. Go to Admin-Build app
5. Please note that this app should never be running - its only purpose is to build the client
6. Copy virtual environment script from the top of the page. E.g.

        `source /home/afeedbff/nodevenv/stc-ad-credit/client/18/bin/activate && cd /home/afeedbff/stc-ad-credit/client`
7. SSH to hosting: `../ssh-krystal.bash`
8. Run virtual env script
9. Update local repository: `git checkout main && git pull`
10. Update packages: `npm install --include=dev`
11. Build client: `npm run build`
12. Ensure that dist folder is linked to `~/public_html/`
    1. Run `readlink -f ~/public_html/admin`, it must return dist folder e.g. `/home/afeedbff/stc-ad-credit/client/dist`
    2. Link if not linked: `ln -s ~/stc-ad-credit/client/dist ~/public_html/admin`