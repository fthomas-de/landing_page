function update_values() {
            $SCRIPT_ROOT = {{ request.script_root|tojson|safe }};
            $.getJSON($SCRIPT_ROOT+"/_dice_results",
                function(data) {
                    $("p").text(data.res1)
                });
        }

	setInterval('update_values()', 1000);