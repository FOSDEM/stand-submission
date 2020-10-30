export class ReviewTable {

    constructor() {
        this.table = document.querySelector('#review-table');
        this.table_jq = $('#review-table');
        this.table_dt = null;
        let cls = this;
        this.table.addEventListener('change', function (event) {
            cls._submit(event.target);
        });
    }

    init() {
        this.table_dt = this.table_jq.DataTable({
            ajax: {
                url: '/review/api/submissions'
            }
        });
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
                    response.json().then(function(results) {
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
                    response.json().then(function(results) {
                        // Comments
                        // Score
                    });
                }
            });
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