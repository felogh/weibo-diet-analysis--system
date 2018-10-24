$(function(){

	$('#food_search').click(function(){
		var food_name = $('#food_name').val();
		var choice = $('#choice').val();
		$.ajax({
			type:"POST",
			url:"/search",
			data:{"food_name": food_name, "choice": choice},
			success:function(data){
                $("#rtn_img").attr("src", data);
			},
		});
		return false;

	});

})
