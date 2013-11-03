/**
 * myswimmingclubtheme
 * v1.0
 * claretnbluester@gmail.com
 */
$(document).ready(
		function() {
			$('##menu>#pull').click(
					function(e) {
						e.preventDefault();
						$("#menu ul").toggle('blind');
						$(this).children("i").toggleClass("icon-caret-right")
								.toggleClass("icon-caret-down");
					});
		});

