(function($){
    $(document).ready(function(){
        console.log('Setting up sql_query id');
        // Find all textareas with class "sql-textarea" on the page
        var sqlTextareas = $('#id_sql_query');

        // Initialize CodeMirror for each found textarea
        sqlTextareas.each(function () {
            CodeMirror.fromTextArea(this, {
                mode: "text/x-pgsql",  // Set SQL mode
                lineNumbers: true,     // Show line numbers
                theme: "darcula",      // You can change the theme if desired
            });
        });
    });
})(django.jQuery);