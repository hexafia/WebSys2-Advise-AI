# STRIDE Security: Spoofing Countermeasures

This plan outlines the steps to mitigate **Spoofing** (the "S" in STRIDE) by implementing robust Identity and Access Management (IAM) controls. The primary focus is preventing role impersonation and hardening session security.

## Proposed Changes

### Core Security Logic
Implement custom Django decorators to enforce strict role-based access control (RBAC).

#### [NEW] [decorators.py](file:///c:/Users/Melben/Downloads/websys_final/django/core/decorators.py)
- Create `role_required` decorator that checks `user.userprofile.role`.
- Handle redirection or "Permission Denied" errors for unauthorized access.

### View Protection
Apply the new decorators to existing views to ensure users cannot "spoof" their way into unauthorized dashboards.

#### [MODIFY] [views.py](file:///c:/Users/Melben/Downloads/websys_final/django/core/views.py)
- Decorate [student_dashboard](file:///c:/Users/Melben/Downloads/websys_final/django/core/views.py#108-186) with `@role_required('student')`.
- Decorate [adviser_dashboard](file:///c:/Users/Melben/Downloads/websys_final/django/core/views.py#187-245) with `@role_required('adviser')`.
- Decorate [admin_dashboard](file:///c:/Users/Melben/Downloads/websys_final/django/core/views.py#246-327) with `@role_required('admin')`.

### Security Hardening
Enhance session and CSRF security in the project configuration.

#### [MODIFY] [settings.py](file:///c:/Users/Melben/Downloads/websys_final/django/config/settings.py)
- Enable `SESSION_COOKIE_HTTPONLY` to prevent script-based session theft.
- (Optional for Prod) Add notes about `SESSION_COOKIE_SECURE` and `CSRF_COOKIE_SECURE`.

## Verification Plan

### Automated/Manual Tests
- **Identity Verification**: Attempt to access `/adviser/` while logged in as a Student. Expect a redirect or error.
- **CSRF Check**: Verify that all forms (login, registration, dashboard actions) include the `{% csrf_token %}` tag and that the middleware is active.
- **Session Analysis**: Use browser dev tools to confirm that the session cookie has the `HttpOnly` flag.
