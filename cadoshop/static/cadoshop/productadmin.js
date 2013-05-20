(function($){
    $(document).ready(function($) {
    	
    	/* function saveExtra(){
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
		}*/
		if ($('#productoption_set-group').length)
		{
	    	
			/*$('.field-extra').each(function(){
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
			$('#id_category').change();*/
			

			$.fn.grp_inline_original = $.fn.grp_inline; 
			$.fn.grp_inline_original.defaults = $.fn.grp_inline.defaults; 
			
			$.fn.grp_inline = function(opts){
				ret = this.grp_inline_original(opts);
				if (opts.prefix == 'productoption_set')
				{
			    	//alert("asd");
			    	//$('#productoption_set-group')
			    	if ($('#productoption_set0').length == 0)
					{
						addButton = $('#productoption_set-group').find("a.grp-add-handler:last");
						addButton.click();
						$('#id_productoption_set-0-name').val('default');
						$('#productoption_set0 .grp-remove-handler').hide();
					}
			    	else
			    	{
			    		$('#productoption_set0 .grp-delete-handler').hide();
			    	}
			    	
			    	
				}
				return ret;
			}
			$.fn.grp_inline.defaults = $.fn.grp_inline_original.defaults;
		}
    });
})(grp.jQuery);