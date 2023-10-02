# App
Start a [python virtual environment](https://docs.python.org/3/tutorial/venv.html).

Install dependencies:
```
pip install -r requirments.txt
```

Run the application using:
```
flask --app flaskr run --debug
```
Requires an AD service to be running. You can use [AD docker](#ad-docker) as an example.


# Config
If you require new config, create a config file in the [config dir](./config). Set the name of the file to the value
of the environment variable `APP_CONFIG_FILE`.

Uses a service account to connect to AD with LDAP simple bind.

# AD docker
https://hub.docker.com/r/bitnami/openldap/

```
docker run --rm --name openldap \
  --env LDAP_ADMIN_USERNAME=admin \
  --env LDAP_ADMIN_PASSWORD=adminpassword \
  --env LDAP_USERS=serviceuser,customuser,customuser2 \
  --env LDAP_PASSWORDS=servicepassword,custompassword,custompassword2\
  --publish 1389:1389 \
  bitnami/openldap:latest
  ```
