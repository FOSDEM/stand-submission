class ReviewTable {

    constructor() {
        this.table = document.querySelector('#review-table');
        this.body = this.table.querySelector('tbody');
        let cls = this;
        fetch('/review/api/submissions')
            .then(function (response) {
                if (!response.ok) {
                    response.text().then(function (msg) {
                        cls._error(parent, msg);
                    });
                } else {
                    response.json().then(function (results) {
                        for (let i = 0; i < results['results'].length; i++) {
                            let submission = results['results'][i];
                            let tr = document.createElement('tr');
                            // Project
                            tr.appendChild(cls._td(submission['project']));
                            // Description
                            tr.appendChild(cls._td(submission['description']));
                            // Justification
                            tr.appendChild(cls._td(submission['justification']));
                            // Review
                            let td_review = document.createElement('td');
                            tr.appendChild(td_review);
                            cls.my_review(td_review, submission['id']);
                            // Score
                            let td_score = document.createElement('td');
                            tr.appendChild(td_score);
                            cls.my_score(td_score, submission['id']);
                            // Total score
                            let td_scores = document.createElement('td');
                            tr.appendChild(td_scores);
                            cls.scores(td_scores, submission['id']);
                            // Accepted
                            let td_decision = document.createElement('td');
                            tr.appendChild(td_decision);
                            cls.decision(td_decision, submission['id']);
                            // More details
                            tr.appendChild(cls._td('Link'));
                            cls.body.appendChild(tr);
                        }
                    });
                }
            });
        this.table.addEventListener('change', function (event) {
            cls._submit(event.target);
        });
    }

    scores(parent, submission_id) {
        let cls = this;
        fetch('/review/api/review/submission/' + submission_id + '/review')
            .then(function (response) {
                if (!response.ok) {
                    response.text().then(function (msg) {
                        cls._error(parent, msg);
                    });
                } else {
                    response.json().then(function (results) {
                        let score = 0;
                        for (let i = 0; i < results['results'].length; i++) {
                            score = score + results['results'][i]['score'];
                        }
                        parent.textContent = score;
                    });
                }
            });
    }

    my_review(parent, submission_id) {
        let cls = this;
        fetch('/review/api/review/submission/' + submission_id + '/review?mine=true')
            .then(function (response) {
                if (!response.ok) {
                    response.text().then(function (msg) {
                        cls._error(parent, msg);
                    });
                } else {
                    response.json().then(function (results) {
                        // Comments
                        let comments_i = parent.querySelector('textarea');
                        if (comments_i === undefined || comments_i === null) {
                            // Comments
                            let f = cls._review_form(submission_id);
                            parent.appendChild(f);
                            comments_i = parent.querySelector('textarea');
                        }
                        comments_i.setAttribute('data-submission-id', submission_id);
                        if (results['total'] === 0) {
                            comments_i.setAttribute('placeholder', 'Any notes for your review.');
                        } else {
                            comments_i.textContent = results['results'][0]['comments'];
                            comments_i.setAttribute('data-review-id', results['results'][0]['id']);
                        }
                    });
                }
            });
    }

    _review_form(submission_id) {
        let f = document.createElement('form');
        f.setAttribute('class', 'form-inline');
        let comments_l = document.createElement('label');
        comments_l.setAttribute('class', 'sr-only');
        comments_l.setAttribute('for', submission_id + '-my-review-comment');
        comments_l.textContent = 'Review';
        let comments_i = document.createElement('textarea');
        comments_i.setAttribute('class', 'form-control');
        comments_i.setAttribute('id', submission_id + '-my-review-comment');
        f.appendChild(comments_l);
        f.appendChild(comments_i);
        return f;
    }

    my_score(parent, submission_id) {
        let cls = this;
        fetch('/review/api/review/submission/' + submission_id + '/review?mine=true')
            .then(function (response) {
                if (!response.ok) {
                    response.text().then(function (msg) {
                        cls._error(parent, msg);
                    });
                } else {
                    response.json().then(function (results) {
                        // Score
                        let score_i = parent.querySelector('input');
                        if (score_i === undefined || score_i === null) {
                            let f = cls._score_form(submission_id);
                            parent.appendChild(f);
                            score_i = parent.querySelector('input');
                        }
                        score_i.setAttribute('data-submission-id', submission_id);
                        if (results['total'] === 0) {
                            score_i.setAttribute('placeholder', '0');
                            score_i.setAttribute('value', '0');
                        } else {
                            score_i.setAttribute('value', results['results'][0]['score']);
                            score_i.setAttribute('data-review-id', results['results'][0]['id']);
                        }
                    });
                }
            });
    }

    _score_form(submission_id) {
        let f = document.createElement('form');
        f.setAttribute('class', 'form-inline');
        let score_l = document.createElement('label');
        score_l.setAttribute('class', 'sr-only');
        score_l.setAttribute('for', submission_id + '-my-review-score');
        score_l.textContent = 'Score';
        let score_i = document.createElement('input');
        score_i.setAttribute('type', 'numeric');
        score_i.setAttribute('class', 'form-control');
        score_i.setAttribute('id', submission_id + '-my-review-score');

        f.appendChild(score_l);
        f.appendChild(score_i);
        return f;
    }

    decision(parent, submission_id) {
        let cls = this;
        fetch('/review/api/decision/submission/' + submission_id + '/decision')
            .then(function (response) {
                if (!response.ok) {
                    response.text().then(function (msg) {
                        cls._error(parent, msg);
                    });
                } else {
                    response.json().then(function (decision) {
                        let decision_i = parent.querySelector('input');
                        if (decision_i === undefined || decision_i === null) {
                            let f = document.createElement('form');
                            f.setAttribute('class', 'form-inline');
                            parent.appendChild(f);
                            let d = document.createElement('div');
                            d.setAttribute('class', 'form-check form-check-inline');
                            decision_i = document.createElement('input');
                            decision_i.setAttribute('type', 'checkbox');
                            decision_i.setAttribute('id', submission_id + '-decision');
                            decision_i.setAttribute('class', 'form-check-input');
                            let label = document.createElement('label');
                            label.setAttribute('class', 'sr-only');
                            label.setAttribute('for', submission_id + '-decision');
                            label.textContent = 'Accept or not?';
                            f.appendChild(label);
                            f.appendChild(decision_i);
                        }
                        decision_i.setAttribute('data-submission-id', submission_id);
                        decision_i.setAttribute('data-type', 'decision');
                        decision_i.value = decision['accepted'];
                    });
                }
            });
    }

    _submit(input) {
        let cls = this;
        let url = '/review/api/review/submission/' + input.getAttribute('data-submission-id') + '/review/';
        let data = {
            'comments': '',
            'score': ''
        };
        if (input.hasAttribute('data-review-id')) {
            url = url + input.getAttribute('data-review-id');
        }
        fetch(url, {
            method: 'POST'
        })
            .then(function(response) {
                if (!response.ok) {
                    response.text().then(function (msg) {
                        cls._error(parent, msg);
                    });
                } else {
                    response.json().then(function(response) {});
                }
            })
    }

    _error(parent, msg) {
        let d = parent.querySelector('.alert');
        if (d === undefined || d === null) {
            d = document.createElement('div');
            d.setAttribute('class', 'alert alert-danger');
            parent.appendChild(d);
        }
        d.textContent = msg;
    }

    _td(content) {
        let td = document.createElement('td');
        if (content instanceof Element) {
            td.appendChild(content);
        } else {
            td.textContent = content;
        }
        return td;
    }

}

$(document).ready(function () {
    let table = new ReviewTable();
});
