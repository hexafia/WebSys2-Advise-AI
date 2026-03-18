# Walkthrough: STRIDE Spoofing Countermeasures

This document summarizes the changes made to harden the project against **Spoofing** (Role Impersonation), a key component of the STRIDE threat model.

## Changes Implemented

### 1. Role-Based Access Control (RBAC)
We introduced custom decorators to ensure that users can only access the dashboards intended for their roles.

- **[django/core/decorators.py](file:///c:/Users/Melben/Downloads/websys_final/django/core/decorators.py)**: Created the `@role_required` decorator. This middleware checks the `user.userprofile.role` against a list of allowed roles. If a user attempts to access an unauthorized page, they receive a "Permission Denied" message and are redirected to their appropriate dashboard or the login page.
- **[django/core/views.py](file:///c:/Users/Melben/Downloads/websys_final/django/core/views.py)**: Applied the decorators to the main views:
  - `@role_required(['student'])` on [student_dashboard](file:///c:/Users/Melben/Downloads/websys_final/django/core/views.py#109-188)
  - `@role_required(['adviser'])` on [adviser_dashboard](file:///c:/Users/Melben/Downloads/websys_final/django/core/views.py#189-248)
  - `@role_required(['admin'])` on [admin_dashboard](file:///c:/Users/Melben/Downloads/websys_final/django/core/views.py#249-331)

### 2. Session Security Enhancements
We updated the project settings to secure session cookies, preventing malicious scripts from stealing session tokens.

- **[django/config/settings.py](file:///c:/Users/Melben/Downloads/websys_final/django/config/settings.py)**: Added `SESSION_COOKIE_HTTPONLY = True` and `CSRF_COOKIE_HTTPONLY = True`.

## Verification Results

We wrote a suite of automated tests ([django/core/tests.py](file:///c:/Users/Melben/Downloads/websys_final/django/core/tests.py)) to verify these access controls.

### Test Cases Passed:
- [test_student_cannot_access_adviser_dashboard](file:///c:/Users/Melben/Downloads/websys_final/django/core/tests.py#22-27): Validated that a student attempting to access `/adviser/` is correctly redirected back to `/student/`.
- [test_adviser_cannot_access_student_dashboard](file:///c:/Users/Melben/Downloads/websys_final/django/core/tests.py#28-33): Validated that an adviser attempting to access `/student/` is correctly redirected back to `/adviser/`.
- [test_unauthenticated_user_redirects_to_login](file:///c:/Users/Melben/Downloads/websys_final/django/core/tests.py#34-40): Ensured that anonymous users are bounced to the login page when trying to access protected views.
- Role-specific access tests ([test_student_can_access_student_dashboard](file:///c:/Users/Melben/Downloads/websys_final/django/core/tests.py#41-45), etc.) confirmed that legitimate access is still permitted.

All 6 automated tests passed successfully, confirming that the spoofing mitigations are active and working as intended.
