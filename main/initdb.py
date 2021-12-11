import sqlite3

# from discord.ext import commands


def create_database():
    cursor = sqlite3.connect("Storage.db")

    cursor.execute(
        """CREATE TABLE common_keys(
        key VARCHAR unique,
        value VARCHAR)"""
    )

    cursor.execute(
        """CREATE TABLE guilds_info(
        guild_id varchar unique,
        logs_channel_id varchar,
        deleted_messages_channel_id varchar,
        prefix varchar default "ka!",
        admin_role_id varchar,
        moderator_role_id varchar
        )"""
    )

    cursor.execute(
        """CREATE TABLE schedule_data(
        client_id varchar,
        course_code varchar,
        course_name varchar,
        course_type varchar,
        course_id varchar,
        slot varchar,
        venue varchar,
        faculty_name varchar,
        faculty_school varchar,
        semester_id varchar,
        semester_name varchar,
        embedded_courses int
    )
    """
    )

    cursor.execute(
        """CREATE TABLE client_info(
        client_id varchar UNIQUE,
        campus varchar,
        email varchar,
        stream varchar,
        full_course_name varchar,
        full_name varchar,
        reg_no varchar
    )
    """
    )

    cursor.execute(
        """CREATE TABLE current_semester(
            client_id varchar,
            semester_id varchar,
            semester_name varchar
        )
        """
    )

    cursor.execute(
        """CREATE TABLE vote_notify(
            client_id varchar,
            last_voted varchar,
            last_notified varchar,
            notified varchar default "no"
        )
        """
    )

    cursor.execute(
        """CREATE TABLE guild_client_info(
        client_id varchar UNIQUE
        )
        """
    )

    cursor.execute(
        """CREATE TABLE client_faculty_rate(
        faculty_name varchar,
        client_id varchar,
        semester_id varchar,
        rating int,
        blacklisted varchar,
        day_voted date
        )
        """
    )

    cursor.execute(
        """CREATE TABLE schedule_display_data(
        client_id varchar,
        course_details json,
        schedule_details json,
        semester_id varchar,
        semester_name varchar,
        full_name varchar
        )
        """
    )
    
    cursor.commit()
    return cursor
