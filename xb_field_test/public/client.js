function FieldTestXBlock(runtime, element, initialState) {
    "use strict";

    const $element = $(element);
    element = $element[0]; // <- Works around a Studio bug in Dogwood: https://github.com/edx/edx-platform/pull/11433
    const usageId = $element.data("usage-id") || $element.data("usage"); // usage-id in LMS/Studio, usage in workbench

    init();

    /**
     * Initialize the client-side code of this Field Test XBlock
     */
    function init() {
        console.log("Initializing FieldTestXBlock");
        // set up event handlers:
        $element.on("click", ".xb-field-test-submit", handleSubmitValue);
    };


    function handleSubmitValue(event) {
        event.preventDefault();

        const $button = $(event.target);
        const $li = $button.closest('li');
        const $input = $li.find('.xb-field-test-new-value');
        const url = runtime.handlerUrl(element, 'update_field');
        const fieldName = $li.data('field-name');
        const newValue = $input.val();
        const data = {field_name: fieldName, new_value: newValue};

        $.post(url, JSON.stringify(data), 'json').done(function(responseData) {
            $li.find(".xb-field-test-value").text(newValue);
            $input.val('');
        }).error(function() {
            $input.prop("disabled", true);
            $button.prop("disabled", true).text("Error: field not writable.");
        });
    }
}
