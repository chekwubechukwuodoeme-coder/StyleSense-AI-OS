from database.database import conn, cursor

def create_user(name, email, password, role, country):

    try:

        cursor.execute(
            """
            INSERT INTO users
            (name,email,password,role,country)

            VALUES (?,?,?,?,?)
            """,

            (
                name,
                email,
                password,
                role,
                country
            )
        )

        conn.commit()

        return True

    except:

        return False


def login(email, password):

    cursor.execute(

        """
        SELECT * FROM users

        WHERE email=?

        AND password=?
        """,

        (
            email,
            password
        )
    )

    return cursor.fetchone()