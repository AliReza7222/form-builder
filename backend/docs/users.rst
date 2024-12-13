 .. _users:

Users
======================================================================

Starting a new project, it’s highly recommended to set up a custom user model,
even if the default User model is sufficient for you.

This model behaves identically to the default user model,
but you’ll be able to customize it in the future if the need arises.

.. automodule:: form_builder.users.models
   :members:
   :noindex:


User Views
----------

**UserDetailView**

`UserDetailView` is a `DetailView` that displays the details of a user. It is protected by the `LoginRequiredMixin`, meaning only authenticated users can access this view.


**UserUpdateView**

`UserUpdateView` is an `UpdateView` that allows a user to update their profile information. It uses the `LoginRequiredMixin` to ensure only authenticated users can update their details.


**UserRedirectView**

`UserRedirectView` is a `RedirectView` that redirects authenticated users to their own profile page.


Management Commands
------------------

The `users` app includes custom management commands located in `management/commands`:

- **create_groups.py**: This command creates user groups for admin panel. It is typically used after migrations to set up the basic user roles for the application.

**Usage Example

To run the `create_groups` command, use the following:

.. code-block:: bash

  python manage.py create_groups


UserAdmin
---------

`UserAdmin` is a custom admin class and is used to manage the `User` model in the Django admin panel.


User API
--------

**UserViewSet**

This viewset supports retrieving, listing, and updating user data, but by default, it only allows access to the authenticated user's own data.

- **serializer_class**: Uses `UserSerializer` for serializing user data.
- **queryset**: Retrieves all `User` objects.
- **lookup_field**: Specifies that the primary key (`pk`) is used for lookups.

- Methods:

  - **get_queryset**: Filters the queryset to return only the data for the currently authenticated user.
  - **me**: A custom action (accessible via `GET /users/me/`) that returns the details of the currently authenticated user.
