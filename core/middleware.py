"""Middleware for audit logging and security."""

from core.audit_queue import get_audit_queue


class AuditMiddleware:
    """
    Middleware that captures POST/PUT/DELETE requests and logs them
    to the audit queue for batch writing to audit.sqlite3.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.method in ("POST", "PUT", "DELETE"):
            self._log_request(request, response)

        return response

    def _log_request(self, request, response):
        """Extract request details and push to audit queue."""
        try:
            user = (
                request.user.username if request.user.is_authenticated else "anonymous"
            )
        except Exception:
            user = "anonymous"

        ip_address = request.META.get("HTTP_X_FORWARDED_FOR", "").split(",")[
            0
        ] or request.META.get("REMOTE_ADDR", "")

        entry = {
            "user": user,
            "action": request.method,
            "url": request.get_full_path(),
            "ip_address": ip_address,
            "model_name": "",
            "object_id": "",
            "old_value": None,
            "new_value": None,
        }

        try:
            queue = get_audit_queue()
            queue.push(entry)
        except Exception:
            pass
