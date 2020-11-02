class ReviewTable {

    constructor() {
        this.table = document.querySelector('#review-table');
        let cls = this;
        this.table.addEventListener('change', function (event) {
            cls._submit(event.target);
        });
    }

    options() {
        let cls = this;
        return {
            ajax: {
                url: '/review/api/submissions',
                dataSrc: 'results'
            },
            paging: false,
            order: [
                [0, 'asc']
            ],
            columnDefs: [
                {
                    // My review
                    render: function (data, type, row) {
                        return cls._review_form(data).outerHTML;
                    },
                    targets: 3
                },
                {
                    // My score
                    render: function (data, type, row) {
                        return cls._score_form(data).outerHTML;
                    },
                    targets: 4
                },
                {
                    // Total score
                    render: function (data, type, row) {
                        return '0';
                    },
                    targets: 5
                },
                {
                    // Accepted
                    render: function (data, type, row) {
                        return '';
                    },
                    targets: 6
                },
                {
                    // More details
                    render: function (data, type, row) {
                        return '';
                    },
                    targets: 7
                }
            ],
            columns: [
                {data: 'project'},
                {data: 'description'},
                {data: 'justification'},
                {data: 'id'},
                {data: 'id'},
                {data: 'id'},
                {data: 'id'},
                {data: 'id'}
            ]
        };
    }

    reviews(parent, submission_id) {
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
                        if (comments_i === undefined) {
                            // Comments
                            let f = cls._review_form(submission_id);
                            parent.appendChild(f);
                            comments_i = parent.querySelector('textarea');
                        }
                        if (results['length'] === 0) {
                            comments_i.setAttribute('placeholder', 'Any notes for your review.');
                        } else {
                            comments_i.setAttribute('value', results['results'][0]['comments']);
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
                        if (score_i === undefined) {
                            let f = cls._score_form(submission_id);
                            parent.appendChild(f);
                            score_i = parent.querySelector('textarea');
                        }
                        if (results['length'] === 0) {
                            score_i.setAttribute('placeholder', '0');
                            score_i.setAttribute('value', '0');
                        } else {
                            score_i.setAttribute('value', results['results'][0]['score']);
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
                        if (decision_i === undefined) {
                            let f = document.createElement('form');
                            f.setAttribute('class', 'form-inline');
                            parent.appendChild(f);
                            let d = document.createElement('div');
                            d.setAttribute('class', 'form-check form-check-inline');
                            let decision_i = document.createElement('input');
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
        console.log(input);
    }

    _error(parent, msg) {
        let d = parent.querySelector('.alert');
        if (d === undefined) {
            d = document.createElement('div');
            d.setAttribute('class', 'alert alert-danger');
            parent.appendChild(d);
        }
        d.textContent = msg;
    }

}

$(document).ready( function () {
    let table = new ReviewTable();
    let dt = $('#review-table');
    console.log(dt);
    dt.DataTable(table.options());
});
