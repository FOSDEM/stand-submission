

def format_review(review):
    formatted = {
        'project': review.submission.project.name,
        'submission': review.submission.__str__(),
        'reviewer': None,
        'comments': review.comments,
        'score': review.score
    }
    if review.reviewer.first_name and review.reviewer.last_name:
        formatted['reviewer'] = '{0} {1}'.format(review.reviewer.first_name, review.reviewer.last_name)
    else:
        formatted['reviewer'] = review.reviewer.username
    return formatted
