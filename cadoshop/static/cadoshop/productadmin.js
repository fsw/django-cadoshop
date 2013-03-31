var $ = django.jQuery;
$(function(){
	
	if ($('#product_form').length)
	{
		$('.field-extra').after('<div id="extraDiv"></div>');
		$('.field-extra').hide();
		var extra = JSON.parse($('#id_extra').val());
		
		$('#id_category').change(function(){
			$.get('/extrafields/' + $(this).val(), {}, function(data){
				$('#extraDiv').html(data);
				for (key in extra)
				{
					$("[name=extra\[" + key + "\]]").val(extra[key]);
				}
				$("[name^=extra]").change(function(i, elem){
					extra[$(elem).attr('name').substring(6, $(elem).attr('name').length-1)] = $(elem).val(); 
				});
			}, 'html');
		})
		
		$('#id_category').change();
		$('#product_form').submit(function(){
			//reset extra data
			extra = {};
			$("[name^=extra]").each(function(i, elem){
				extra[$(elem).attr('name').substring(6, $(elem).attr('name').length-1)] = $(elem).val(); 
			});
			$('#id_extra').val(JSON.stringify(extra));
		});
	}
})