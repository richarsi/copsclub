var common_content_filter = '#content>*:not(div.configlet),dl.portalMessage.error,dl.portalMessage.info';
var forumbase = {
	agendaFilterSubmit : function() {
		jq.ajax({
			url : 'agenda-overzicht-bare',
			type : 'GET',
			asynchronous : true,
			data : jq('.gf-AgendaFilter form').serialize(),
			complete : function(request) {
				if (request.status == 200) {
					jq('#content').html(request.responseText);
					forumbase.agendaFilterNrOfPerfs();
					forumbase.centerImages();
				}
			}
		});
	},
	agendaFilter : function() {
		jq(".gf-filter input").hide();
		jq('.gf-filter label').css('cursor', 'pointer');
		jq('#_filter_wanneer_widget_datepicker').datepicker(
				$.datepicker.regional.nl);
		jq('label[for="_filter_wanneer_widget_datepicker"]').click(function() {
			jq('#_filter_wanneer_widget_datepicker').show();
			jq('#_filter_wanneer_widget_datepicker').datepicker('show');
		});
		jq('#_filter_wanneer_widget_datepicker').change(function() {
			forumbase.agendaFilterSubmit();
			jq('#_filter_wanneer_widget_datepicker').val('');
		});
		jq('.gf-filter label')
				.click(
						function() {
							var input = jq(this).parents('li').find('input');
							var filter = jq(this).parents('ul');
							input.attr('checked', true);
							filter.find('label').removeClass('selected');
							jq('#_filter_wanneer_widget_datepicker').hide();
							jq(this).addClass('selected');
							if (jq(this).attr('for') != '_filter_wanneer_widget_datepicker') {
								forumbase.agendaFilterSubmit();
							}
							var filter_for = jq(this).attr('for');
							var str = '_filter_activiteit_categorie_';
							if (filter_for.match("^" + str) == str) {
								if (filter_for != str) {
									jq(
											".gf-filter label[for='_filter_aantal_voorstellingen_eerste']")
											.click();
								}
							}
						});
	},
	agendaFilterNrOfPerfs : function() {
		jq("p.gf-firstonly-filter-shortcut").show();
		var selector = "a[class~='gf-filter']";
		jq(selector).css('cursor', 'pointer');
		var filter_ul = jq(
				".gf-filter label[for='_filter_aantal_voorstellingen_eerste']")
				.parent().parent();
		filter_ul.prev().hide();
		filter_ul.hide();
		jq(selector)
				.click(
						function() {
							if (jq(this).hasClass("firstonly")) {
								jq(
										".gf-filter label[for='_filter_aantal_voorstellingen_eerste']")
										.click();
							} else {
								if (jq(this).hasClass("nofirstonly")) {
									jq(
											".gf-filter label[for='_filter_aantal_voorstellingen_']")
											.click();
								};
							}
						});
	},
	centerImages : function() {
		if (jq(".gf-item-image img").length > 0) {
			jq(".gf-item-image img").imgCenter();
		}
		if (jq("p.plonetruegallery > a > img") > 0) {
			jq("p.plonetruegallery > a > img").imgCenter();
		}
	},
	vandaagUitgelicht : function() {
		jq('#gf-vandaag-uitgelicht-portlet .gf-vandaagUitgelichtTitle')
				.click(
						function() {
							jq('#gf-vandaag-uitgelicht-portlet .content')
									.hide();
							jq(
									'#gf-vandaag-uitgelicht-portlet .gf-vandaagUitgelichtTitle')
									.removeClass('gf-selected');
							jq(this).addClass('gf-selected');
							jq('#' + jq(this).attr('id') + '-content').show();
						});
	},
	todayTomorrow : function() {
		jq('#today-tomorrow .title').live('click', function() {
			jq('#today-tomorrow .content').hide();
			jq('#today-tomorrow .title').removeClass('selected');
			jq(this).addClass('selected');
			jq('#' + jq(this).attr('id') + '-content').show();
		});
	},
	makeDivsClickable : function() {
		jq("div.gf-clickable").click(function() {
			window.location = jq(this).find("a:first").attr("href");
		});
	},
	highlightWidget : function() {
		jq("#gf-highlight-widget").cycle();
		jq(".gf-highlight-selector .gf-highlight-selection").click(function() {
			var index = 0;
			var classes = jq(this).attr('class').split(' ');
			var i, klass;
			for (i = 0; i < classes.length; ++i) {
				klass = classes[i];
				if (klass.match(/^index-/)) {
					index = klass.replace("index-", '');
					break;
				}
			}
			jq("#gf-highlight-widget").cycle(parseInt(index));
		});
	},
	clearInputsOnClick : function() {
		jq('#gf-portal-footer-newsletter input[type="text"]').each(function() {
			jq(this).focus(function() {
				this.value = ' ';
			});
		});
	},
	dropShadow : function() {
		jq('#content #gf-highlight-title h1').each(function() {
			var shadowOptions = {
				left : 0,
				top : 0,
				blur : 1,
				opacity : '.5',
				color : "black",
				swap : false
			};
			jq(this).dropShadow(shadowOptions);
		});
	},
	starRating : function() {
		jq('#formfield-form-widgets-rate span.label').hide();
		jq('input[name=form.widgets.rate:list]').rating();
	},
	readOnlyStarRating : function() {
		var counter = 0;
		jq('div.commentRate')
				.each(
						function() {
							counter += 1;
							var rate = jq(this);
							var rate_string = rate.children('span').text();
							var uid = counter;
							var iRate = parseInt(rate_string) - 1;
							var maxRate = 5;
							var html = "";
							var input_tpl = '<input name="rate-'
									+ uid
									+ '" type="radio" class="star" disabled="disabled" ';
							var i;
							for (i = 0; i < maxRate; i++) {
								if (i == iRate) {
									html += input_tpl + '"checked="checked"/>';
								} else {
									html += input_tpl + '/>';
								}
							}
							html += '<span class="gf-waardering">'
									+ rate_string + '</span>';
							rate.html(html);
						});
		jq('input.star').rating();
	},
	cleanupCommenting : function() {
		var form_errors = jq('div#commenting').find('div.error');
		if (!form_errors.length) {
			jq('#commenting').hide();
		}
		jq('div.commentBody').addClass('gf-commentBody');
		jq('div.commentBody').removeClass('commentBody');
		jq('#gf-write-comment').click(function(e) {
			e.preventDefault();
			jq('#commenting').toggle('slow');
		});
	},
	tvScreens : function() {
		var background = jq("#tvscreen #background");
		if (background) {
			background.cycle({
				speed : 1000,
				timeout : 10000
			});
			setInterval(function() {
				$.ajax({
					url : window.location.pathname,
					success : function(data) {
						var jqdata = $(data);
						$('#background')
								.html(jqdata.find('#background').html());
						$('#list').html(jqdata.find('#list').html());
						background.cycle('stop');
						background.cycle('resume');
					}
				});
			}, 1800000);
		}
	},
	updateClock : function() {
		var clock = jq("#clock");
		if (clock) {
			setInterval(function() {
				var currentTime = new Date();
				var currentHours = currentTime.getHours();
				var currentMinutes = currentTime.getMinutes();
				currentMinutes = (currentMinutes < 10 ? "0" : "")
						+ currentMinutes;
				currentHours = (currentHours == 0) ? 12 : currentHours;
				clock.html(currentHours + ":" + currentMinutes);
			}, 60000);
		}
	},
	forumOverlay : function() {
		jq("#content a[href$='@@event-aanmelden']").prepOverlay({
			subtype : 'ajax',
			formselector : "form",
			closeselector : "a[href*='@@register'], a[href*='mail_password']",
			filter : common_content_filter
		});
		jq("#pb_3, #pb_4").bind("onLoad", function() {
			jq(".pb-ajax a[href*='@@register']").prepOverlay({
				subtype : 'ajax',
				formselector : 'form',
				filter : common_content_filter
			});
			jq(".pb-ajax a[href*='mail_password']").prepOverlay({
				subtype : 'ajax',
				formselector : 'form',
				filter : common_content_filter
			});
			jq("[id*=pb]").bind("onLoad", function() {
				forumbase.profileMultiSelect();
				forumbase.datepickerBirthday();
			});
		});
		jq("#banners a[href$='@@register']").prepOverlay({
			subtype : 'ajax',
			formselector : 'form',
			filter : common_content_filter,
			noform : function() {
				return 'reload';
			}
		});
		jq("[id*=pb]").bind("onLoad", function() {
			forumbase.profileMultiSelect();
			forumbase.datepickerBirthday();
		});
	},
	datepickerBirthday : function() {
		jq(document.getElementById('form.birthdate')).datepicker({
			yearRange : '1900:2011',
			changeMonth : true,
			hideIfNoPrevNext : true,
			changeYear : true
		});
	},
	profileMultiSelect : function() {
		jq("select[multiple='multiple']:not(#themefilter)").addClass(
				"multiselect");
		jq(".multiselect").multiselect({
			sortable : false,
			searchable : false
		});
	},
	handleDefaultInputs : function() {
		jq("input.show_default").each(function() {
			var v = this.value;
			$(this).blur(function() {
				if (this.value.length == 0) {
					this.value = v;
				}
			}).focus(function() {
				this.value = "";
			});
		});
	},
	enableMobileMenu : function() {
		$('#pull').click(
				function(e) {
					e.preventDefault();
					jq("#menu ul").toggle('blind');
					jq(this).children("i").toggleClass("icon-caret-right")
							.toggleClass("icon-caret-down");
				});
	},
	mobileMovement : function() {
		var top_portlet = jq("#today-tomorrow, #gf-vandaag-uitgelicht-portlet")
				.parent();
		if (!top_portlet.hasClass("cloned")) {
			jq("#content").prepend(top_portlet.clone({
				withDataAndEvents : true
			}).addClass("clone"));
			top_portlet.addClass('cloned');
		}
		var personal_tools = jq("#portal-personaltools-wrapper");
		var site_selector = jq("#gf-site-selector");
		if (!personal_tools.hasClass("cloned")) {
			jq("#gf-portal-footer-copyright .gf-divider").after(
					personal_tools.clone({
						withDataAndEvents : true
					}).addClass("clone"));
			personal_tools.addClass('cloned');
		}
		if (!site_selector.hasClass("cloned")) {
			site_selector.addClass('cloned');
		}
		jq(
				"#gf-news-widget .notclickable h2, #gf-news-widget .notclickable img")
				.click(
						function() {
							jq(this).closest(".gf-news-widget-cell").children(
									'p').toggle('blind');
						});
		jq(".gf-filter-header").click(
				function() {
					jq(this).next("ul").toggle('blind');
					jq(this).children("i").toggleClass("icon-caret-right")
							.toggleClass("icon-caret-down");
				});
		var program = jq("#gf-programma").not('.clone');
		if (!program.hasClass("cloned")) {
			jq(".gf-activiteitImage").after(program.clone({
				withDataAndEvents : true
			}).addClass("clone"));
			program.addClass('cloned');
		}
		jq(".header").not("#gf-programma .header").click(
				function() {
					jq(this).next().toggle('blind');
					jq(this).children("i").toggleClass("icon-caret-right")
							.toggleClass("icon-caret-down");
				});
		jq("#gf-programma .header").click(
				function() {
					jq(".gf-programma-list, .gf-programma-info")
							.toggle('blind');
					jq(this).children("i").toggleClass("icon-caret-right")
							.toggleClass("icon-caret-down");
				});
		var navportlet = jq(".portletNavigationTree");
		if (navportlet.length > 0) {
			navportlet.children(".portletHeader")
					.toggleClass("hiddenStructure");
			var header_anchor = navportlet.children(".portletHeader").children(
					"a");
			header_anchor.click(function(e) {
				e.preventDefault();
				jq(this).parent().parent().children("dd").toggle('blind');
				jq(this).children("i").toggleClass("icon-caret-right")
						.toggleClass("icon-caret-down");
			});
			if (!header_anchor.hasClass("handled")) {
				header_anchor.append(' <i class="icon-caret-right"></i>');
				header_anchor.addClass('handled');
			}
			jq(".portletNavigationTree .portletItem").hide();
		}
		jq(".link-overlay").unbind("click");
		jq("p.gf-firstonly-filter-shortcut").toggleClass('cloned');
		if (jq(".gf-selected-filter").length == 0) {
			jq(".gf-agenda-description").hide();
		}
	},
	undomobileMovement : function() {
		$('#pull').unbind('click');
		jq(".gf-filter-header").unbind('click');
		jq(".header").unbind('click');
		jq(".portletNavigationTree .portletHeader").toggleClass(
				"hiddenStructure");
		jq(".portletNavigationTree .portletItem").show();
	}
};
jq(document).ready(function() {
	if ($('#media-query-check').css('margin-bottom') == '1px') {
		forumbase.cssQuerySupport = true;
	} else {
		forumbase.cssQuerySupport = false;
	}
	forumbase.forumOverlay();
	forumbase.agendaFilter();
	forumbase.agendaFilterNrOfPerfs();
	forumbase.vandaagUitgelicht();
	forumbase.todayTomorrow();
	forumbase.makeDivsClickable();
	forumbase.highlightWidget();
	forumbase.clearInputsOnClick();
	forumbase.dropShadow();
	forumbase.starRating();
	forumbase.readOnlyStarRating();
	forumbase.cleanupCommenting();
	forumbase.tvScreens();
	forumbase.updateClock();
	forumbase.centerImages();
	forumbase.datepickerBirthday();
	forumbase.profileMultiSelect();
	forumbase.handleDefaultInputs();
	if (forumbase.cssQuerySupport != false) {
		enquire.register("screen and (max-width:600px)", {
			match : function() {
				forumbase.mobileMovement();
				forumbase.enableMobileMenu();
			},
			unmatch : function() {
				forumbase.undomobileMovement();
			}
		}).listen(10);
	}
});