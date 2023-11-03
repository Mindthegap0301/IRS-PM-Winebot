[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

## Welcome

<hr>

### Environment file

1. Copy `.env.example` file to your project root folder and rename it to `.env`.
2. Fill in the values for each environment variable in the `.env` file.

### Quick Start

1. You should have `python 3.10` and `poetry` installed. If not, install it gloabally with `pip install poetry`.
2. Install the dependencies, and create a virtual environment with the following.

```shell
# install dependencies and create environment for python 3
$ poetry install
```

3. You can run the following command to switch to an environment (replace the User path and `app-env-name-python3.10` with your own environment name):

```shell
# show all poetry environments
$ poetry env list

# activate an environment
$ poetry env use [app-env-name-python3.10]
```

4. Alternatively, on Visual Studio Code, install the Python Environment Manager, which allows you to switch to the `upskill-backend` environment.

5. Create a copy of `.env.example` and rename the copied file to `.env`.

```shell
$ cp .env.example .env
```

6. [Optional] Uncomment and change the `SQLALCHEMY_DATABASE_URI` value in the `.env` file to your desired PostgreSQL database connection string, if you already have one. Otherwise, leave it commented and the app will set up an SQLite database.

7. Migrate the tables with the following command:

```shell
$ alembic upgrade head
```

8. Seed the tables with the following command:

```shell
$ flask seed run
```

9. Run the app with:

```shell
$ flask run
```

10. Navigate to [http://localhost:5000](http://localhost:5000)

## For Developers

### Database and Migrations on PostgreSQL Migrations

1. You must set up a PostgreSQL database before you can migrate.
2. Assign the PostgreSQL connection string to the environment variable `SQLALCHEMY_DATABASE_URI`. This variable should be in the `.env` file.

```
SQLALCHEMY_DATABASE_URI=postgres://username:password@localhost:5432/dbname
```

3. To run the migration files (for building the database tables), input the following command line.

```bash
alembic upgrade head
```

4. Run the seeder to fill the database with preliminary data.

```bash
flask seed run
```

### Note on new migrations

1. Do the following if you want to change the database schema, e.g. creating tables, adding / removing columns to tables:
   - Make the appropriate changes in the `app/models/` python files. Refer to the [SQLAlchemy documentation for creating models] (https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/)
   - Add the new model metadata to `app/models/__init__.py` file
   - Run the Alembic command to auto-generate migration file:

```bash
alembic revision --autogenerate -m "Add ____ table"
```

- Run the Alembic upgrade command.

```bash
alembic upgrade head
```

## Useful poetry notes

Set the current folder as the location for your virtual environment. This creates a `.venv` folder for your dependencies.

```bash
$ poetry config virtualenvs.in-project true
```

View the path of the current virtual environment with

```bash
$ poetry env info -p
```

Remove a virtual environment with

```bash
$ poetry env remove [app-env-name]
```

Use this command to view a virtual environment

```bash
$ poetry show -v
```

For convenience, you can go to Virtual Studio Code Preferences and set the variable `python.venvPath` to the path containing your virtual environments.
