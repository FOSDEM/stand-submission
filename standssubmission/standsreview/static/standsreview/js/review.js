import {ReviewTable} from "./review/table.js";


document.addEventListener('DOMContentLoaded', function() {
    let table = new ReviewTable();
    let dt = $('#review-table').DataTables(table.options());
});
