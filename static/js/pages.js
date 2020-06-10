$(document).ready(function () {

    var csrftoken = document.getElementById("csrf_token").value;

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken)
            }
        }
    })

    var page_elements_dialog = $("#page-element-overview-dialog").dialog({
        buttons: [
            {
                text: "schließen",
                click: function () {
                    $(this).dialog("close");
                }
            }
        ]
    });

    page_elements_dialog.dialog("close");

    $('.button-add-page-element').bind("click touch", function () {
        page_elements_dialog.dialog("open");
    });

    $('.button-display-tab-content').bind("click touch", function () {
        $(this).toggleClass('clicked');

        if ($(this).hasClass('clicked')) {
            $(this).parent('.tab').children('.form-group').addClass('hidden');
            $(this).html('<span class="oi oi-arrow-thick-bottom"></span>Inhalt einblenden');
        } else {
            $(this).parent('.tab').children('.form-group').removeClass('hidden');
            $(this).html('<span class="oi oi-arrow-thick-top"></span>Inhalt ausblenden');
        }

    });

    $('.page-element-item').bind("click touch", function () {

        $.ajax({
            url: "/backend/ajax/page_element_create",
            method: "POST",
            credentials: true,
            data: {eid: $(this).attr("eid"), page_id: $('#id').val()},
            success: function (response) {
                if (response.success === true) {
                    $('#page-elements').append(response.html);
                } else {
                    alert("Seitenelement konnte nicht erstellt werden");
                }
            },
            error: function (error) {
                alert(error);
            }
        });

    });

});