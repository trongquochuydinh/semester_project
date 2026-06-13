from api.domain.user import CreateUserResult, CurrentUserProfile, UserProfile, UserStats
from api.schemas import (
    UserCountResponse,
    UserCreateResponse,
    UserEditResponse,
    UserGetResponse,
)
from api.schemas.auth_schema import OAuthInfo


def user_profile_to_get_response(profile: UserProfile) -> UserGetResponse:
    return UserGetResponse(
        username=profile.username,
        email=profile.email,
        company_id=profile.company_id,
        role=profile.role,
    )


def user_profile_to_edit_response(profile: UserProfile) -> UserEditResponse:
    return UserEditResponse(
        username=profile.username,
        email=profile.email,
        company_id=profile.company_id,
        role=profile.role,
    )


def create_user_result_to_response(result: CreateUserResult) -> UserCreateResponse:
    return UserCreateResponse(
        message=result.message,
        initial_password=result.initial_password,
    )


def user_stats_to_response(stats: UserStats) -> UserCountResponse:
    return UserCountResponse(
        total_users=stats.total_users,
        online_users=stats.online_users,
    )


def current_user_profile_to_dict(profile: CurrentUserProfile) -> dict:
    return {
        "id": profile.id,
        "username": profile.username,
        "role": profile.role,
        "company_id": profile.company_id,
        "oauth_info": OAuthInfo(github=profile.oauth_github),
    }
