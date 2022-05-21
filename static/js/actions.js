var url = window.location.href;
var curl = '';

$('#max_price').keyup(function () {
    min_price = $('#min_price').val();
    max_price = $('#max_price').val();
})

$('.price-filter').click(function () {
    $('#min_price').keyup(function () {
        min_price = $('#min_price').val();
    });
    $('#max_price').keyup(function () {
        max_price = $('#max_price').val();
    });
    max_price = $('#max_price').val();
    min_price = $('#min_price').val();
    if (parseInt(min_price) > parseInt(max_price)) {
        $('#max_price').css("border", "5px solid red");
        alert("Max ga kattaroq son kiriting !!!");
    } else {
        new_url = set_params(url, 'min-price', min_price);
        new_url = set_params(new_url, 'max-price', max_price);
        window.location.replace(new_url);
    }
});

$('.sorting').change(function () {
    new_url = set_params(url, 'sorting', $(this).val());
    window.location.replace(new_url);
});
$('.per-page').change(function () {
    new_url = set_params(url, 'per-page', $(this).val());
    window.location.replace(new_url);
});
$('.paging').click(function () {
    new_url = set_params(url, 'page', $(this).data('value'));
    window.location.replace(new_url);
});
$('.select-category').click(function () {
    new_url = set_params(url, 'cat', $(this).data('category'));
    window.location.replace(new_url);
});

function set_params(url, param, value) {
    path = url.split('?')[0];
    if (url.includes("?")) {
        curl = url.split('?')[1];
        params = curl.split('&');
        is_finded = false;
        for (i = 0; i < params.length; i++) {
            if (params[i].split('=')[0] == param) {
                params[i] = `${param}=${value}`;
                is_finded = true;
            };
        };
        curl = params.join('&');
        url = path + '?' + curl;
        if (!is_finded)
            url += `&${param}=${value}`;
    } else {
        curl += `?${param}=${value}`;
        url = path + curl;
    };

    return url;
};
$('.add-cart').click(function () {
    product_id = $(this).data('id');
    data = {'product_id': product_id};
    url_add_cart = '/order/add-cart/';
    post_data(url_add_cart, data,update_badge);
});

function update_badge(response) {
    console.log(response)
    $('#badge').text(response.items_count)
    if(response.event == 'added'){
        $(`#pbtn${response.pid}`).removeClass('btn-primary')
        $(`#pbtn${response.pid}`).text('Added to cart')
        $(`#pbtn${response.pid}`).addClass('btn-success')
    }else if(response.event == 'deleted'){
        $(`#pbtn${response.pid}`).removeClass('btn-success')
        $(`#pbtn${response.pid}`).text('Add to cart')
        $(`#pbtn${response.pid}`).addClass('btn-primary')
    }
}

function post_data(url, data,callback)  {
    $.ajax({
        type: "POST",
        url: url,
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        data: JSON.stringify(data),
        success: callback
    })
}
   // sdsdsd


$('.change-quantity').click(function () {
    item_id=$(this).data('item')
    action=$(this).data('action')
})

$('.input-quantity').keyup(function () {
    value=$(this).val()
    item_id=$(this).data('item')
    console.log(value,item_id)
    action='onkeyup'
    let url_change_quantity='/order/change-quantity/'
    let data={
        'item':item_id,
        'action':action,
        'value':value
    }
    post_data(url_change_quantity,data,item_quantity_cange)
})

function item_quantity_cange(response) {
    if(response.error == false){
        $(`#${response.item}`).val(response.item_quantity)
        $(`#price${response.item}`).text(`$${response.total_price}.0`)
        $('#total-price').text(`$${response.total}.0`)

    }
}


$('.remove-item').click(function () {
    item_id=$(this).data('id')
    console.log(item_id)
    $.ajax({
        type: "GET",
        url: `/order/remove/${item_id}/`,
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        success: function (response) {
            console.log(response)
            if(response.success)
                $(`#item_tr_${response.id}`).remove()
            $('#badge').text(response.items_count)
            $('#total-price').text(`$${response.total}.0`)
            $('#total-price').text(`$0`)
        }
    })
})