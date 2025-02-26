var filters = {}; // column:[value]

let isValidHttpUrl = function(string){
    let url;
    try{
        url = new URL(string);
    }catch (_){
        return false;
    }
    return url.protocol === "http:" || url.protocol === "https:";
}

let filters_count_shown = function(){
    var shown = 0
    $.each($('tbody tr'), function(){
        if($(this).is(":visible")){
            shown++;
        }
    });
    return shown;
}

let filters2string = function(){
    var eruit = ''
    for(key in filters){
        eruit += '<strong>'+key+'</strong> = '+filters[key].toString()+'<br>'
    }
    return eruit.replaceAll(',', ', ');
}

let add_2_filter = function(td_o, empty) {
    let key = td_o.attr('data-th');
    if(td_o.attr('id') == '') {
        // checkbox, ignore
        return;
    }
    if(empty){
        filters = {}
    }
    if (filters.hasOwnProperty(key)) {
        if (!filters[key].includes(td_o.text())) {
            filters[key].push(td_o.text())
        }
    } else {
        filters[key] = [td_o.text()]
    }
}

let filteren = function(){
    $('tbody tr').hide();
    $('tbody td').removeClass('filteredcel')
    $.each($('tbody tr'), function(){
        let rij = $(this);
        var tonen = true;
        for(var key in filters){
            // ignore checkbox value
            if(key == 'checked'){
                continue;
            }
            let cel = rij.find('td[data-th="'+key+'"]'); // cel met te filteren kolom
            if(filters[key].includes(cel.text())){
                cel.addClass('filteredcel')
            }else{
                tonen = tonen && false;
            }
        }
        if(tonen){
            rij.show();
        }
    });
    $('td input[type="checkbox"]:checked').parent().parent().show();
}

let zeropad = function(num, size) {
    num = num.toString();
    while (num.length < size) num = "0" + num;
    return num;
}

let sortTable = function(td_nr, order) {
    let table = $('table')
    let asc = order === 'asc';
    let tbody = table.find('tbody');
    // get column head:
    let thname = table.find('thead th:nth-child('+td_nr+')').text().trim().replaceAll("↓", "").replaceAll("↑", "");
    tbody.find('tr').sort(function (a, b) {
        var vala = $('td:nth-child(' + td_nr + ')', a).attr('data-csv');
        var valb = $('td:nth-child(' + td_nr + ')', b).attr('data-csv');
        // numeric fields sortable as text
        if(['id', 'grade', 'ecs', 'year'].includes(thname)){
            vala = zeropad(vala, 10);
            valb = zeropad(valb, 10);
        }
        if (asc) {
            return vala.localeCompare(valb);
        } else {
            return valb.localeCompare(vala);
        }
    }).appendTo(tbody);
}

let tabel2csv = function(header) {
    // Select rows from table_id
    var csvtext = '';
    if (header) {
        var eerste = true;
        var komma = '';
        $.each($('thead th'), function () {
            if (eerste) {
                // skip checkbox field
                eerste = false;
            } else {
                $(this).find('span').html(''); // pijltje eruit
                csvtext += komma + $(this).text();
                komma = ';';
            }
        });
        csvtext += "\n";
    }

    var nietnul = false;
    $.each($('tbody tr'), function () {
        let rij = $(this);
        let checked = $(this).find('td input[name="add"]').prop('checked');
        if (rij.is(":visible") && checked) {
            var eerste = true;
            komma = '';
            $.each(rij.find('td'), function () {
                if (eerste) {
                    // skip checkbox field
                    eerste = false;
                } else {
                    nietnul = true;
                    let t = $(this).data('csv');
                    if($(this).hasClass('circular')){
                        console.log($(this).data('cirval'))
                        if(t === 0){
                            csvtext += komma + '';
                        }else if(t === 1){
                            csvtext += komma + 'green';
                        }else if(t === 2){
                            csvtext += komma + 'orange';
                        }else if(t === 3){
                            csvtext += komma + 'red';
                        }
                    }else{
                        csvtext += komma + t;
                    }
                    komma = ';';
                }
            })
            csvtext += "\n";
        }
    });
    if(nietnul){
        $('#csv-area').val(csvtext);
        return true;
    }else{
        return false;
    }
}

let click_to_group = function(){
    // maakt groep-vak rechtsklik-baar als student actief.
    let acts = {{ actiefstats|safe }}
    $.each($('tbody tr'), function(){
        let status = $(this).attr('data-status')*1;
        let filter = $(this).attr('data-filter');
        if(acts.includes(status) || true) {
            $(this).find('td[data-th="s_group"]')
                .on('contextmenu', function (e) {
                    e.preventDefault();
                    window.location.replace('/groepen/' + $(this).attr('data-idnr'));
                });
        }else{
            $(this).find('td')
                .on('contextmenu', function (e) {
                    e.preventDefault();
                });
        }
    })
}

let get_checked_ids = function(){
    var lijst = [];
    $('td input[name="add"]:checked').each(function(){
        lijst.push($(this).val()*1);
    });
    return lijst;
}

let checked_emails = function(){
    var csv = ''
    $('td input[name="add"]:checked').closest('tr').each(function(){
        let id = $(this).attr('id') * 1;
        let em = $(this).find('td[data-th="email"]').text();
        csv += em + '\r\n';
    });
    $('#csv-area').val(csv);
}

let collectief_verzenden = function(){
    let lijst = get_checked_ids();
    if(lijst.length == 0){
        return false;
    }
    $('input[name="col-ids"]').val(lijst);

    let s_group = $('select[name="to-group"]').find(":selected").val();
    let s_stream = $('select[name="to-stream"]').find(":selected").val();
    let s_status = $('select[name="to-status"]').find(":selected").val();
    if(s_group == 0 && s_status == 0 && s_stream == 0){
        return false;
    }
    // verzenden
    return true;
}

let form_2_data = function(form_id){
    // get all form fields and change it into a dict object
    var data = {};
    $("#"+form_id).serializeArray().map(function(x){data[x.name] = x.value;});
    return data;
}

let yes_ajax_send = function(data, elem){
    $.post("/studenten/yes_ajax", data, function(result){
        yes_ajax_return(result['result'], elem);
    });
}

let ajax_sort = function(path, fieldname, direction){
    // does not wait for response
    var data = {'path': path, 'fieldname': fieldname, 'direction': direction}
    data = JSON.stringify(data)
    $.ajax({
        url: "/studenten/set_sort",
        type: "post",
        data: data,
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function () {
        },
    })

}

let ccolor = function(val){
    if(val === 1){
        return 'c-een';
    }else if(val === 2){
        return 'c-twee';
    }else if(val === 3){
        return 'c-drie';
    }else{
        return 'c-nul';
    }
}

let yes_ajax_return = function(value, elem) {
    if (value === false) {
        return;
    }
    console.log(value, elem);
    if($(elem).hasClass("do-asshole")){
        $(elem).removeClass('c-nul c-een c-twee c-drie').addClass(ccolor(value));
        $(elem).attr('data-csv', value);
        $(elem).attr('data-cirval', value);
    }else if($(elem).hasClass('custom')){
        $(elem).val(value)
        $(elem).attr('data-cusval', value);
        $(elem).attr('data-csv', value);
    }else if($(elem).hasClass('circular')){
        $(elem).removeClass('c-nul c-een c-twee c-drie').addClass(ccolor(value));
        $(elem).attr('data-cirval', value);
        $(elem).attr('data-csv', value);
    }else if($(elem).find('input[name="grade"]')){
        $(elem).parent().removeClass('grade-not grade-failed grade-passed');
        if(value >= 10 && value < 55){
            $(elem).parent().addClass('grade-failed');
        }else if(value >= 55){
            $(elem).parent().addClass('grade-passed');
        }else{
            $(elem).parent().addClass('grade-not');
        }
    }
}

let sort_on_load = function(){
    // sorteer adhv props
    const urlParams = new URLSearchParams(window.location.search);
    var sortfield = urlParams.get('sort-field');
    var sortdir = urlParams.get('sort-dir');
    let sorteer = {{ props.get_sort(sortpath) }};
    if(sortfield && sortdir){
        // given bij url args
    }else if(sorteer.length == 3){
        // then check stuff from props
        try{
            sortfield = sorteer[1];
            sortdir = sorteer[2];
        }catch (e){
            sortfield = null;
            sortdir = null;
        }
    }else{
        sortfield = "firstname";
        sortdir = "asc";
    }
    // now sort
    $.each($('table thead th'), function(k, v){
        if($(v).attr("id") == sortfield){
            sortTable(k+1, sortdir);
            if(sortdir === 'desc') {
                $(v).find("span").html('↑');
            }else{
                $(v).find("span").html('↓');
            }
            return;
        }
    });
}

$(function(){
    $('button[name="tocsv"]').on('click', function(){
        tabel2excel();
    })

    // sort on column
    $('table thead th:not(.no-sort)').on('click', function(){
        let th = $(this);
        var i = 0;
        var richting = 'asc';
        $.each($('table thead th'), function(k, v){
            i++;
            if($(this).attr('id') == th.attr('id')){
                // get asc/desc
                if($(this).find('span').text() == String.fromCharCode(8593)){
                    // was up, goes down
                    richting = 'asc';
                }else if($(this).find('span').text() == String.fromCharCode(8595)){
                    // was down, goes up
                    richting = 'desc';
                }
                sortTable(i, richting)
            }
        });
        $('th span').html('');
        if(richting == 'asc'){
            th.find('span').html('&darr;');
        }else{
            th.find('span').html('&uarr;');
        }

        $('#no-ajax input[name="sort-field"]' ).val(th.attr('id'));
        $('#no-ajax input[name="sort-dir"]' ).val(richting);
        $('#asshole input[name="sort-field"]' ).val(th.attr('id'));
        $('#asshole input[name="sort-dir"]' ).val(richting);
        let all_aas = $('a.must-sort');
        $.each(all_aas, function(k, v){
            var href = $(this).attr('href');
            href = href.split('?')[0];
            href = href+'?sort-field='+th.attr('id')+'&sort-dir='+richting;
            $(this).attr('href', href);
        })

        let path = window.location.pathname;
        let field = th.attr('id');
        if(field) {
            ajax_sort(path, field, richting)
        }
    });

    // checkboxes on and off
    $('th input[type="checkbox"]').on('change', function(){
        if($(this).is(':checked')){
            $('tr:visible td input[type="checkbox"]').prop('checked', true);
        }else{
            $('tr:visible td input[type="checkbox"]').prop('checked', false);
        }
    })

    // show-hide on cel value
    $('table td:not(.dblignore)').on('dblclick', function(){
        let td_o = $(this)
        // https://craftpip.github.io/jquery-confirm/
        $.confirm({
            columnClass: 'medium',
            containerFluid: true,
            title: 'Filters ['+filters_count_shown()+'] :',
            content: filters2string(),
            autoClose: 'cancel|8000',
            buttons: {
                cancel: {
                    text: 'Annuleer',
                    btnClass: 'btn-white',
                    keys: ['esc'],
                    action: function(){
                        // niets doen
                    }
                },
                reset_filter: {
                    text: 'Reset',
                    btnClass: 'btn-red',
                    keys: [],
                    action: function(){
                        filters = {}
                        $('tbody td').removeClass('filteredcel')
                        $('tbody tr').show();
                    }
                },
                new_filter: {
                    text: 'Nieuw & Go',
                    btnClass: 'btn-blue',
                    keys: [],
                    action: function(){
                        add_2_filter(td_o, true);
                        filteren();
                    }
                },
                add_to_filter: {
                    text: 'Voeg toe',
                    btnClass: 'btn-orange',
                    keys: [],
                    action: function(){
                        add_2_filter(td_o, false)
                    }
                },
                add_to_go_filter: {
                    text: 'Voeg toe & Go',
                    btnClass: 'btn-blue',
                    keys: ['enter'],
                    action: function(){
                        add_2_filter(td_o, false)
                        filteren();
                    }
                },
                go_filter: {
                    text: 'Go',
                    btnClass: 'btn-blue',
                    keys: ['enter'],
                    action: function(){
                        filteren();
                    }
                }
            },
            onDestroy: function(){
                // niets
            },
        });
    })

    // disable context menu on tables
    $('td, th')
        .on('contextmenu', function(e){
            e.preventDefault();
        })

    // contrasteren tekst in cellen en .contrast class
    $('td, .contrast')
        .each(function(){
            let kleur = $(this).css('background-color');
            let contra = calc_contra_color(kleur)
            $(this).css('color', contra);
        });

    // als op collectief geklikt
    $('form[name="to-collectief"]').on('submit', function(e){
        // alle aangevinkte id's naar veld col-ids
        if(! collectief_verzenden()){
            e.preventDefault();
        }
    });

    $('input[name="to-emails"]').on('click', function(e){
        e.preventDefault();
        checked_emails();
    });

    $('input[name="to-csv"]').on('click', function(e) {
        e.preventDefault();
        tabel2csv(header=true)
    });

    $('input[name="to-excel"]').on('click', function(e) {
        if( tabel2csv(header=true) ){
            // submit form
        }else{
            e.preventDefault();
        }
        // download_excel();
    });

    $('#csv-area').css('width', $('table').width());

    // input portfolio url
    $('input[name="pf_url"]').on('keypress', function(e){
        var deze = $(this);
        var keycode = (e.keyCode ? e.keyCode : e.which);
        if(keycode == 13){
            let pfu = $(this).val();
            if(!isValidHttpUrl(pfu) && pfu !== ''){
                $(this).val('')
                return;
            }
            $('#no-ajax input[name="field-name"]').val('pf_url');
            $('#no-ajax input[name="what"]').val('portfolio');
            $('#no-ajax input[name="field-value"]').val(pfu);
            let id = $(this).closest('tr').attr('id')*1;
            $('#no-ajax input[name="student-id"]').val(id)
            let viewid = $(this).closest('tr').attr('data-viewid')*1;
            $('#no-ajax input[name="view-id"]').val(viewid);
            data = form_2_data('no-ajax');
            yes_ajax_send(data, deze)
        }
    });

    // input grade
    $('input[name="grade"]').on('keypress', function(e){
        var deze = $(this);
        var keycode = (e.keyCode ? e.keyCode : e.which);
        if(keycode == 13){
            let grade = $(this).val()*1;
            if(grade < 0 || grade > 90){
                $(this).val('').addClass('valop');
                return;
            }
            $('#no-ajax input[name="field-name"]').val('grade');
            $('#no-ajax input[name="what"]').val('grade');
            $('#no-ajax input[name="field-value"]').val(grade);
            let id = $(this).closest('tr').attr('id')*1;
            $('#no-ajax input[name="student-id"]').val(id)
            let viewid = $(this).closest('tr').attr('data-viewid')*1;
            $('#no-ajax input[name="view-id"]').val(viewid);
            data = form_2_data('no-ajax');
            yes_ajax_send(data, deze)
        }
    });

    // input custom field
    $('td.custom input').on('keypress',function(e) {
        var deze = $(this);
        if(e.which === 13){
            let id = $(this).closest('tr').attr('id')*1;
            let cusval = $(this).val().trim();
            let cusname =$(this).prop('name');
            $('#no-ajax input[name="student-id"]').val(id)
            $('#no-ajax input[name="field-name"]').val(cusname);
            $('#no-ajax input[name="what"]').val('customs');
            $('#no-ajax input[name="field-value"]').val(cusval);
            let viewid = $(this).closest('tr').attr('data-viewid')*1;
            $('#no-ajax input[name="view-id"]').val(viewid);
            data = form_2_data('no-ajax');
            yes_ajax_send(data, deze)
        }
    });

    // click on circular field
    $('td.circular').on('click', function(){
        var deze = $(this);
        let id = $(this).closest('tr').attr('id')*1;
        let cirval = $(this).attr('data-cirval')*1;
        let cirname = $(this).attr('data-cirname');
        $('#no-ajax input[name="student-id"]').val(id)
        $('#no-ajax input[name="field-name"]').val(cirname);
        $('#no-ajax input[name="what"]').val('circulars');
        $('#no-ajax input[name="field-value"]').val(cirval);
        let viewid = $(this).closest('tr').attr('data-viewid')*1;
        $('#no-ajax input[name="view-id"]').val(viewid);
        data = form_2_data('no-ajax');
        yes_ajax_send(data, deze)
    });

    // doubel click is empty circular field
    $('td.circular').on('contextmenu', function(){
        var deze = $(this);
        var cirval = $(this).attr('data-cirval')*1;
        if(cirval < 1){
            return;
        }
        let id = $(this).closest('tr').attr('id')*1;
        let cirname = $(this).attr('data-cirname');
        let viewid = $(this).closest('tr').attr('data-viewid')*1;
        $('#no-ajax input[name="view-id"]').val(viewid);
        $('#no-ajax input[name="student-id"]').val(id)
        $('#no-ajax input[name="field-name"]').val(cirname);
        $('#no-ajax input[name="what"]').val('circulars');
        $('#no-ajax input[name="field-value"]').val(3);
        data = form_2_data('no-ajax');
        yes_ajax_send(data, deze)
    });

    // toggle cumlaude, asshole or no assessment
    $('td.do-asshole').on('click', function(){
        var deze = $(this);
        let id = $(this).closest('tr').attr('id')*1;
        let curval = $(this).attr('data-csv')*1;
        let viewid = $(this).closest('tr').attr('data-viewid')*1;
        $('#no-ajax input[name="view-id"]').val(viewid);
        $('#no-ajax input[name="student-id"]').val(id)
        $('#no-ajax input[name="field-name"]').val("do-asshole");
        $('#no-ajax input[name="what"]').val("do-asshole");
        $('#no-ajax input[name="field-value"]').val(curval);
        data = form_2_data('no-ajax');
        yes_ajax_send(data, deze)
    })

    $('a.idbutton').on('contextmenu', function(e) {
        let id = $(this).closest('tr').attr('id');
        window.location.replace("/studenten/opendir/" + id);
    });

    sort_on_load();

    click_to_group();
});