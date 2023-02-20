# arcadian

![arcadian: a simple budgeting app](https://i.imgur.com/9WVml0Q.png)

Following the closure of [Simple](https://en.wikipedia.org/wiki/Simple_(bank)) in 2021, I've been searching for an ideal budgeting application.

After being betrayed by neobanks a 2nd time (looking at you One Finance), I decided to start building my own.

arcadian uses Django, Postgres, and Svelte. Components are from the [IBM Carbon](https://github.com/carbon-design-system/carbon-components-svelte)

## Install:

1. Clone into a directory

   ```sh
   git clone ttps://github.com/kitschmensch/arcadian.git
   cd arcadian
   ```

2. Create virtualenv, install dependencies.

   ```
   virtualenv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. Install frontend dependencies and start vite dev environment

   ```
   cd frontend
   npm install
   npm run dev

4. In a seperate terminal, start Django server. Vite automatically builds front end assets into a directory that Django serves.

   ```
   cd ~/arcadian
   source venv/bin/activate
   python manage.py runserver
   ```

5. visit `http://127.0.0.1:8000/` to test!


   
