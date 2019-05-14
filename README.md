
PasswordlessDRF is a quick way to integrate ‘passwordless’ auth into
your Django Rest Framework project using a user’s email address or
mobile number only.

Built to work with DRF’s own TokenAuthentication system, it sends the
user a 4-digit callback token to a given email address or a mobile
number. The user sends it back correctly and they’re given an
authentication token (again, provided by Django Rest Framework’s
TokenAuthentication system).

Callback tokens by default expire after 15 minutes.

Example Usage:
==============

```bash
curl -X POST -d “email=joe@email.com” localhost:8000/auth/email/
```

Email to joe@email.com:

```
...
<h1>Your login token is 7834.</h1>
...
```

Return Stage

```bash
curl -X POST -d "token=7834" localhost:8000/callback/auth/

> HTTP/1.0 200 OK
> {"token":"76be2d9ecfaf5fa4226d722bzdd8a4fff207ed0e”}
```

Requirements
============

- Python (3.6+)
- Django (1.11+)
- Django Rest Framework + AuthToken (3.9+)
- Africa Stalking( for mobile.)
- Sendgrid( for email.)


Install
=======

Install 

   ```
    Create a virtualenv. 
    ## mkvirtualenv passwordless_drf
   ```
   ```
    Clone the Repo.
    ### git clone https://github.com/Ngahu/Passwordless-Django-Rest-Framework.git
   ```
   ```
    pip install requirements.txt
   ```




And run
```bash
python manage.py migrate
```



Start the Server
```bash
python manage.py runserver
```
