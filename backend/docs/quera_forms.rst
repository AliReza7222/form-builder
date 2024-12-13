.. _quera_forms:

Quera_Forms
======================================================================

The quera_forms app is used for creating forms by site administrators,
collecting and managing responses from users, and validating the responses.

Models
------

**Form Model**

The `Form` model represents a form created by an administrator. It contains the following fields:

- **title**: A unique title for the form (max length: 100 characters).
- **created_at**: Timestamp when the form was created.
- **created_by**: Foreign key to the user who created the form.
- **updated_by**: Foreign key to the user who last updated the form.
- **updated_at**: Timestamp when the form was last updated.

- **Meta**: An index is created for the `title` field to improve query performance.

The `Form` model is used for creating forms that can contain multiple questions.


**Question Model**

The Question model is designed as a fat model to enable optimized queries and reduce the
number of database queries. This approach also allows for easier access to its associated
questions directly from the Form model.

The `Question` model represents a question in a form. It contains the following fields:

- **form**: Foreign key to the associated `Form`.
- **question_text**: The text of the question (max length: 300 characters).
- **help_text**: Optional help text for the question (max length: 300 characters).
- **required**: A boolean indicating if the question is required.
- **type**: The type of the question (e.g., text, numeric).
- **max_length**: Optional maximum length for text-based answers.
- **min_value**: Optional minimum value for numeric answers.
- **max_value**: Optional maximum value for numeric answers.
- **is_decimal**: A boolean indicating if the question allows decimal values.

- **Meta**: An index is created for the `type` field to optimize queries on question type.

The `Question` model is used to define the individual questions in a form.


**Response Model**

The `Response` model represents a user's response to a form. It contains the following fields:

- **form**: Foreign key to the associated `Form`.
- **user_identifier**: The user's email address to identify the responder.
- **created_at**: Timestamp when the response was created.

- **Meta**: An index is created for the `user_identifier` field to quickly query responses by user.

The `Response` model is used to store the responses submitted by users for specific forms.


**Answer Model**

The `Answer` model represents a specific answer to a question in a form response. It contains the following fields:

- **response**: Foreign key to the associated `Response`.
- **question**: Foreign key to the associated `Question`.
- **answer_text**: The text of the user's answer (optional).
- **answer_number**: The numeric value of the user's answer (optional).

The `Answer` model is used to store individual answers provided by users for each question in the form.


Forms
-----

**QuestionForm**:

The `QuestionForm` is a custom Django `ModelForm` designed to validate `Question`
objects in the admin interface. It leverages design patterns for flexible
and maintainable validation logic.

- **Strategy Pattern**:
    - Validation logic is implemented using the **Strategy Pattern**.
      Each question type (e.g., short text, long text, number) has a
      dedicated validator encapsulating type-specific rules.

- **Simple Factory Pattern**:
    - The `QuestionValidatorFactory` uses the **Simple Factory Pattern** to
      dynamically provide the appropriate validator based on the `type` field
      of the `Question`. If no specific validator is available, a DefaultValidator is used.

- **Dynamic Validation**:
    - The form's `clean` method utilizes the selected validator to check fields
      like `max_length`, `min_value`, and `max_value`. Errors are captured and mapped
      to individual fields using `self.add_error`.


Admin
-----

The admin interface for the `quera_forms` app is designed to provide an intuitive
and efficient way to manage forms and their associated questions.

**QuestionInline**

The `QuestionInline` class allows questions to be managed directly within the
`Form` admin interface. It is implemented as a stacked inline form with the following properties:

- **model**: `Question` - Specifies the related model for the inline.
- **form**: `QuestionForm` - Custom form for question management.
- **extra**: No extra empty forms are displayed by default.
- **Media**: Includes a custom JavaScript file (`js/questions_admin.js`) for
             showing dynamic fields related to type question.

**FormAdmin**

The `FormAdmin` class customizes the admin interface for the `Form` model,
enabling the management of forms and their associated questions. Key features include:

- **list_display**: Displays `title`, `created_by`, and `created_at` in the list view.
- **search_fields**: Allows searching by form title or the username of the user who created the form.
- **readonly_fields**: Fields such as `created_by`, `created_at`, `updated_by`,
                       and `updated_at` are read-only to prevent manual edits.
- **inlines**: Integrates `QuestionInline` to manage related questions directly within the form admin interface.

- **Custom Methods**

    1. **get_fieldsets(request, obj=None)**:
       Includes general fields like `title` and an informational section with
       read-only fields if the form already exists.

    2. **has_delete_permission(request, obj=None)**:
       Restricts delete permissions to the user who created the form or superusers.

    3. **save_model(request, obj, form, change)**:
       Automatically sets the `created_by` field when a new form is created.
       Updates the `updated_by` field for every save action.


Serializers
-----------

**QuestionSerializer**

- Serializes the `Question` model.
- Includes fields such as:

  - `id`: Unique identifier for the question.
  - `question_text`: The text of the question.
  - `help_text`: Optional additional guidance for users.
  - `required`: Indicates if the question is required.
  - `type`: Type of the question (e.g., short text, number).
  - `max_length`: Maximum character length (if applicable).
  - `min_value` and `max_value`: Minimum and maximum values (if applicable).
  - `is_decimal`: Specifies if the number accepts decimals.

**FormSerializer**

- Serializes the `Form` model.
- Includes the following fields:

  - `id`: Unique identifier for the form.
  - `title`: Title of the form.
  - `created_at` and `updated_at`: Timestamps for form creation and updates.
  - `created_by` and `updated_by`: Users who created and last updated the form.
  - `questions`: Nested representation of associated `Question` objects using `QuestionSerializer`.

**AnswerSerializer**

- Serializes the `Answer` model.
- Fields:

  - `question`: The related `Question` object.
  - `answer_text`: The text answer provided by the user.
  - `answer_number`: The numerical answer provided by the user.

- Validation:

  - Ensures the `answer_text` or `answer_number` aligns with the type and
    requirements of the associated `question`.

  - Uses the **Strategy Pattern** for validation, implemented through the
    `AnswerValidatorFactory` to determine and apply the appropriate validator for the question type.

  - Relies on the **Simple Factory Pattern**, implemented through the
    `AnswerValidatorFactory`, to dynamically instantiate and return the
    appropriate validator based on the question type.

**ResponseSerializer**

- Serializes the `Response` model.
- Fields:

  - `form`: The `Form` object associated with the response.
  - `user_identifier`: Unique identifier (email) for the user submitting the response.
  - `answers`: Nested list of `Answer` objects, serialized using `AnswerSerializer`.

- Validation:

  - Verifies all provided answers belong to the specified `form`.
  - Ensures all required questions from the form are answered.
  - Raises detailed validation errors for:

    - Answers referencing questions outside the specified form.
    - Missing answers for required questions.

- Creation:

  - Custom `create` method:

    - Saves the `Response` object.
    - Bulk creates associated `Answer` objects for optimal database performance.


API Views
---------

**FormListView**

- Endpoint: Lists all forms with associated questions.
- FormPagination:

  - Implements custom pagination for forms:

    - `page_size`: Default number of forms per page (10).
    - `page_size_query_param`: Allows clients to customize page size.
    - `max_page_size`: Restricts maximum page size to 100.

- Features:

  - Fetches all forms, prefetching related `questions` to optimize database queries.
  - Supports pagination using `FormPagination`.
- Serializer: `FormSerializer`.

**FormDetailView**

- Endpoint: Retrieves details of a single form, including its associated questions.
- Features:

  - Prefetches `questions` for efficient query handling.
- Serializer: `FormSerializer`.

**ResponseViewSet**

This viewset handles the creation and modification of user responses to forms.

- queryset: Fetches all `Response` objects from the database.
- serializer_class: Utilizes the `ResponseSerializer` to validate and serialize request and response data.
- http_method_names: Restricts the allowed HTTP methods to `POST`, `PUT`, and `PATCH`, ensuring that only response creation and updates are permitted.
- permission_classes: Uses `AllowAny`, granting unrestricted access to the viewset for any user or system.
