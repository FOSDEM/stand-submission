document.addEventListener('DOMContentLoaded', function() {
    $('#result_list').DataTable({
        'buttons': ['csv', 'excel']
    });
});