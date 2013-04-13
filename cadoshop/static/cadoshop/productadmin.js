var $ = django.jQuery;
$(function(){
	
	function saveExtra(){
		$('.extraFormDiv').each(function(){
			var extra = {};
			$(this).find("[name^=extra]").each(function(i, elem){
				if($(elem).attr('name') != 'extra')
					extra[$(elem).attr('name').substring(6, $(elem).attr('name').length-1)] = $(elem).val(); 
			});
			$(this).parents('.field-extra').find('textarea').first().val(JSON.stringify(extra));
		});
	}
	
	function loadExtra(){
		$('.extraFormDiv').each(function(){
			var extra = JSON.parse($(this).parents('.field-extra').find('textarea').first().val());
			for (key in extra)
			{
				$(this).find("[name=extra\[" + key + "\]]").val(extra[key]);
			}
		});
	}

	if ($('#product_form').length)
	{
		$('.field-extra').each(function(){
			extraDiv = $('<div class="extraFormDiv"></div>');
			$(this).append(extraDiv);
			$(this).children().first().hide();
		});
		
		
		$('#id_category').change(function(){
			$.get('/extrafields/' + $(this).val(), {}, function(data){
				$('.extraFormDiv').each(function(){
					$(this).html(data);
					$(this).find("[name^=extra]").change(function(){
						saveExtra();
					});
				});
				loadExtra();
			}, 'html');
		})
		$('#id_category').change();
	}
})