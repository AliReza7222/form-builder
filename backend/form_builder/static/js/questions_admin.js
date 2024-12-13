document.addEventListener('DOMContentLoaded', function () {
    const typeFields = document.querySelectorAll('select[id$="-type"]');

    typeFields.forEach(function (typeField) {
        updateFieldsVisibility(typeField);

        typeField.addEventListener('change', function () {
            updateFieldsVisibility(typeField);
        });
    });

    const observer = new MutationObserver(function (mutations) {
        mutations.forEach(function (mutation) {
            if (mutation.type === 'childList') {
                const addedNodes = mutation.addedNodes;
                addedNodes.forEach(function (node) {
                    if (node.nodeType === 1 && node.matches('.inline-related')) {
                        const newTypeField = node.querySelector('select[id$="-type"]');
                        if (newTypeField) {
                            updateFieldsVisibility(newTypeField);
                            newTypeField.addEventListener('change', function () {
                                updateFieldsVisibility(newTypeField);
                            });
                        }
                    }
                });
            }
        });
    });

    observer.observe(document.body, {
        childList: true,
        subtree: true
    });

    function updateFieldsVisibility(typeField) {
        const row = typeField.closest('.inline-related');
        const typeValue = typeField.value;

        const maxLengthRow = row.querySelector('[id$="-max_length"]').closest('.form-row');
        const minValueRow = row.querySelector('[id$="-min_value"]').closest('.form-row');
        const maxValueRow = row.querySelector('[id$="-max_value"]').closest('.form-row');
        const isDecimalRow = row.querySelector('[id$="-is_decimal"]').closest('.form-row');

        if (typeValue === "SHORT_TEXT" || typeValue === "LONG_TEXT") {
            maxLengthRow.style.display = "block";
            minValueRow.style.display = "none";
            maxValueRow.style.display = "none";
            isDecimalRow.style.display = "none";
        } else if (typeValue === "NUMBER") {
            maxLengthRow.style.display = "none";
            minValueRow.style.display = "block";
            maxValueRow.style.display = "block";
            isDecimalRow.style.display = "block";
        } else {
            maxLengthRow.style.display = "none";
            minValueRow.style.display = "none";
            maxValueRow.style.display = "none";
            isDecimalRow.style.display = "none";
        }
    }
});
