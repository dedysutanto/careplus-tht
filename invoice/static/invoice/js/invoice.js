$(document).ready(function() {
    if ($('#id_is_final').is(":checked")) {

        $('input').each(
            function (index) {
                let input = $(this);
                input.prop('readonly', true);
                //input.prop("readonly",true);
            });

        $('#id_related_invoice-ADD').hide();
        $('option:not(:selected)').remove();
        $('#id_is_final').prop('disabled', true).prop('name', '');
        let elem = $('div').find('[data-contentpath="is_final"]');
        elem.append('<input id="id_is_final" type="hidden" name="is_final" value="true">');

        //console.log($('div').find('[data-contentpath="is_final"]'));
        if ($('#id_is_cancel').is(":checked")) {
            $('#id_is_cancel').prop('disabled', true).prop('name', '');
            $('div').find('[data-contentpath="is_final"]').append('<input id="id_is_cancel" type="hidden" name="is_cancel" value="true">')
        }
    }
    else {
        $('#id_is_cancel').prop('disabled', true);
    }
    //$('input[name="csrfmiddlewaretoken"]').prop('readonly', false);

});