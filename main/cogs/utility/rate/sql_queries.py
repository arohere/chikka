from datetime import datetime, timedelta



async def fetch_yet_to_notify(cursor):
    return cursor.execute(
            """SELECT client_id FROM vote_notify
            WHERE (last_voted is not NULL and last_voted < ?) and (last_notified is NULL or last_notified < last_voted)
            """,
            # (datetime.now() - timedelta(days=31),),
            (datetime.now() - timedelta(minutes=1),),
        ).fetchall()
    
async def fetch_yet_to_notify_again(cursor):
    return cursor.execute(  # add already notified bool
            """SELECT client_id, last_voted, last_notified FROM vote_notify
            WHERE (last_notified is not NULL and last_notified < ?) and notified == "no"
            """,
            # (datetime.now() - timedelta(days=14),),
            (datetime.now() - timedelta(minutes=1),),
        ).fetchall()

async def update_last_notify(cursor,client_id):
    cursor.execute(
    f"""UPDATE vote_notify
    SET notified = "no", last_notified = ?
    WHERE client_id = '{client_id}'
    """,
    (datetime.now(),),
    )

async def update_last_notify_again(cursor,client_id):
    return cursor.execute(
        f"""UPDATE vote_notify
        SET notified = "yes", last_notified = ?
        WHERE client_id = '{client_id}'
        """,
        (datetime.now(),),
    )

async def fetch_current_semester(cursor,client_id):
    return cursor.execute(
        f"""SELECT semester_id FROM current_semester
        WHERE client_id = '{client_id}'
        """
    ).fetchone()[0]

async def previous_rated_data(cursor,client_id,current_semester):
    return cursor.execute(
        f"""SELECT * FROM client_faculty_rate
        WHERE client_id = '{client_id}' AND semester_id = '{current_semester}'
        """
    ).fetchall()
    
async def ratings_for_faculty(cursor, faculty_name):
    data = cursor.execute(
        f"""SELECT MAX(day_voted),rating FROM client_faculty_rate
        WHERE faculty_name = '{faculty_name}' and blacklisted is NULL and rating is not NULL
        GROUP BY client_id
        """
    ).fetchall()
    return [int(b[1]) for b in data]

async def blacklisted_count_for_faculty(cursor, faculty_name):
    return cursor.execute(
        f"""SELECT count(*) FROM client_faculty_rate
        WHERE faculty_name = '{faculty_name}' and blacklisted = "yes"
        """
    ).fetchone()[0]

async def total_students_for_faculty(cursor, faculty_name):
    return cursor.execute(
        f"""SELECT count(DISTINCT client_id) FROM client_faculty_rate
        WHERE faculty_name = '{faculty_name}' and rating is not NULL
        """
    ).fetchone()[0]

async def update_blacklist_rating(cursor,client_id,current_semester,faculty_name):
    cursor.execute(
        f"""UPDATE client_faculty_rate
    SET rating = 0, blacklisted = 'yes'
    WHERE client_id = '{client_id}' AND semester_id = '{current_semester}' AND faculty_name = '{faculty_name}'
    """
    )

async def update_rating(cursor,client_id,current_semester,faculty_name,rating_data):
    cursor.execute(
        f"""UPDATE client_faculty_rate
    SET rating = {rating_data[faculty_name]}, blacklisted = NULL
    WHERE client_id = '{client_id}' AND semester_id = '{current_semester}' AND faculty_name = '{faculty_name}'
    """
    )

async def update_voted_date(cursor,client_id):
    cursor.execute(
        f"""UPDATE vote_notify
        SET last_voted = ?, last_notified = NULL, notified = "no"
        WHERE client_id == '{client_id}'
        """,
        (datetime.now(),),
    )