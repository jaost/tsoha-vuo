# Vuo
## Share photostreams with a passphrase

### Features
- User login
- Logged in users can create their stream with passphrase (eg. platform.com/feed/< passphrase >)
- Anyone knowing the passphrase can view created stream without login
- Logged in users can upload photos to any stream
- Users can remove their own uploads
- Feed creators can delete the whole feed or individual items

### Considerations
- [ ] Users can upvote photos
- [ ] Light [Preact](https://preactjs.com/) front to render feeds & update live
- [ ] [Ably](https://www.ably.io/) integration to get feed updates in real time
- [ ] Require [reCAPTCHA](https://www.google.com/recaptcha/about/) on auth & upload forms.
- [ ] Let feed owner disable uploads
- [ ] Hide guest uploads from public feed

## Heroku
[Tsoha-vuo](https://tsoha-vuo.herokuapp.com/)

## Running the environment

Make sure you are running PostgreSQL instance locally.
Git clone

Create .env file
```python
DATABASE_URL=< database url >
SECRET_KEY=< string >
```

Run virtual environment in the project folder
```python
source venv/bin/activate
```

Install project requirements 
```python
pip install -r requirements.txt
```

Drop & create tables to database
```python
psql < schema.sql
```

Run flask
```python
flask run
```

## Images of the running project
![Vuo](https://raw.githubusercontent.com/jaost/tsoha-vuo/master/documentation/VuoIndex.png)
![Vuo](https://raw.githubusercontent.com/jaost/tsoha-vuo/master/documentation/VuoLogin.png)
![Vuo](https://raw.githubusercontent.com/jaost/tsoha-vuo/master/documentation/VuoNewFeed.png)
![Vuo](https://raw.githubusercontent.com/jaost/tsoha-vuo/master/documentation/VuoFeed.png)
![Vuo](https://raw.githubusercontent.com/jaost/tsoha-vuo/master/documentation/VuoNewItem.png)
![Vuo](https://raw.githubusercontent.com/jaost/tsoha-vuo/master/documentation/VuoFeed2.png)

