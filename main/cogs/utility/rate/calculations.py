
async def get_faculty_summary(ratings_for_faculty, total_records, total_student_count, blacklisted_count,previous_rate):
    mean_rating = sum(ratings_for_faculty) / total_records

    standard_deviation = (
        sum([(rating - mean_rating) ** 2 for rating in ratings_for_faculty]) / total_records
    ) ** 0.5
    return {
        "not_rated_before": False,
        "standard_deviation": standard_deviation,
        "mean": mean_rating,
        "total_students": total_student_count,
        "blacklisted_count": blacklisted_count,
        "previous_rate": int(previous_rate) if previous_rate else 0,
    }