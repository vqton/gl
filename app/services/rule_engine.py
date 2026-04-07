"""Accounting Rule Engine for SoD, period locks, and amount thresholds.

Implements domain-specific validation rules required by Circular 99/2025/TT-BTC
for Vietnamese enterprise accounting, including Segregation of Duties (SoD)
checks, accounting period lock enforcement, and monetary amount thresholds.
"""

from decimal import Decimal


class RuleEngine:
    """Static rule engine for accounting-specific authorization checks.

    All methods are stateless and return a result dict with the following keys:
        - ``allowed`` (bool): Whether the action is permitted.
        - ``reason`` (str): Human-readable explanation (Vietnamese + English).
        - ``requires_escalation`` (bool): Whether the action needs higher-level approval.
    """

    AMOUNT_THRESHOLD_VND = Decimal("1000000000")  # 1 billion VND

    @staticmethod
    def check_sod_creator_approver(user, resource):
        """Enforce SoD: the creator of a resource cannot approve it.

        Prevents a single individual from both creating and approving
        accounting entries, which is a fundamental internal control
        requirement under Circular 99/2025/TT-BTC.

        Args:
            user: The user attempting the approval action. Must have an ``id``
                attribute matching the ``created_by`` foreign key on the resource.
            resource: The accounting resource (e.g. JournalEntry) being approved.
                Must have a ``created_by`` attribute.

        Returns:
            dict: Result with ``allowed``, ``reason``, and ``requires_escalation`` keys.
        """
        if hasattr(resource, "created_by") and resource.created_by == user.id:
            return {
                "allowed": False,
                "reason": (
                    "Người tạo không được phê duyệt chứng từ do chính mình lập. "
                    "Segregation of Duties violation: creator cannot approve own entry."
                ),
                "requires_escalation": False,
            }
        return {
            "allowed": True,
            "reason": "SoD check passed: user is not the creator.",
            "requires_escalation": False,
        }

    @staticmethod
    def check_sod_approver_executor(user, resource):
        """Enforce SoD: a user who approved a resource cannot execute (pay) it.

        Ensures that the person who authorises a transaction is not the same
        person who carries out the payment or execution, preventing
        unauthorised fund movement.

        Args:
            user: The user attempting the execute/pay action.
            resource: The accounting resource being executed.
                Must have an ``approved_by`` attribute.

        Returns:
            dict: Result with ``allowed``, ``reason``, and ``requires_escalation`` keys.
        """
        if hasattr(resource, "approved_by") and resource.approved_by == user.id:
            return {
                "allowed": False,
                "reason": (
                    "Người phê duyệt không được thực hiện thanh toán. "
                    "Segregation of Duties violation: approver cannot execute own approved entry."
                ),
                "requires_escalation": False,
            }
        return {
            "allowed": True,
            "reason": "SoD check passed: user is not the approver.",
            "requires_escalation": False,
        }

    @staticmethod
    def check_period_lock(resource):
        """Deny operations on resources belonging to a locked or closed period.

        Accounting periods that have been locked or closed must not accept
        new entries or modifications. This is a core requirement for
        financial period integrity.

        Args:
            resource: The accounting resource to check.
                Must have an ``accounting_period`` attribute (YYYY-MM string).

        Returns:
            dict: Result with ``allowed``, ``reason``, and ``requires_escalation`` keys.
        """
        from app.models.period import AccountingPeriod

        period_str = getattr(resource, "accounting_period", None)
        if not period_str:
            return {
                "allowed": True,
                "reason": "No accounting period on resource; period lock check skipped.",
                "requires_escalation": False,
            }

        period = AccountingPeriod.query.filter_by(period=period_str).first()
        if period is None:
            return {
                "allowed": True,
                "reason": f"Accounting period {period_str} not found; period lock check skipped.",
                "requires_escalation": False,
            }

        if period.is_locked:
            return {
                "allowed": False,
                "reason": (
                    f"Kỳ kế toán {period.display_name} đã bị khóa. "
                    f"Accounting period {period_str} is locked."
                ),
                "requires_escalation": False,
            }

        if period.is_closed:
            return {
                "allowed": False,
                "reason": (
                    f"Kỳ kế toán {period.display_name} đã đóng hoàn toàn. "
                    f"Accounting period {period_str} is closed."
                ),
                "requires_escalation": False,
            }

        return {
            "allowed": True,
            "reason": f"Period {period.display_name} is open.",
            "requires_escalation": False,
        }

    @staticmethod
    def check_amount_threshold(amount, user):
        """Check if the transaction amount exceeds the 1 billion VND threshold.

        Transactions exceeding 1,000,000,000 VND require escalated approval
        from a CFO or higher role. Users with ``cfo`` or ``admin`` roles
        may proceed; others receive a warning and escalation flag.

        Args:
            amount: The transaction amount as a Decimal or numeric value.
            user: The user attempting the transaction. Must have a
                ``get_all_roles()`` method returning a set of role names.

        Returns:
            dict: Result with ``allowed``, ``reason``, and ``requires_escalation`` keys.
                - ``allowed`` is True but ``requires_escalation`` is True when the
                  amount exceeds the threshold and the user lacks elevated privileges.
                - ``allowed`` is True with no escalation for users with cfo/admin roles.
        """
        amount = Decimal(str(amount))
        if amount <= RuleEngine.AMOUNT_THRESHOLD_VND:
            return {
                "allowed": True,
                "reason": f"Amount {amount:,.0f} VND is within threshold.",
                "requires_escalation": False,
            }

        user_roles = user.get_all_roles() if hasattr(user, "get_all_roles") else set()
        elevated_roles = {"admin", "cfo"}

        if user_roles & elevated_roles:
            return {
                "allowed": True,
                "reason": (
                    f"Amount {amount:,.0f} VND exceeds 1B threshold, "
                    f"but user has elevated role ({', '.join(user_roles & elevated_roles)})."
                ),
                "requires_escalation": False,
            }

        return {
            "allowed": True,
            "reason": (
                f"Số tiền {amount:,.0f} VND vượt ngưỡng 1 tỷ đồng, "
                f"cần phê duyệt bởi CFO hoặc cao hơn. "
                f"Amount {amount:,.0f} VND exceeds 1B threshold; escalation required."
            ),
            "requires_escalation": True,
        }
