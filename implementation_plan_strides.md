# Expanded STRIDE Security Plan (T, R, I, D, E)

This plan outlines the steps to harden the application against the remaining five threats in the STRIDE model.

## Proposed Countermeasures

### 🛡️ Tampering (T)
**Vulnerability**: An attacker can manipulate IDs in form submissions to approve/reject records they don't own.
- **Action**: Add direct ownership/permission checks in [adviser_dashboard](file:///c:/Users/Melben/Downloads/websys_final/django/core/views.py#189-248) and [admin_dashboard](file:///c:/Users/Melben/Downloads/websys_final/django/core/views.py#249-331) views.
- **Goal**: Ensure that an adviser can only update forms they are authorized to manage.

### 📜 Repudiation (R)
**Vulnerability**: Currently, there is no audit log of critical actions (enrollment approvals, user status changes).
- **Action**: Create a `SecurityLog` model and implement a lightweight logging system in [views.py](file:///c:/Users/Melben/Downloads/websys_final/django/core/views.py).
- **Goal**: Create an immutable record of "Who did what and when."

### 📂 Information Disclosure (I)
**Vulnerability**: `DEBUG = True` leaks system architecture on error pages. Also, sensitive fields might be exposed in logs.
- **Action**: Suggest turning off `DEBUG` in a "production-ready" settings block and add standard error handlers.
- **Goal**: Prevent data leaks through error messages.

### 🚦 Denial of Service (D)
**Vulnerability**: No rate limiting on login or form submission actions.
- **Action**: Implement a simple, built-in rate limiter for the login view to prevent brute-force attacks.
- **Goal**: Ensure the application remains available under attack.

### 🔑 Elevation of Privilege (E)
**Vulnerability**: A student might try to POST directly to an admin-only endpoint if the decorator is bypassed.
- **Action**: Reinforce object-level permissions and ensure that superuser checks are consistently applied.
- **Goal**: Prevent users from gaining unauthorized access to higher privileges.

---

## Technical Details

#### [MODIFY] [models.py](file:///c:/Users/Melben/Downloads/websys_final/django/core/models.py)
- **NEW**: `SecurityAuditLog` model with fields: [user](file:///c:/Users/Melben/Downloads/websys_final/django/core/views.py#98-102), `action`, `target_object_id`, `timestamp`, `ip_address`.

#### [MODIFY] [views.py](file:///c:/Users/Melben/Downloads/websys_final/django/core/views.py)
- Integrate logging calls after successful POST actions.
- Add stricter validation checks in `update_form` and `update_enrollment` to prevent unauthorized cross-user modifications.

---

## Verification Plan

### Manual & Automated Tests
1. **Tampering**: Log in as Adviser A and attempt to approve a form intended for Adviser B using a modified `form_id`. Expect failure.
2. **Repudiation**: Perform an enrollment approval and then check the `SecurityAuditLog` table to verify the event was recorded.
3. **Denial of Service**: Attempt to log in with an incorrect password 10 times in 1 minute. Expect a temporary block.
