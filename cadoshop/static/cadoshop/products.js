$(function(){
	
	$(".fancybox").fancybox({});
	$("select.optionSelect").change(function(){
		$(this).parents('.product').find('.optionPer').hide();
		$(this).parents('.product').find('.option' + $(this).val()).show();
	});
	$("select.optionSelect").change();
	
	if($("#tagcloud").length){
		$("#tagcloud").jQCloud(document.tags_list);
	}
})