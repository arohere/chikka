import sqlite3

from discord.ext import commands

def create_database():
    cursor = sqlite3.connect("Storage.db")

    cursor.execute("""CREATE TABLE common_keys(
        key VARCHAR unique,
        value VARCHAR)""")

    cursor.execute("""CREATE TABLE guilds_info(
        guild_id varchar unique,
        logs_channel_id varchar,
        deleted_messages_channel_id varchar,
        prefix varchar default "ka!",
        admin_role_id varchar,
        moderator_role_id varchar
        )""") 

    cursor.execute("""CREATE TABLE schedule_data(
        client_id varchar,
        course_code varchar,
        course_name varchar,
        course_id varchar,
        slot varchar,
        venue varchar,
        faulty_name varchar,
        faculty_school varchar,
        semester_id varchar,
        semester_name varchar
    )
    """)

    cursor.execute("""CREATE TABLE client_info(
        client_id varchar UNIQUE,
        school varchar,
        full_course_name varchar,
        full_name varchar,
        reg_no varchar
    )
    """)


    cursor.commit()
    return cursor

