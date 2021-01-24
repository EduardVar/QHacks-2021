const buyModal = "#buy-modal";
const updateModal = "#update-modal";
const serviceFee = 0.35;
const tax = 0.05;

function calculateCost(price, amount) {

    let costOfTickets = price * amount;
    return costOfTickets + (costOfTickets * tax) + (costOfTickets + serviceFee);
}

function SubmitForm(formid, location) {
    

    let el = $(`form#${formid}-ticket-form`);
    let data = el.serialize();

    if (location == "/update") {
        data += "&Ticket_Id=" + el.attr("data-ticket-id");
        console.log(data);
    }

    if (el.attr('method') == 'POST') $.post(location, data)
        .done(function() { window.location.reload()})
        .fail(function() { window.location.reload()})
    else if(el.attr('method') == 'PUT') $.put(location, data);

    $(`#${formid}-modal`).modal('hide');
}

function LoadBuyModal(name, quantity, price, date) {

    $(buyModal).modal('show');

    let quantityEl = $(buyModal).find("input[name='Quantity']");
    let priceEl = $(buyModal).find("input[name='Price']");

    $(buyModal).find("#cost-output").html(`Cost: \$${calculateCost(priceEl.val(), quantityEl.val())}`);

    $(buyModal).find("input[name='Quantity']").attr("max", quantity);
    $(buyModal).find("#buy-max").html("Max available " + quantity + ".");

    $(buyModal).find("input[name='Name']").val(name);
    $(buyModal).find("input[name='Price']").val(price);
    $(buyModal).find("input[name='Date']").val(date);

    $(buyModal).find("input[name='Quantity']").change(function() {
        $(buyModal).find("#cost-output").html(`Cost: \$${calculateCost(priceEl.val(), quantityEl.val())}`);        
    });
}

function LoadUpdateModal(name, quantity, price, date, ticketid) {

    $(updateModal).modal('show');
    $(updateModal + " input[name='Name']").val(name);
    $(updateModal + " input[name='Quantity']").val(quantity);
    $(updateModal + " input[name='Price']").val(price);
    $(updateModal + " input[name='Date']").val(date);
    $(updateModal + " #update-ticket-form").attr("data-ticket-id", ticketid);
}

$(function () {

    $.fn.datetimepicker.Constructor.Default = $.extend({}, $.fn.datetimepicker.Constructor.Default, {
        viewMode: 'days',
        collapse: true,
        format: 'L',
        icons: {
            time: 'far fa-clock',
            date: 'far fa-calendar',
            up: 'fa fa-arrow-up',
            down: 'fa fa-arrow-down',
            previous: 'fa fa-chevron-left',
            next: 'fa fa-chevron-right',
            today: 'fa fa-calendar-check-o',
            clear: 'fa fa-trash',
            close: 'fa fa-times'
        },
        format: 'YYYY[/]M[/]D'
    });

    $('#sell-datetime').datetimepicker();
    $('#update-datetime').datetimepicker();

    // Use /viewPOST as api endpoint for testing, make sure to change this!!! (you can see it in the console)

    $('#sell-ticket-button').click(function () {SubmitForm('sell', '/sell')});
    $("#update-ticket-button").click(function() {SubmitForm('update', '/update')});
    $("#buy-ticket-button").click(function() {SubmitForm('buy', '/buy')});
});

