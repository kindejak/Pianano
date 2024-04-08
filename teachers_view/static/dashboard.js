Chart.defaults.color = '#fff';

$(function() {

    // request data from the server for students-xp
    var data0
    var labels_array0 = []
    var data_array0 = []
    data0 = $.ajax({
        url: '/api/students-xp/',
        method: 'GET',
        success: function(data) {
            console.log(data);
            for (var i = 0; i < data.length; i++) {
                labels_array0.push(data[i].student);
                data_array0.push(data[i].xp);
            }
            ctx = document.getElementById('lineChart').getContext('2d');
            new Chart (ctx, {
                type: 'bar',
                data: {
                    labels: labels_array0,
                    datasets: [{
                        label: 'XP',
                        data: data_array0,
                        borderWidth: 1,
                        backgroundColor: '#FFB1C1',
                    }]
                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    },
                    ticks: {
                        stepSize: 10
                    }
                }
            });

        }
    });
    var data1
    var labels_array1 = []
    var data_array1 = []
    // request data from the server for students-lessons-finished
    data1 = $.ajax({
        url: '/api/students-lessons-finished/',
        method: 'GET',
        success: function(data) {
            for (var i = 0; i < data.length; i++) {
                labels_array1.push(data[i].student);
                data_array1.push(data[i].lessons_finished);
            }
            ctx = document.getElementById('barChart').getContext('2d');
            new Chart (ctx, {
                type: 'bar',
                data: {
                    labels: labels_array1,
                    datasets: [{
                        label: 'Number of solved lessons',
                        data: data_array1,
                        borderWidth: 1
                    }]
                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    },
                    ticks: {
                        stepSize: 1
                    }
                }
            });

        }
    });
});



var $table = $('#table')
$(function() {
    $.ajax({
        url: '/api/students-from-teacher/',
        method: 'GET',
        success: function(data) {
            console.log(data);
            table_data = data;
            $table.bootstrapTable({data: table_data})
        }
    });
});