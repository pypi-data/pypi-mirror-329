Construct SQL commands and queries using Python classes.

```python

from sqlclasses import sql

login = "me"
password = "secret"

query = sql.select( ("firstname", "lastname", "login",),
                    ("users",),
                    sql.where("login = ", sql.string_literal(login),
                              " AND ",
                              "password = ", sql.string_literal(password)) )

print(repr(query))

# >> select: <SELECT firstname, lastname, login FROM users WHERE login = 'me' AND password = 'secret'>

```

This used to be at the core of my Object Ralational Membrane years ago. I have ported it to Python 3 and re-publish it here. More documentation forthcomming. 
