from app.core.utils import generate_4_digits
from app.modules.verification.exceptions import VerificationCodeCrudInsertError
from app.modules.verification.schemas import VerificationCodeFromDB


async def create_code(db, user_id: int) -> VerificationCodeFromDB | None:
    """
    Create a verification code for a user.
    """

    query = """
        INSERT INTO verification_codes (user_id, code) 
        VALUES (:user_id, :code)
        RETURNING id, user_id, code, created_at
        ;
    """

    code = generate_4_digits()

    row = await db.fetch_one(
        query,
        {
            "user_id": user_id,
            "code": code,
        },
    )

    if not row:
        raise VerificationCodeCrudInsertError

    return VerificationCodeFromDB(**row)


async def get_valid_code(db, user_id: int, code: str) -> VerificationCodeFromDB | None:
    """
    Get user verification code from string code.
    """

    query = """
        SELECT id, user_id, code, created_at
        FROM verification_codes
        WHERE 
            user_id = :user_id
            AND code = :code
            AND created_at > NOW() - INTERVAL '1 minute'
        ;
    """

    row = await db.fetch_one(
        query,
        {
            "user_id": user_id,
            "code": code,
        },
    )

    if not row:
        return None

    return VerificationCodeFromDB(**row)
