## 6.03.2024

### Added

- Users can now edit and delete their responses.
  - Edit only if response has not been accepted yet and only if current user is author of the response or has such permissions
  - Delete only if current user is author of the response or has such permissions
- Users can view list of their responses
- Users can view details of their responses

### Changed

- Moved response accepted notification from board/signals.py to accept method of Response model in board/models.py, because it executed also when response has been edited.

## 2.03.2024

### Added

- Started django project
- Database: PostgreSQL
- Created Advert and Response models, extended Usser model with subcriptions array field
- Advert model 'text' field is a WYSYWIG editor (used django-tinymce)
- Created views:
  - AdvertList
    - shows list of adverts
    - paginated by 10 per page
    - supports filtering
  - AdvertDetail
    - shows details of advert
  - AdvertCreate
    - handles creation of advert
    - only for authenticated users
  - AdvertEdit
    - handles advert editing
    - only for author of the advert or users with such permissions
  - AdvertDelete
    - handles deleteing of an advert
    - only for author of the advert or users with sudch permissions
  - ResponseCreate
    - handles creation of the response
    - only for authenticated users
    - users can not respond to their own adverts
  - ResponseList
    - shows list of responses to current user's adverts
    - only for authenticated users
    - paginated by 10 per page
    - supports filtering
  - subscriptions
    - handles user's subscriptions to categories
    - available actions:
      - subscribe - subscribes user to chosen category
      - unsubscribe - unsubscribe user from chosen category
      - clear - unsubscribe user from all categories
      - all - subscribe user to all categories
    - only for authenticated users
  - response_action_handle
    - handles accept and reject actions of the response
    - only for authenticated users
  - ProfileUser
    - shows information about current user
    - username (readonly)
    - email (readonly)
    - first name (editable)
    - last name (editable)
    - user's subscriptions
- Urls:
  - board/urls.py:
    - adverts/ - list of adverts (AdvertList view)
    - user_adverts - list of current user's adverts (AdvertList view filtered by current user)
    - adverts/<int:pk> - details of the advert (AdvertDetail view)
    - adverts/create - create an advert (AdvertCreate view)
    - advert/<int:pk>/edit - advert editing (AdvertEdit view)
    - adverts/<int:pk>/delete - delete an advert (AdvertDelete view)
    - respoonse/create - create a response (ResponseCreate view)
    - responses/ - list of responses to current user's adverts (ResponseList view)
    - responses/action_handle - handles accepting and rejecting responses (response_action_handle view)
    - subscriptions/ - user's subscriptions to categories (subscriptions view)
  - accounts/urls.py:
    - profile/ - user's profile (ProfileUser view)
- Authorization via email + mandatory email verification (using django-allauth)
- Sending emails using django signals and celery (message broker: redis):
  - to author of advertisement when new response added to that advert
  - to author of the response when response is accepted
  - to all users subscribed to category when advert is created
  - to all users subscribed to categories of adverts created over the past week
- Filters (using django-filter):
  - ResponseFilter - used in ResponseList view, filterable fields:
    - title of the advert, response is associated with
    - category of the advert, response is associated with
    - date of response creation
    - whether response is accepted or not
  - AdvertFilter - used in AdvertList view, filterable fields:
    - title of the advert
    - category of the advert
    - date of advert creation
- Translation to russian
  - language can be selected on navbar
- Filebased caching
  - Advert instances are cached until modified

### Changed

- email backend changes depending on DEBUG
  - If DEBUG = True, then send emails to console, send to email otherwise
