/* Labelisation */
$('.container-fluid').on('click',"i[class*='vote-']", function(){
    review_id = $(this).attr('review-id');
    vote = $(this).attr('vote');
    console.log(review_id);
    $.ajax({
       url : '/label-review/'+ review_id,
       data : {"vote": vote},
       success : function(html){
          row = $("tr[id-review="+review_id+"]");
          update_row = $(html).find("tr[id-review="+review_id+"]");
          console.log(update_row);
          console.log(row);
          row.replaceWith(update_row);
       }
    });
});

/* Prediction */
$('#predict-btn').click(function(){
    $.ajax({
        url : '/admin/predict-label',
        success : function(html){
            reviews = $(html).filter('#reviews-table');
            $('#reviews-table').html(reviews.html());
        }
    });
});

/* Remove review */
$('.container-fluid').on('click','.remove-review', function(){
    review_id = $(this).parent().parent().attr('id-review');
    console.log(review_id);
    $.ajax({
       url : '/remove-review/'+ review_id,
       success : function(html){
          row = $("tr[id-review="+review_id+"]");
          update_row = $(html).find("tr[id-review="+review_id+"]");
          console.log(update_row);
          row.remove();
       }
    });
})

/* Filter Form */
$('#form_filter_label').on('change','input[name="search"]', function(){
    var currentUrl = window.location.href;
    var serialize = $('#form_filter_label').serialize();
    if (currentUrl.includes('?')) {
        currentUrl = currentUrl.replace(/\?.+/,'?'+serialize);
    } else {
        currentUrl = window.location.href + '?' + serialize; }

    $.ajax({
        url : currentUrl,
        type: 'GET',
        success : function(html){
            filter_label = $(html).find('#reviews-table');
            $('#reviews-table').html(filter_label.html());
        }
    });
});