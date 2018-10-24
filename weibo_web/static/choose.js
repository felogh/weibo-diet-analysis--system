$(function(){

	$('#food_search').click(function(){
		var district = $('#district').val();
		var gender = $('#gender').val();
		var time = $('#time').val();
		var mode = $('#mode').val();
		$.ajax({
			type:"POST",
			url:"/",
			data:{"district": district, "gender": gender, "time": time, "mode": mode},
			success:function(data){
                arr = data.split("#")
                $("#topfoods").attr("src", arr[0]);
                $("#wordcloud").attr("src", arr[1]);
			},
		});
		return false;

	});

})
